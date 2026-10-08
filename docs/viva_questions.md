# Viva Questions and Answers

1. **What is your project?** A virtual drawing board where you draw in the air with hand gestures using a webcam.
2. **Why is it AI?** It uses a pretrained deep-learning hand model (MediaPipe) and computer vision to understand hands and gestures.
3. **Did you train a model?** No. MediaPipe's model is pretrained. We built feature extraction and rule-based gesture logic on top.
4. **What is computer vision?** Teaching computers to understand images and video.
5. **What is OpenCV?** A library for image processing, camera access and drawing.
6. **What is MediaPipe?** A Google framework with ready-made ML solutions, including hand tracking.
7. **What are hand landmarks?** 21 key points on a hand (wrist, joints, fingertips).
8. **Which landmark is the index fingertip?** Number 8.
9. **How do you know a finger is up?** Its tip is clearly farther from the wrist than its middle joint.
10. **How do you detect a fist?** All four fingers are folded, and thumbs-up is excluded.
11. **How do you detect thumbs-up?** Thumb extended and pointing upward with the other fingers folded.
12. **What is gesture recognition?** Identifying meaningful hand shapes and mapping them to actions.
13. **What is the drawing boundary?** A rectangle where drawing is allowed. Outside it, drawing stops.
14. **How is the boundary checked?** We test whether x and y are between the rectangle limits.
15. **What is coordinate mapping?** Landmark values are fractions (0 to 1); we convert them to pixels, which map to the canvas.
16. **Why flip the frame?** A mirror view feels natural: moving right moves the pointer right.
17. **Why convert BGR to RGB?** OpenCV uses BGR but MediaPipe expects RGB.
18. **What is smoothing?** Averaging the new and previous position to reduce shaking.
19. **What is interpolation here?** Drawing a line between previous and current points so there are no gaps.
20. **What is debouncing?** Requiring a gesture to repeat for several frames so one wrong frame cannot trigger an action.
21. **Why hold a fist to clear?** To prevent accidental clearing.
22. **How does undo work?** We store canvas copies in a stack and restore the last one.
23. **Why is the saved PNG clean?** It is saved from the white canvas, not the camera image.
24. **Why one hand only?** Simpler and more reliable; we set max_num_hands=1.
25. **What is FPS?** Frames processed per second. Higher means smoother.
26. **Why use a virtual environment?** To keep project packages separate and avoid version conflicts.
27. **What affects accuracy?** Lighting, background, camera quality, hand angle and distance.
28. **What are the limitations?** Lighting dependence, gesture misclassification, hand fatigue, no touch feedback.
29. **How can you improve it?** Train a deep-learning gesture classifier, add handwriting recognition and multi-hand support.
30. **What are real applications?** Online teaching, presentations, accessibility tools, touchless kiosks.
31. **Is the phone feature required?** No. It is optional and works only on the same Wi-Fi.
