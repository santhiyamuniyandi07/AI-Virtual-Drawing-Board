"""
ui.py
Everything that is drawn on the screen: toolbar, boundary, banners, status panel.
"""
import cv2
import numpy as np

import config

FONT = cv2.FONT_HERSHEY_SIMPLEX
GREEN = (0, 200, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)


def put_text(img, text, pos, scale=0.6, color=WHITE, thickness=1):
    cv2.putText(img, text, pos, FONT, scale, color, thickness, cv2.LINE_AA)


def get_toolbar_buttons():
    """6 color buttons + 1 eraser button, each 80x44 pixels."""
    buttons = []
    x = 10
    for name in config.COLORS:
        buttons.append({"name": name, "rect": (x, 8, x + 80, 52)})
        x += 88
    buttons.append({"name": "ERASER", "rect": (x, 8, x + 80, 52)})
    return buttons


def hit_test(point):
    """Return the toolbar button name under the point, or None."""
    px, py = point
    for b in get_toolbar_buttons():
        x1, y1, x2, y2 = b["rect"]
        if x1 <= px <= x2 and y1 <= py <= y2:
            return b["name"]
    return None


def draw_toolbar(frame, selected_name, hover_name):
    width = frame.shape[1]
    cv2.rectangle(frame, (0, 0), (width, config.TOOLBAR_HEIGHT), (35, 35, 35), -1)
    for b in get_toolbar_buttons():
        x1, y1, x2, y2 = b["rect"]
        name = b["name"]
        if name == "ERASER":
            fill, text_color = (200, 200, 200), (0, 0, 0)
        else:
            fill = config.COLORS[name]
            brightness = 0.114 * fill[0] + 0.587 * fill[1] + 0.299 * fill[2]
            text_color = (0, 0, 0) if brightness > 150 else WHITE
        cv2.rectangle(frame, (x1, y1), (x2, y2), fill, -1)
        if name == selected_name:
            cv2.rectangle(frame, (x1 - 3, y1 - 3), (x2 + 3, y2 + 3), (0, 255, 255), 3)
        elif name == hover_name:
            cv2.rectangle(frame, (x1 - 2, y1 - 2), (x2 + 2, y2 + 2), WHITE, 2)
        put_text(frame, name, (x1 + 6, y1 + 28), 0.45, text_color, 1)


def draw_boundary(frame, state):
    """state: 'ACTIVE' (green), 'OUT' (red), anything else (white)."""
    x1, y1, x2, y2 = config.BOUNDARY
    color = GREEN if state == "ACTIVE" else RED if state == "OUT" else WHITE
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    put_text(frame, "DRAWING AREA", (x1 + 4, y1 - 8), 0.5, color, 1)


def draw_banner(frame, text, color):
    """A message strip at the bottom of the picture."""
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, h - 30), (w, h), (20, 20, 20), -1)
    size = cv2.getTextSize(text, FONT, 0.7, 2)[0]
    put_text(frame, text, ((w - size[0]) // 2, h - 8), 0.7, color, 2)


def compose_window(camera_view, canvas_view, info):
    """Join header + camera + canvas + status panel into one image."""
    h, w = camera_view.shape[:2]
    total_w = w * 2

    header = np.full((50, total_w, 3), (90, 50, 30), dtype=np.uint8)
    put_text(header, "AI VIRTUAL DRAWING BOARD", (20, 34), 0.95, WHITE, 2)
    put_text(header, "Real-Time Hand Gesture Recognition | MediaPipe + OpenCV",
             (total_w - 560, 32), 0.55, (220, 220, 220), 1)

    put_text(canvas_view, "DRAWING CANVAS", (10, 25), 0.6, (90, 90, 90), 2)
    panels = np.hstack([camera_view, canvas_view])

    footer = np.full((170, total_w, 3), (40, 40, 40), dtype=np.uint8)
    lines = [
        f"Gesture : {info['gesture']}",
        f"Mode    : {info['mode']}",
        f"Color   : {info['color']}",
        f"Brush   : {info['size']}",
        f"Boundary: {info['boundary']}",
        f"FPS     : {info['fps']:.0f}",
        f"Message : {info['message']}",
    ]
    y = 24
    for line in lines:
        put_text(footer, line, (15, y), 0.55, WHITE, 1)
        y += 22

    controls = [
        "KEYS: 1-6 Colors | Q/W/E Brush size | X Eraser | B Brush",
        "      C Clear | U Undo | R Redo | S Save | P Phone QR | ESC Exit",
        "GESTURES:",
        "  Index finger up      = DRAW (inside the drawing area)",
        "  Index + middle up    = CURSOR / pick toolbar color (hold)",
        "  Fist (hold)          = CLEAR canvas",
        "  Thumb up (hold)      = SAVE drawing",
        "  Open palm            = PAUSE",
    ]
    y = 22
    for line in controls:
        put_text(footer, line, (w + 15, y), 0.5, (200, 255, 200), 1)
        y += 19

    return np.vstack([header, panels, footer])
