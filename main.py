"""
main.py
AI Virtual Drawing Board - run with:  python main.py
Optional phone viewer:                python main.py --phone
"""
import argparse
import os
import time

import cv2
import numpy as np

import config
import gesture_recognition as gr
import ui
from drawing_canvas import DrawingCanvas
from hand_tracking import HandTracker


def open_camera():
    """Open the webcam. Returns None if it cannot be opened."""
    cap = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)  # DirectShow is reliable on Windows
    if not cap.isOpened():
        cap.release()
        cap = cv2.VideoCapture(config.CAMERA_INDEX)
    if not cap.isOpened():
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    return cap


def show_camera_error():
    img = np.zeros((300, 800, 3), dtype=np.uint8)
    ui.put_text(img, "Camera not found. Please check your webcam.", (40, 140), 0.9, ui.RED, 2)
    ui.put_text(img, "Close other apps using the camera, or change CAMERA_INDEX in config.py",
                (40, 190), 0.55, ui.WHITE, 1)
    cv2.imshow(config.WINDOW_NAME, img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()


def select_tool(canvas, name):
    if name == "ERASER":
        canvas.eraser = True
    else:
        canvas.color_name = name
        canvas.eraser = False


def save_drawing(canvas):
    try:
        path = canvas.save(config.DRAWINGS_DIR)
        print("Saved:", path)
        return "Drawing saved successfully!"
    except Exception as error:
        print("Save error:", error)
        return "Save failed (see terminal)"


def setup_phone():
    """Start the optional phone viewer. Returns (url, qr_path) or (None, None)."""
    try:
        import phone_server
        url = phone_server.start_server()
        qr_path = os.path.join(config.ASSETS_DIR, "phone_qr.png")
        os.makedirs(config.ASSETS_DIR, exist_ok=True)
        phone_server.make_qr(url, qr_path)
        print("Phone viewer running at:", url)
        print("Phone must be on the same Wi-Fi. Press P in the app to show the QR code.")
        return url, qr_path
    except ImportError:
        print("Phone feature needs: pip install -r requirements-optional.txt")
        return None, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phone", action="store_true", help="enable optional phone viewer")
    args = parser.parse_args()

    cap = open_camera()
    if cap is None:
        print("Camera not found. Please check your webcam.")
        show_camera_error()
        return

    tracker = HandTracker()
    canvas = DrawingCanvas(config.FRAME_WIDTH, config.FRAME_HEIGHT, config.BOUNDARY)
    stabilizer = gr.GestureStabilizer(config.STABLE_FRAMES)

    phone_url, qr_path = (setup_phone() if args.phone else (None, None))
    qr_visible = False

    message, message_until = "", 0.0
    last_action = {"CLEAR": 0.0, "SAVE": 0.0}
    consumed = {"CLEAR": False, "SAVE": False}   # True = action already done; release gesture to re-arm
    hover_name, hover_start = None, 0.0
    prev_time, fps = time.time(), 0.0

    def set_message(text):
        nonlocal message, message_until
        message, message_until = text, time.time() + config.MESSAGE_SECONDS

    print("AI Virtual Drawing Board started. Press ESC in the window to exit.")

    while True:
        ok, frame = cap.read()
        if not ok or frame is None:
            print("Camera not found. Please check your webcam.")
            break

        frame = cv2.flip(frame, 1)                     # mirror view feels natural
        frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
        now = time.time()

        # ---------- 1. AI part: detect hand, get landmarks, find gesture ----------
        hand = tracker.find_hand(frame)
        raw_gesture, tip = "NONE", None
        if hand is not None:
            landmarks = tracker.get_landmark_positions(hand, frame.shape)
            raw_gesture = gr.detect_gesture(landmarks)
            tip = landmarks[gr.INDEX_TIP]              # landmark 8 = index fingertip
            tracker.draw_landmarks(frame, hand)
        stable = stabilizer.update(raw_gesture)

        # Re-arm clear/save once the gesture is released
        if stable != "FIST":
            consumed["CLEAR"] = False
        if stable != "THUMB_UP":
            consumed["SAVE"] = False
        if stable != "TWO_FINGERS":
            hover_name = None

        # ---------- 2. Action selection ----------
        mode, boundary_state, banner = "IDLE", "-", None
        inside = tip is not None and canvas.inside_boundary(tip)
        if tip is not None:
            boundary_state = "ACTIVE" if inside else "OUT OF AREA"

        if hand is None:
            canvas.end_stroke()
            mode, banner = "NO HAND", ("No hand detected", (200, 200, 200))

        elif stable == "INDEX":
            if inside and canvas.draw(tip):
                mode = "ERASING" if canvas.eraser else "DRAWING"
                banner = ("DRAWING AREA ACTIVE", ui.GREEN)
            else:
                canvas.end_stroke()
                mode = "STOPPED"
                banner = ("OUT OF DRAWING AREA", ui.RED)

        elif stable == "TWO_FINGERS":
            canvas.end_stroke()
            mode = "CURSOR"
            button = ui.hit_test(tip)
            if button:
                if button != hover_name:
                    hover_name, hover_start = button, now
                elif now - hover_start >= config.BUTTON_DWELL_SECONDS:
                    select_tool(canvas, button)
                    set_message(f"Selected {button}")
                    hover_name = None
                else:
                    set_message(f"Hold to select {button}")
            else:
                hover_name = None

        elif stable == "OPEN_PALM":
            canvas.end_stroke()
            mode = "PAUSED"

        elif stable == "FIST":
            canvas.end_stroke()
            mode = "HOLD FIST TO CLEAR"
            if not consumed["CLEAR"] and now - last_action["CLEAR"] > config.ACTION_COOLDOWN:
                held = stabilizer.frames_held
                if held >= config.HOLD_FRAMES_CLEAR:
                    canvas.clear()
                    consumed["CLEAR"] = True
                    last_action["CLEAR"] = now
                    set_message("Canvas Cleared")
                else:
                    set_message(f"Clearing... {int(100 * held / config.HOLD_FRAMES_CLEAR)}%")

        elif stable == "THUMB_UP":
            canvas.end_stroke()
            mode = "HOLD THUMB UP TO SAVE"
            if not consumed["SAVE"] and now - last_action["SAVE"] > config.ACTION_COOLDOWN:
                held = stabilizer.frames_held
                if held >= config.HOLD_FRAMES_SAVE:
                    set_message(save_drawing(canvas))
                    consumed["SAVE"] = True
                    last_action["SAVE"] = now
                else:
                    set_message(f"Saving... {int(100 * held / config.HOLD_FRAMES_SAVE)}%")

        else:
            canvas.end_stroke()     # unknown gesture: do nothing safely
            mode = "IDLE"

        # ---------- 3. Build the screen ----------
        selected = "ERASER" if canvas.eraser else canvas.color_name
        camera_view = frame
        ui.draw_toolbar(camera_view, selected, hover_name)
        ui.draw_boundary(camera_view, "ACTIVE" if inside else ("OUT" if tip is not None else "-"))

        canvas_view = canvas.canvas.copy()
        ui.draw_boundary(canvas_view, "-")

        if tip is not None:
            pointer_color = ui.GREEN if mode in ("DRAWING", "ERASING") else \
                            (255, 120, 0) if mode == "CURSOR" else ui.RED
            cv2.circle(camera_view, tip, 9, pointer_color, 2)
            cv2.circle(canvas_view, tip, 9, pointer_color, 2)

        if banner:
            ui.draw_banner(camera_view, banner[0], banner[1])

        fps = 0.9 * fps + 0.1 * (1.0 / max(now - prev_time, 1e-3))
        prev_time = now

        info = {
            "gesture": raw_gesture if raw_gesture != "NONE" else "NONE",
            "mode": mode,
            "color": "ERASER" if canvas.eraser else canvas.color_name,
            "size": canvas.size_name,
            "boundary": boundary_state,
            "fps": fps,
            "message": message if now < message_until else "",
        }
        cv2.imshow(config.WINDOW_NAME, ui.compose_window(camera_view, canvas_view, info))

        # ---------- 4. Keyboard ----------
        key = cv2.waitKey(1) & 0xFF
        if key == 27:                                   # ESC
            break
        ch = chr(key).lower() if key != 255 else ""
        if len(ch) == 1:
            if ch in config.COLOR_KEYS:
                select_tool(canvas, config.COLOR_KEYS[ch])
            elif ch in config.SIZE_KEYS:
                canvas.size_name = config.SIZE_KEYS[ch]
            elif ch == "x":
                canvas.eraser = True
            elif ch == "b":
                canvas.eraser = False
            elif ch == "c":
                canvas.clear()
                set_message("Canvas Cleared")
            elif ch == "u":
                set_message("Undo done" if canvas.undo() else "Nothing to undo")
            elif ch == "r":
                set_message("Redo done" if canvas.redo() else "Nothing to redo")
            elif ch == "s":
                set_message(save_drawing(canvas))
            elif ch == "p":
                if qr_path and os.path.exists(qr_path):
                    qr_visible = not qr_visible
                    if qr_visible:
                        cv2.imshow("Scan with phone: " + str(phone_url), cv2.imread(qr_path))
                    else:
                        cv2.destroyWindow("Scan with phone: " + str(phone_url))
                else:
                    set_message("Phone feature off. Run: python main.py --phone")

        # Window closed with the X button?
        if cv2.getWindowProperty(config.WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()
    print("Application closed.")


if __name__ == "__main__":
    main()
