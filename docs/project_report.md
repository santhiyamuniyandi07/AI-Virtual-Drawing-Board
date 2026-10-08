# AI-Based Virtual Drawing Board Using Real-Time Hand Gesture Recognition

## 1. Abstract
Traditional digital drawing depends on a mouse, touchpad or stylus. These devices need physical contact and are hard to use for people with limited mobility, in shared classrooms, or in touchless settings. This project presents an AI-Based Virtual Drawing Board that lets users draw in the air using hand gestures captured by an ordinary webcam. The system uses OpenCV to capture and process video frames in real time and MediaPipe Hands, a pretrained computer-vision model, to detect 21 hand landmarks. From these landmark coordinates, the system extracts features such as the distance of each fingertip from the wrist and classifies gestures using rule-based logic. An index finger draws, two fingers act as a cursor, a fist clears the canvas, a thumbs-up saves the drawing, and an open palm pauses. A virtual canvas supports six colors, three brush sizes, an eraser, and undo and redo. A safe drawing boundary prevents accidental strokes outside the working area. Exponential smoothing and line interpolation make strokes natural, while debouncing and hold-to-confirm logic prevent accidental actions. Drawings are saved as PNG files, and an optional local web viewer with a QR code shows them on a phone. The system runs on a standard Windows laptop without special hardware. Applications include digital teaching, presentations, accessibility, creative drawing and touchless interfaces.

## 2. Introduction
Human-computer interaction is moving from physical devices toward natural interfaces such as voice, touch and gestures. Computer vision lets computers understand video. This project uses a webcam to track the user's hand and convert gestures into drawing commands on a virtual canvas.

## 3. Problem Statement
Conventional drawing tools require physical contact with a mouse, touchscreen or stylus. This raises hygiene concerns in shared spaces, is inconvenient for teachers writing while standing away from a screen, and can be difficult for users with limited fine motor control. Touchscreens and graphics tablets are also costly. There is a need for a low-cost, contactless drawing interface that works with hardware people already own.

## 4. Objectives
1. Detect and track a human hand in real time using a webcam.
2. Extract 21 hand landmarks with MediaPipe Hands.
3. Recognize gestures (draw, cursor, clear, save, pause) from landmark geometry.
4. Provide contactless drawing without a mouse, touchpad or stylus.
5. Apply computer vision techniques to a real interactive application.
6. Improve human-computer interaction through natural gestures.
7. Confine drawing to a safe boundary.
8. Produce smooth lines using smoothing and interpolation.
9. Encourage digital creativity with colors, brush sizes and an eraser.
10. Support accessibility and reduce dependence on physical input devices.
11. Prevent accidental actions using debouncing and hold-to-confirm.

## 5. Existing System
Mouse, touchpad, stylus and touchscreen drawing tools need physical contact and often extra hardware. Many air-drawing demos are simple color-tracking scripts that are sensitive to lighting and lack boundaries, gestures and undo.

## 6. Proposed System
A gesture-based drawing application using MediaPipe hand landmarks and rule-based gesture recognition, with a safe drawing zone, toolbar, smoothing, debouncing, undo/redo and PNG saving.

## 7. Technologies Used
Python 3.11, OpenCV (capture, drawing, display), MediaPipe Hands (pretrained landmarks), NumPy (arrays), Flask and qrcode (optional).

## 8. System Requirements
Hardware: laptop or PC, Intel i3 / Ryzen 3 or better, 4 GB RAM minimum (8 GB recommended), 500 MB free storage, webcam (720p recommended).
Software: Windows 11, Python 3.11, VS Code, OpenCV, MediaPipe, NumPy.

## 9. Methodology
1. Image acquisition: OpenCV reads and mirrors frames.
2. Hand detection: MediaPipe detects a hand in the RGB frame.
3. Landmark extraction: 21 points converted to pixel coordinates.
4. Finger analysis: tip-to-wrist distance compared with joint-to-wrist distance.
5. Gesture classification: rules map finger states to gestures; a stabilizer needs several frames.
6. Coordinate mapping: index fingertip (landmark 8) pixel maps onto the canvas of the same size.
7. Boundary validation: the point is checked against the rectangle.
8. Drawing: the point is smoothed and a line connects it to the previous point.
9. User interaction: toolbar by pointing, keyboard shortcuts, status messages.
10. Saving output: the drawing area is cropped and saved as a timestamped PNG.

## 10. System Architecture
```
Webcam -> OpenCV -> MediaPipe Hands -> 21 Landmarks -> Finger Analysis + Gesture Rules
 -> Stabilizer -> Action (Draw/Cursor/Clear/Save/Pause + boundary check)
 -> Virtual Canvas -> Display -> PNG -> (optional) Flask page -> Phone via QR
```

