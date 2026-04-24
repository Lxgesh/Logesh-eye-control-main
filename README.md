# 🧠 Advanced Biometric Hands-Free Accessibility Tool v3.0

An intelligent, voice-activated eye-tracking interface that enables complete hands-free computer control. Move your cursor with your gaze, click with blinks, and execute commands using the **Lucy voice assistant**.

---

## 🚀 Overview

This project is a **hands-free human-computer interaction system** designed for accessibility and productivity. It combines computer vision, voice recognition, and automation to allow users to control their computer using only **eyes and voice**.

---

## 🌟 Features

### 🎯 Eye-Gaze Tracking

* 9-point full-screen calibration system
* Real-time iris tracking using facial landmarks
* Adaptive smoothing for stable cursor movement
* Accuracy scoring with performance metrics
* Persistent calibration profiles

---

### 👁️ Blink-Based Controls

* Left eye blink → Left click
* Right eye blink → Right click
* Eye Aspect Ratio (EAR) for precise detection
* Cooldown to prevent accidental clicks

---

### 🎤 Voice Command System

All commands require the wake word **"Lucy"**

| Command        | Action              |
| -------------- | ------------------- |
| Lucy click     | Left click          |
| Lucy right     | Right click         |
| Lucy double    | Double click        |
| Lucy scroll    | Scroll down         |
| Lucy scroll up | Scroll up           |
| Lucy type      | Types "Hello World" |
| Lucy stop      | Exit program        |

---

### 🔒 Biometric Authentication

* Facial landmark-based user verification
* Auto-lock when unauthorized user detected
* Visual feedback (green = active, red = locked)

---

### 🛡️ Safety Features

* Emergency failsafe (move mouse to top-left corner)
* Multi-threaded architecture (video + audio)
* Robust error handling

---

## 📦 Installation

### Prerequisites

* Python 3.8+
* Webcam
* Microphone
* Windows / Linux / macOS

---

### Step 1: Clone Repository

```bash
git clone https://github.com/real-rohit/Lucy-eye-control.git
cd biometric-hands-free-tool
```

---

### Step 2: Install Dependencies

```bash
pip install opencv-python mediapipe pyautogui SpeechRecognition pyaudio numpy
```

#### Platform-specific setup

**Windows**

```bash
pip install pipwin
pipwin install pyaudio
```

**macOS**

```bash
brew install portaudio
pip install pyaudio
```

**Linux**

```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

---

### Step 3: (Optional) Enable Authentication

Add an image named `owner.jpg` in the project folder:

* Clear, front-facing face
* Good lighting
* Minimal obstructions

---

## 🎬 Quick Start

Run the application:

```bash
python biometric_tool_v3.py
```

### First Run

* Calibration starts automatically
* Follow 9-point gaze calibration
* Results are saved

### Later Runs

* Calibration loads automatically

---

## 🎯 Calibration Guide

### Tips for Best Accuracy

* Sit in a stable position
* Keep head still
* Look directly at each point
* Use consistent lighting

### Accuracy Ratings

| Score   | Quality   |
| ------- | --------- |
| 85–100% | Excellent |
| 70–84%  | Good      |
| 50–69%  | Fair      |
| <50%    | Poor      |

---

## 💻 Usage

### Cursor Control

* Move eyes → Move cursor
* Mirror-based tracking

### Blink Actions

* Left blink → Left click
* Right blink → Right click

### Voice Commands

* Say: **"Lucy + command"**
* Speak clearly and wait for readiness

### Keyboard Shortcuts

| Key              | Action         |
| ---------------- | -------------- |
| r                | Recalibrate    |
| q                | Quit           |
| Move to top-left | Emergency stop |

---

## ⚙️ Configuration

Edit parameters inside the script:

```python
BASE_SENSITIVITY = 2.5
SMOOTHING_FRAMES = 10
EAR_THRESHOLD = 0.21
BLINK_COOLDOWN = 0.5
FACE_MATCH_THRESHOLD = 0.15
```

---

## 🔧 Troubleshooting

### Webcam Not Working

* Check permissions
* Try different camera index

### Voice Not Recognized

* Reduce noise
* Speak clearly
* Use wake word

### Poor Calibration

* Improve lighting
* Recalibrate
* Keep head still

### Cursor Jitter

* Increase smoothing

```python
SMOOTHING_FRAMES = 15
```

---

## 🚀 Performance Tips

* Use a 720p+ webcam
* Maintain consistent lighting
* Sit 50–80 cm from camera
* Close background apps

---

## 🔬 Technical Overview

### Architecture

* Video Thread → Eye tracking & cursor control
* Audio Thread → Voice commands

### Core Techniques

* Facial landmark detection
* Iris tracking
* Eye Aspect Ratio (EAR)
* Calibration via transformation mapping

---

## 📁 Project Structure

```
biometric-hands-free-tool/
├── biometric_tool_v3.py
├── owner.jpg
├── eye_calibration.json
├── requirements.txt
└── README.md
```

---

## 📊 Performance Benchmarks

| Metric          | Good    | Excellent |
| --------------- | ------- | --------- |
| Accuracy        | 70–84%  | 85–100%   |
| Avg Error       | 50–80px | <50px     |
| Blink Detection | 90%+    | 95%+      |

