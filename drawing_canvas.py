"""
drawing_canvas.py
The virtual canvas: smooth drawing, erasing, undo/redo, clear and save.
The canvas is a plain white image, so the camera picture never gets saved.
"""
import os
from datetime import datetime

import cv2
import numpy as np

import config


class DrawingCanvas:
    def __init__(self, width, height, boundary):
        self.width = width
        self.height = height
        self.boundary = boundary                   # (x1, y1, x2, y2)
        self.canvas = np.full((height, width, 3), 255, dtype=np.uint8)

        self.color_name = config.DEFAULT_COLOR
        self.size_name = config.DEFAULT_SIZE
        self.eraser = False

        self.prev_point = None      # last point drawn (None = no stroke in progress)
        self.smooth_point = None    # smoothed fingertip position

        self.undo_stack = []
        self.redo_stack = []

    # ---------- helpers ----------
    def inside_boundary(self, point):
        x, y = point
        x1, y1, x2, y2 = self.boundary
        return x1 <= x <= x2 and y1 <= y <= y2

    def thickness(self):
        sizes = config.ERASER_SIZES if self.eraser else config.BRUSH_SIZES
        return sizes[self.size_name]

    def draw_color(self):
        if self.eraser:
            return (255, 255, 255)   # erasing = painting white
        return config.COLORS[self.color_name]

    def _push_undo(self):
        """Save a copy of the canvas before it changes."""
        self.undo_stack.append(self.canvas.copy())
        if len(self.undo_stack) > config.MAX_UNDO:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    # ---------- drawing ----------
    def draw(self, point):
        """
        Draw using the fingertip position. Returns True if drawing happened.
        Steps: smooth the point -> check boundary -> draw a line from the previous point.
        """
        x, y = point

        # Exponential smoothing: new = alpha*current + (1-alpha)*previous
        if self.smooth_point is None:
            sx, sy = float(x), float(y)
        else:
            a = config.SMOOTHING_ALPHA
            sx = a * x + (1 - a) * self.smooth_point[0]
            sy = a * y + (1 - a) * self.smooth_point[1]
        self.smooth_point = (sx, sy)
        current = (int(sx), int(sy))

        # Safety: never draw outside the boundary.
        if not self.inside_boundary(current):
            self.end_stroke()
            return False

        color = self.draw_color()
        thick = self.thickness()

        if self.prev_point is None:
            # A new stroke begins: save for undo and draw a dot.
            self._push_undo()
            cv2.circle(self.canvas, current, max(1, thick // 2), color, -1, cv2.LINE_AA)
        else:
            moved = np.hypot(current[0] - self.prev_point[0], current[1] - self.prev_point[1])
            if moved < config.MIN_MOVE_PIXELS:
                return True       # too small a move, ignore to reduce jitter
            # Connect the previous point to the current point (no gaps).
            cv2.line(self.canvas, self.prev_point, current, color, thick, cv2.LINE_AA)

        self.prev_point = current
        return True

    def end_stroke(self):
        """Stop the current line. The next drawing starts a new, unconnected stroke."""
        self.prev_point = None
        self.smooth_point = None

    # ---------- canvas actions ----------
    def clear(self):
        self._push_undo()
        self.canvas[:] = 255
        self.end_stroke()

    def undo(self):
        if not self.undo_stack:
            return False
        self.redo_stack.append(self.canvas.copy())
        self.canvas = self.undo_stack.pop()
        self.end_stroke()
        return True

    def redo(self):
        if not self.redo_stack:
            return False
        self.undo_stack.append(self.canvas.copy())
        self.canvas = self.redo_stack.pop()
        self.end_stroke()
        return True

    def save(self, folder):
        """Save ONLY the drawing area as a PNG. Returns the file path."""
        os.makedirs(folder, exist_ok=True)
        x1, y1, x2, y2 = self.boundary
        crop = self.canvas[y1:y2, x1:x2]

        stamp = datetime.now().strftime("drawing_%Y_%m_%d_%H%M%S")
        path = os.path.join(folder, stamp + ".png")
        counter = 1
        while os.path.exists(path):             # avoid overwriting in the same second
            path = os.path.join(folder, f"{stamp}_{counter}.png")
            counter += 1

        ok, buffer = cv2.imencode(".png", crop)
        if not ok:
            raise RuntimeError("PNG encoding failed")
        buffer.tofile(path)   # works even if the folder name has special characters
        return path
