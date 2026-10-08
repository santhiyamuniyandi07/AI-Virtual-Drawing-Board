"""
gesture_recognition.py
Decides which gesture the hand is making using the 21 landmark positions.

Landmark numbers used (MediaPipe Hands):
  0 = wrist
  Thumb : 1 CMC, 2 MCP, 3 IP,  4 TIP
  Index : 5 MCP, 6 PIP, 7 DIP, 8 TIP
  Middle: 9 MCP, 10 PIP, 11 DIP, 12 TIP
  Ring  : 13 MCP, 14 PIP, 15 DIP, 16 TIP
  Pinky : 17 MCP, 18 PIP, 19 DIP, 20 TIP
(TIP = fingertip, MCP = knuckle, PIP/DIP/IP = middle joints)

Main idea: a finger is "up" when its tip is much farther from the wrist than its
middle joint (PIP). A curled finger has its tip close to the palm. Because we use
distances (not "up/down" directions), tilted hands also work.
"""
import math

WRIST = 0
THUMB_MCP, THUMB_IP, THUMB_TIP = 2, 3, 4
INDEX_MCP, INDEX_TIP = 5, 8
MIDDLE_MCP = 9
PINKY_MCP = 17

# (tip, pip) pairs for index, middle, ring, pinky
FINGER_JOINTS = [(8, 6), (12, 10), (16, 14), (20, 18)]

UP_RATIO = 1.1  # tip must be 10% farther from wrist than PIP to count as "up"


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def palm_size(lm):
    """Distance wrist -> middle knuckle. Used to make rules work at any distance from the camera."""
    return max(_dist(lm[WRIST], lm[MIDDLE_MCP]), 1.0)


def is_thumb_extended(lm):
    """Thumb is out if its tip is far from the index knuckle and farther than its own joint from the pinky."""
    palm = palm_size(lm)
    far_from_index = _dist(lm[THUMB_TIP], lm[INDEX_MCP]) > 0.6 * palm
    tip_beyond_joint = _dist(lm[THUMB_TIP], lm[PINKY_MCP]) > _dist(lm[THUMB_IP], lm[PINKY_MCP])
    return far_from_index and tip_beyond_joint


def detect_fingers(lm):
    """Return [thumb, index, middle, ring, pinky] where 1 = up and 0 = folded."""
    fingers = [1 if is_thumb_extended(lm) else 0]
    for tip, pip in FINGER_JOINTS:
        up = _dist(lm[tip], lm[WRIST]) > UP_RATIO * _dist(lm[pip], lm[WRIST])
        fingers.append(1 if up else 0)
    return fingers


def is_index_up(fingers):
    """Only the index finger is up (thumb is ignored)."""
    return fingers[1] == 1 and fingers[2:] == [0, 0, 0]


def is_two_finger_gesture(fingers):
    """Index and middle up, ring and pinky down (thumb ignored)."""
    return fingers[1:] == [1, 1, 0, 0]


def is_open_palm(fingers):
    """All four fingers up."""
    return sum(fingers[1:]) == 4


def is_thumb_up(lm, fingers):
    """Thumb out and pointing upward, all other fingers folded."""
    if fingers[0] != 1 or sum(fingers[1:]) != 0:
        return False
    palm = palm_size(lm)
    # In image coordinates y grows downward, so "above" means a smaller y.
    pointing_up = lm[THUMB_TIP][1] < lm[INDEX_MCP][1] - 0.25 * palm
    return pointing_up


def is_fist(fingers):
    """All four fingers folded (thumb up is checked before this in detect_gesture)."""
    return sum(fingers[1:]) == 0


def detect_gesture(lm):
    """
    Return one of: OPEN_PALM, INDEX, TWO_FINGERS, THUMB_UP, FIST, UNKNOWN.
    The order matters so that gestures do not overlap.
    """
    fingers = detect_fingers(lm)
    if is_open_palm(fingers):
        return "OPEN_PALM"
    if is_index_up(fingers):
        return "INDEX"
    if is_two_finger_gesture(fingers):
        return "TWO_FINGERS"
    if is_thumb_up(lm, fingers):
        return "THUMB_UP"
    if is_fist(fingers):
        return "FIST"
    return "UNKNOWN"


class GestureStabilizer:
    """
    Debouncing. A new gesture only becomes "stable" after it appears in several
    frames in a row, so one wrong frame cannot clear or save the drawing.
    """

    def __init__(self, stable_frames):
        self.stable_frames = stable_frames
        self.candidate = "NONE"
        self.count = 0
        self.stable = "NONE"

    def update(self, raw_gesture):
        if raw_gesture == self.candidate:
            self.count += 1
        else:
            self.candidate = raw_gesture
            self.count = 1
        if raw_gesture == "NONE":
            self.stable = "NONE"          # hand lost: react immediately
        elif self.count >= self.stable_frames:
            self.stable = self.candidate
        return self.stable

    @property
    def frames_held(self):
        """How many frames in a row the current stable gesture has been shown."""
        return self.count if self.candidate == self.stable else 0
