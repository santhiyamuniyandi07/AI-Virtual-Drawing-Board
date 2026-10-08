# 🎨 AI-Based Virtual Drawing Board

> **Draw in the air using real-time hand gestures!**
> An AI and Computer Vision based virtual drawing application that uses a laptop webcam to track hand movements and convert finger gestures into digital drawings.

## 📌 Project Overview

The **AI-Based Virtual Drawing Board** is a software-only Computer Vision project that allows users to draw on a virtual canvas without using a physical mouse, touchscreen, or special hardware.

The laptop webcam captures the user's hand movements. **MediaPipe Hands** detects and tracks hand landmarks, while **OpenCV** processes the webcam frames. The system identifies specific hand gestures using landmark geometry and performs actions such as drawing, selecting colors, clearing the canvas, saving drawings, and pausing the application.

### 🎯 Project Workflow

```text
Laptop Webcam
      ↓
Hand Detection
      ↓
21 Hand Landmarks
      ↓
Fingertip Tracking
      ↓
Gesture Recognition
      ↓
Action Detection
      ↓
Virtual Canvas
      ↓
Real-Time Display
```

## ✨ Features

* 🖐️ Real-time hand tracking
* 📍 Detection of 21 hand landmarks
* ☝️ Index-finger based drawing
* ✌️ Two-finger cursor/selection mode
* ✊ Fist gesture for clearing the canvas
* 👍 Thumb-up gesture for saving drawings
* 🖐️ Open-palm gesture for pause
* 🎨 Multiple drawing colors
* 🖌️ Multiple brush sizes
* 🧹 Eraser mode
* ↩️ Undo functionality
* ↪️ Redo functionality
* 🚧 Safe drawing-area boundary
* ⚠️ Warning when the fingertip leaves the drawing area
* 📸 Save drawings as timestamped PNG files
* 📱 Optional phone viewer using Flask and QR code
* ✨ Smooth drawing using interpolation and smoothing techniques

## 🧠 AI and Computer Vision

This project uses **MediaPipe Hands**, a pretrained hand-tracking solution, to detect hand landmarks from webcam frames.

The project does **not train a new deep-learning model**. Instead, gesture recognition is implemented using rules based on the positions and geometry of detected hand landmarks.

The system analyzes the relationship between landmarks to determine whether the user is:

* Drawing
* Selecting a tool/color
* Clearing the canvas
* Saving the drawing
* Pausing the application

## 👋 Gesture Controls

| Hand Gesture             | Action          |
| ------------------------ | --------------- |
| ☝️ Index finger up       | Draw            |
| ✌️ Index + Middle finger | Cursor / Select |
| ✊ Fist                   | Clear canvas    |
| 👍 Thumb up              | Save drawing    |
| 🖐️ Open palm            | Pause           |

## ⌨️ Keyboard Controls

| Key     | Function               |
| ------- | ---------------------- |
| `1 - 6` | Select colors          |
| `Q`     | Small brush            |
| `W`     | Medium brush           |
| `E`     | Large brush            |
| `X`     | Eraser                 |
| `B`     | Brush                  |
| `C`     | Clear canvas           |
| `U`     | Undo                   |
| `R`     | Redo                   |
| `S`     | Save drawing           |
| `P`     | Show QR / Phone viewer |
| `ESC`   | Exit application       |

## 🛠️ Technologies Used

* **Python 3.11**
* **OpenCV**
* **MediaPipe**
* **NumPy**
* **Flask** – Optional phone viewer
* **qrcode** – Optional QR functionality

## 🏗️ Project Architecture

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Hands
   ↓
Hand Landmarks
   ↓
Gesture Recognition
   ↓
Action Controller
   ↓
Drawing Canvas
   ↓
User Interface
```

## 📂 Project Structure

```text
AI-Virtual-Drawing-Board/
│
├── assets/
│
├── docs/
│   └── project_report.md
│
├── drawings/
│
├── screenshots/
│
├── config.py
├── drawing_canvas.py
├── gesture_recognition.py
├── hand_tracking.py
├── main.py
├── phone_server.py
├── ui.py
│
├── requirements.txt
├── requirements-optional.txt
├── .gitignore
└── README.md
```

## 💻 System Requirements

### Hardware

* Laptop/Desktop
* Working webcam
* Minimum 4 GB RAM
* Keyboard
* Good lighting environment

### Software

* Windows 10/11
* Python 3.11
* VS Code
* Git
* Webcam drivers

## ⚙️ Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/santhiyamuniyandi07/AI-Virtual-Drawing-Board.git
cd AI-Virtual-Drawing-Board
```

