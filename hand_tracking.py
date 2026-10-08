"""
hand_tracking.py
Wraps MediaPipe Hands. It takes a camera frame and returns the 21 hand landmarks.

MediaPipe's hand model is PRETRAINED by Google. We do not train it ourselves.
"""
import cv2
import mediapipe as mp

import config


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # video mode: tracks between frames (faster)
            max_num_hands=config.MAX_NUM_HANDS,
            model_complexity=config.MODEL_COMPLEXITY,
            min_detection_confidence=config.DETECTION_CONFIDENCE,
            min_tracking_confidence=config.TRACKING_CONFIDENCE,
        )

    def find_hand(self, frame_bgr):
        """Return the first detected hand's landmarks, or None if no hand."""
        # MediaPipe expects RGB, but OpenCV gives BGR, so we convert.
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0]
        return None

    @staticmethod
    def get_landmark_positions(hand_landmarks, frame_shape):
        """
        MediaPipe gives x, y as fractions (0 to 1) of the image size.
        We convert them to pixel positions: [(x0, y0), (x1, y1), ... (x20, y20)].
        """
        height, width = frame_shape[:2]
        return [(int(lm.x * width), int(lm.y * height))
                for lm in hand_landmarks.landmark]

    def draw_landmarks(self, frame, hand_landmarks):
        """Draw the hand skeleton on the frame."""
        self.mp_draw.draw_landmarks(
            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def close(self):
        self.hands.close()