## 11. Algorithm
1. Start and read settings. 2. Open webcam (error if it fails). 3. Initialize MediaPipe and canvas.
4. Capture, flip, resize frame. 5. Detect hand; if none, end stroke and show "No hand detected".
6. Extract landmarks. 7. Compute finger states and gesture. 8. Stabilize the gesture.
9. Get index fingertip. 10. If INDEX and inside boundary, smooth and draw; else end stroke.
11. TWO_FINGERS: cursor and toolbar dwell selection. 12. FIST / THUMB_UP held long enough and not on cooldown: clear / save.
13. OPEN_PALM: pause. 14. Update UI and read keyboard. 15. Repeat until ESC.

## 12. Flowchart
```
START -> Open Webcam (fail -> "Camera not found" -> EXIT)
 -> Init MediaPipe + Canvas -> Capture Frame
 -> Hand? NO -> "No hand detected" -> next frame
 -> YES -> Landmarks -> Gesture -> Stabilize
    INDEX -> inside boundary? YES draw / NO stop "OUT OF DRAWING AREA"
    TWO FINGERS -> cursor    OPEN PALM -> pause
    FIST (held) -> clear     THUMB UP (held) -> save
 -> Update display + keyboard -> ESC? NO -> next frame / YES -> EXIT
```

## 13. Gesture Recognition
A finger is "up" when its tip is at least 10 percent farther from the wrist than its PIP joint. The thumb uses distance from the index knuckle plus a direction check for thumbs-up. Clear and save need about 0.5 s hold, release before re-firing, and a 2 s cooldown.

## 14. Boundary Detection
A rectangle (60,100)-(580,450) defines the safe zone. Each smoothed fingertip position is tested. Outside means the stroke ends, nothing is drawn and "OUT OF DRAWING AREA" shows.

## 15. AI vs Normal Programming
AI / Computer Vision: MediaPipe pretrained hand model, landmark feature extraction, rule-based gesture classification. Normal programming: canvas, undo stack, toolbar, saving, keyboard. No model was trained in this project.

## 16. Testing
| ID | Input | Expected output | Result |
|---|---|---|---|
| TC01 | Run with webcam | Window opens, camera shows | |
| TC02 | Webcam unplugged | "Camera not found. Please check your webcam." | |
| TC03 | No hand | "No hand detected", no crash | |
| TC04 | Index finger inside box | Line drawn, "DRAWING AREA ACTIVE" | |
| TC05 | Index finger outside box | Drawing stops, "OUT OF DRAWING AREA" | |
| TC06 | Finger returns inside | New stroke, no connecting line | |
| TC07 | Two fingers | Mode CURSOR, no line | |
| TC08 | Two fingers on RED 1 s | Color becomes RED | |
| TC09 | Open palm | PAUSED, no line | |
| TC10 | Fist held 1 s | Canvas clears once | |
| TC11 | Fist held 5 s | Clears only once | |
| TC12 | Thumb up held 1 s | PNG in drawings/, "Drawing saved successfully!" | |
| TC13 | Open saved PNG | Only drawing, no webcam image | |
| TC14 | Keys 1-6 | Color changes | |
| TC15 | Keys Q/W/E | Thickness changes | |
| TC16 | X then draw over a line | Line erased | |
| TC17 | Draw, U, R | Stroke removed then restored | |
| TC18 | Two hands | One hand tracked, no crash | |
| TC19 | Quick gesture changes | No accidental clear/save | |
| TC20 | ESC | Closes cleanly | |

## 17. Results
Fill in after your tests. Example: "The system detected the hand in good lighting and drew smooth strokes at about X FPS on [your laptop]. Boundary protection worked in all trials." Do not claim more than you measured.

## 18. Advantages
Contactless; low cost; no special hardware; intuitive; real-time; accessibility; remote teaching; boundary protection; debouncing; clean PNG output; modular code; works offline.

## 19. Limitations
Lighting dependence; webcam quality; cluttered background; occlusion; rule-based gestures can misclassify; one hand only; no touch feedback; hand fatigue; never 100 percent accurate; thresholds may need tuning.

## 20. Applications
Education, digital classrooms, online teaching, presentations, creative drawing, accessibility, touchless interfaces, smart displays, interactive kiosks, assistive technology.

## 21. Future Enhancements
Deep-learning gesture classifier, multi-hand support, voice commands, mobile app, cloud storage, handwriting recognition, shape recognition, equation recognition, OCR, collaborative drawing.

## 22. Conclusion
The project shows how computer vision can create a contactless drawing interface using only a webcam. With MediaPipe landmarks and rule-based gesture recognition, users can draw, erase, clear and save. The boundary and debouncing improve reliability. It has limits in lighting and gesture sensitivity, but is a solid base for deep-learning gesture classification and handwriting or shape recognition.

## 23. References
1. MediaPipe Hands documentation, Google (developers.google.com/mediapipe)
2. Zhang et al., "MediaPipe Hands: On-device Real-time Hand Tracking," 2020 (arXiv:2006.10214)
3. OpenCV documentation (docs.opencv.org)
4. Python documentation (docs.python.org)
5. NumPy documentation (numpy.org)