### 2. Create Virtual Environment

```powershell
py -3.11 -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### 5. Install Required Packages

```powershell
pip install -r requirements.txt
```

## ▶️ Run the Project

Start the virtual drawing board using:

```powershell
python main.py
```

The webcam will open and the application will begin detecting hand movements.

## 📱 Optional Phone Viewer

The project also includes an optional phone-viewing feature.

Install the optional packages:

```powershell
pip install -r requirements-optional.txt
```

Then run:

```powershell
python main.py --phone
```

The phone viewer allows the drawing output to be accessed through a browser on a device connected to the same network.

## 🚧 Drawing Boundary

A dedicated drawing area is provided to prevent unwanted drawings outside the permitted region.

When the fingertip moves outside the defined drawing boundary:

```text
OUT OF DRAWING AREA
```

is displayed and drawing is stopped.

This feature improves drawing control and prevents accidental marks outside the canvas.

## 🧪 Testing

The project was tested for:

| Test Case            | Expected Result                |
| -------------------- | ------------------------------ |
| Webcam detection     | Webcam opens successfully      |
| Hand detection       | Hand landmarks detected        |
| Index finger gesture | Drawing starts                 |
| Two-finger gesture   | Cursor/selection mode          |
| Fist gesture         | Canvas cleared                 |
| Thumb-up gesture     | Drawing saved                  |
| Open palm            | Drawing paused                 |
| Boundary crossing    | Drawing stops                  |
| Eraser               | Existing drawing can be erased |
| Undo                 | Previous action removed        |
| Redo                 | Removed action restored        |
| Save                 | PNG file generated             |

Detailed testing information is available in:

```text
docs/project_report.md
```

## 📸 Screenshots

Screenshots demonstrating the project can be added here:

```text
screenshots/
├── main_window.png
├── drawing_demo.png
└── boundary_warning.png
```

## 🤖 AI Tools Used During Development

AI-assisted development tools were used during the development and learning process.

### ChatGPT

Used for:

* Understanding Python and Computer Vision concepts
* Debugging errors
* Explaining code
* Improving project structure
* Documentation support
* Testing and troubleshooting guidance

### Claude

Used for:

* Exploring implementation approaches
* Generating development ideas
* Code assistance
* Project documentation
* Debugging and refinement

The final project was **reviewed, configured, tested, and customized during development** to meet the project's requirements.

## 📚 Learning Outcomes

Through this project, I gained practical experience in:

* Python programming
* Computer Vision
* OpenCV
* MediaPipe
* Hand landmark detection
* Real-time image processing
* Gesture recognition
* GUI development
* File handling
* Git and GitHub
* AI-assisted software development
* Debugging and testing

## ⚠️ Limitations

* Performance depends on webcam quality.
* Poor lighting can affect hand detection.
* Complex backgrounds may reduce tracking accuracy.
* The current system is designed primarily for one-hand interaction.
* Gesture recognition is rule-based.
* Very fast hand movements may affect drawing smoothness.

## 🚀 Future Enhancements

Possible future improvements include:

* Deep-learning based gesture classification
* Handwriting recognition
* Shape recognition
* Multi-hand interaction
* Voice commands
* More drawing tools
* Mobile application integration
* Cloud-based drawing storage
* AI-based automatic shape correction
* Mathematical equation recognition

## 🌍 Applications

This project can be useful for:

* Digital education
* Online teaching
* Interactive presentations
* Touch-free interfaces
* Creative drawing applications
* Accessibility-focused interfaces
* Human-computer interaction research
* AI and Computer Vision demonstrations

## 👩‍💻 Author

**Santhiya Muniyandi**

B.Sc. Artificial Intelligence and Machine Learning
Arasu College of Arts and Science for Women
Karur, Tamil Nadu

GitHub: **santhiyamuniyandi07**

