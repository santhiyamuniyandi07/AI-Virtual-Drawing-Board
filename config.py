"""
config.py
All settings live here, so you can tune the project without editing other files.
Colors are in BGR order (Blue, Green, Red), which is how OpenCV stores them.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRAWINGS_DIR = os.path.join(BASE_DIR, "drawings")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

WINDOW_NAME = "AI Virtual Drawing Board"

# ---- Camera ----
CAMERA_INDEX = 0          # 0 = built-in webcam. Try 1 for an external webcam.
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# ---- MediaPipe ----
MAX_NUM_HANDS = 1         # we track only one hand
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.6
MODEL_COMPLEXITY = 0      # 0 = fastest, 1 = more accurate

# ---- Drawing boundary (x1, y1, x2, y2) in camera-frame pixels ----
BOUNDARY = (60, 100, 580, 450)
TOOLBAR_HEIGHT = 60       # toolbar occupies the top 60 pixels of the camera view

# ---- Colors (BGR) ----
COLORS = {
    "BLACK": (0, 0, 0),
    "RED": (0, 0, 255),
    "BLUE": (255, 0, 0),
    "GREEN": (0, 160, 0),
    "YELLOW": (0, 220, 255),
    "PURPLE": (160, 0, 160),
}
DEFAULT_COLOR = "BLUE"

# ---- Brush and eraser sizes (pixels) ----
BRUSH_SIZES = {"SMALL": 4, "MEDIUM": 8, "LARGE": 14}
ERASER_SIZES = {"SMALL": 20, "MEDIUM": 35, "LARGE": 50}
DEFAULT_SIZE = "MEDIUM"

# ---- Keyboard shortcuts ----
COLOR_KEYS = {"1": "BLACK", "2": "RED", "3": "BLUE",
              "4": "GREEN", "5": "YELLOW", "6": "PURPLE"}
SIZE_KEYS = {"q": "SMALL", "w": "MEDIUM", "e": "LARGE"}

# ---- Smoothing ----
SMOOTHING_ALPHA = 0.5     # 0..1. Lower = smoother but slower to follow the finger
MIN_MOVE_PIXELS = 1.5     # ignore tiny movements (reduces jitter)

# ---- Gesture stability and actions ----
STABLE_FRAMES = 3         # a gesture must appear this many frames in a row
HOLD_FRAMES_CLEAR = 15    # hold a fist this many frames (~0.5 s) to clear
HOLD_FRAMES_SAVE = 15     # hold thumbs-up this many frames to save
ACTION_COOLDOWN = 2.0     # seconds between two clear/save actions
BUTTON_DWELL_SECONDS = 0.8  # hold the pointer on a toolbar button this long
MESSAGE_SECONDS = 2.0

MAX_UNDO = 20
