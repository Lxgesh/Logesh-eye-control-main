# 👁️ Advanced Biometric Hands-Free Accessibility Tool v3.0
An intelligent, voice-activated eye-tracking interface. Move your cursor with gaze, click with blinks, and command your PC using the Lucy assistant.


[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)](https://google.github.io/mediapipe/)

A sophisticated hands-free computer control system featuring **iris tracking**, **blink-to-click**, **voice commands**, and **personalized calibration**. Designed for accessibility and powered by computer vision and AI.

![Demo](demo.gif)
*Control your computer entirely hands-free using only your eyes and voice*


🌟 Features

### 🎯 Personalized Eye-Gaze Tracking
- **Full-screen calibration system** with 9-point grid
- **Iris tracking** using MediaPipe Face Mesh (landmarks 468-477)
- **Adaptive smoothing** with configurable moving average filters
- **Real-time accuracy scoring** and performance metrics
- **Persistent calibration** saves your profile between sessions

### 👁️ Blink-Based Controls
- **Left eye blink** → Left mouse click
- **Right eye blink** → Right mouse click
- **Eye Aspect Ratio (EAR)** algorithm for precise blink detection
- **Cooldown system** prevents accidental double-clicks

### 🎤 Voice Command System
- **Wake word activation**: All commands require "Lucy" prefix
- **Supported commands**:
  - "Lucy click" - Left click
  - "Lucy right" - Right click  
  - "Lucy double" - Double click
  - "Lucy scroll up/down" - Scroll
  - "Lucy type" - Type "Hello World"
  - "Lucy stop" - Exit program

### 🔒 Biometric Authentication
- **Facial landmark matching** for owner verification
- **Lightweight authentication** (no CMake/dlib required)
- **Visual feedback** with green/red border indicators
- **Auto-locking** when owner not detected

### 🛡️ Safety Features
- **PyAutoGUI failsafe**: Move mouse to top-left corner to emergency stop
- **Threaded architecture**: Video and audio processing run independently
- **Graceful error handling** throughout all modules

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Calibration Guide](#-calibration-guide)
- [Usage](#-usage)
- [Configuration](#%EF%B8%8F-configuration)
- [Troubleshooting](#-troubleshooting)
- [Performance Optimization](#-performance-optimization)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [License](#-license)


## 🚀 Installation

### Prerequisites
- **Python 3.8 or higher**
- **Webcam** (built-in or USB)
- **Microphone** for voice commands
- **Windows/Linux/macOS** (tested on Windows 10/11)

### Step 1: Clone Repository
```bash
git clone https://github.com/real-rohit/Lucy-eye-control.git
cd biometric-hands-free-tool
```

### Step 2: Install Dependencies
```bash
pip install opencv-python mediapipe pyautogui SpeechRecognition pyaudio numpy
```

#### Platform-Specific Notes

**Windows:**
```bash
# If pyaudio fails, install pipwin first
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

### Step 3: Optional - Owner Authentication
To enable biometric authentication, place a clear front-facing photo named `owner.jpg` in the project directory.

**Requirements for owner.jpg:**
- Clear, front-facing photo
- Good lighting
- Face clearly visible
- No obstructions (glasses OK)
- Recommended: Neutral expression

---

## 🎬 Quick Start

### First Run (Calibration Required)

```bash
python biometric_tool_v3.py
```

**On first launch:**
1. The system will automatically start calibration
2. Follow the on-screen instructions
3. Look at each red circle as it appears (9 points total)
4. Keep your head still, move only your eyes
5. Wait ~1 second per calibration point
6. Calibration is saved automatically

### Subsequent Runs

```bash
python biometric_tool_v3.py
```

Your calibration profile loads automatically! No need to recalibrate unless you move your setup.

---

## 🎯 Calibration Guide

### Why Calibrate?

Calibration creates a **personalized mathematical model** of YOUR eye movements. Everyone's eyes are different - calibration accounts for:
- Eye shape and size variations
- Distance from camera
- Monitor size and position
- Individual gaze patterns

### Calibration Process

#### Step 1: Preparation
- Sit in your normal working position
- Ensure good lighting (face your screen, not a window)
- Position your webcam at eye level if possible
- Close unnecessary applications

#### Step 2: 9-Point Calibration
A 3×3 grid of red circles will appear across your screen:

```
[1]  [2]  [3]
[4]  [5]  [6]
[7]  [8]  [9]
```

For each point:
1. **Look directly at the CENTER** of the red circle
2. **Keep your head still** (only move your eyes)
3. **Hold your gaze steady** for ~1 second
4. The circle will pulse - use this to focus
5. Progress bar shows completion

#### Step 3: Results

After calibration, you'll see:

```
CALIBRATION RESULTS
Points Collected: 9
Average Error: 45.2 pixels
Maximum Error: 78.3 pixels
Accuracy Score: 87.5%

✓ EXCELLENT calibration! Very accurate tracking expected.
```

**Accuracy Ratings:**
- **85-100%**: ✓ EXCELLENT - Ready to use!
- **70-84%**: ✓ GOOD - Usable, minor adjustments possible
- **50-69%**: ⚠ FAIR - Consider recalibrating
- **Below 50%**: ✗ POOR - Please recalibrate

#### Step 4: Recalibration

Press **'r'** anytime during use to recalibrate.

**Recalibrate when:**
- Accuracy drops noticeably
- You move your monitor or chair
- Lighting conditions change significantly
- You want to improve accuracy

---

## 💻 Usage

### Control Methods

#### 1. Eye-Gaze Cursor Control
- **Look around** to move the mouse cursor
- Movement is smooth and natural after calibration
- Mirror-mode enabled (look left = cursor goes left)

#### 2. Blink Controls
| Action | Command |
|--------|---------|
| Left Click | Blink **left eye only** |
| Right Click | Blink **right eye only** |

**Tips:**
- Blink deliberately (not a natural blink)
- One eye at a time
- 0.5s cooldown between blinks

#### 3. Voice Commands

All commands must start with **"Lucy"**:

| Command | Action |
|---------|--------|
| `Lucy click` | Left mouse click |
| `Lucy right` | Right mouse click |
| `Lucy double` | Double click |
| `Lucy scroll` | Scroll down |
| `Lucy scroll up` | Scroll up |
| `Lucy type` | Type "Hello World" (demo) |
| `Lucy stop` | Exit program |

**Voice Tips:**
- Speak clearly and at normal volume
- Wait for "Ready!" message before speaking
- Commands ignored if not authenticated

#### 4. Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `r` | Recalibrate eye tracking |
| `q` | Quit program |
| Move mouse to top-left corner | Emergency stop (failsafe) |

### Status Indicators

**On-Screen Display:**
- **Green Border**: Owner authenticated, system active
- **Red Border**: System locked, owner not detected
- **Calibration Status**: Shows if calibrated and accuracy %
- **EAR Values**: Real-time eye aspect ratio (for debugging blinks)

---

## ⚙️ Configuration

### Adjustable Parameters

Edit the configuration section at the top of the script:

```python
# ============ CONFIGURATION ============

# Eye tracking sensitivity
BASE_SENSITIVITY = 2.5  # Range: 1.5-4.0 (higher = more sensitive)

# Smoothing (higher = smoother but slower response)
SMOOTHING_FRAMES = 10  # Range: 5-15

# Screen padding (prevents cursor getting stuck at edges)
SCREEN_PADDING = 50  # Pixels

# Blink detection threshold
EAR_THRESHOLD = 0.21  # Range: 0.18-0.25 (lower = more sensitive)
BLINK_COOLDOWN = 0.5  # Seconds between blinks

# Authentication
AUTH_CHECK_INTERVAL = 30  # Frames between auth checks
FACE_MATCH_THRESHOLD = 0.15  # Range: 0.10-0.20 (lower = stricter)

# Wake word
WAKE_WORD = "lucy"  # Change to your preferred wake word

# Calibration
CALIBRATION_POINTS = 9  # 3x3 grid (don't change without adjusting code)
CALIBRATION_SAMPLES_PER_POINT = 30  # Frames per calibration point
```

### Common Adjustments

#### Cursor is Too Sensitive
```python
SMOOTHING_FRAMES = 15  # Increase smoothing
```

#### Cursor is Too Slow
```python
SMOOTHING_FRAMES = 5   # Decrease smoothing
BASE_SENSITIVITY = 3.5  # Increase sensitivity (if not calibrated)
```

#### Blinks Not Detected
```python
EAR_THRESHOLD = 0.19  # Lower threshold (more sensitive)
```

#### Accidental Blink Triggers
```python
EAR_THRESHOLD = 0.23  # Higher threshold (less sensitive)
BLINK_COOLDOWN = 0.7   # Longer cooldown
```

#### Authentication Too Strict
```python
FACE_MATCH_THRESHOLD = 0.18  # Higher = more lenient
```

---

## 🔧 Troubleshooting

### Issue: "Cannot open webcam"

**Solutions:**
1. Check if another application is using the webcam
2. Try changing camera index:
   ```python
   cap = cv2.VideoCapture(0)  # Try 0, 1, 2, etc.
   ```
3. Grant camera permissions to Python
4. Update webcam drivers

### Issue: "No module named 'pyaudio'"

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### Issue: Voice commands not recognized

**Solutions:**
1. Check microphone permissions
2. Speak louder and clearer
3. Reduce background noise
4. Always say wake word first: "Lucy [command]"
5. Wait for "[VOICE] Ready!" message

### Issue: Poor calibration accuracy (<70%)

**Try these:**
1. **Improve lighting**: Face your screen, avoid backlighting
2. **Adjust camera**: Position webcam at eye level
3. **Stay still**: Keep head stationary during calibration
4. **Focus carefully**: Look at the CENTER of each circle
5. **Clean webcam lens**
6. **Run calibration 2-3 times**: Keep the best result

### Issue: Cursor jumps or jitters

**Solutions:**
1. Increase smoothing:
   ```python
   SMOOTHING_FRAMES = 15
   ```
2. Recalibrate in current lighting conditions
3. Improve webcam framerate (better webcam or close other apps)
4. Ensure stable head position

### Issue: Blinks not detected or too sensitive

**Not detecting:**
```python
EAR_THRESHOLD = 0.19  # More sensitive
```

**Too sensitive:**
```python
EAR_THRESHOLD = 0.23  # Less sensitive
BLINK_COOLDOWN = 0.7   # Longer cooldown
```

Print EAR values to debug:
```python
print(f"Left EAR: {left_ear:.3f}, Right EAR: {right_ear:.3f}")
```

### Issue: Authentication keeps locking

**Solutions:**
1. Retake `owner.jpg` with better lighting
2. Increase threshold:
   ```python
   FACE_MATCH_THRESHOLD = 0.18
   ```
3. Ensure owner.jpg shows clear face without obstructions
4. Disable authentication (delete or rename owner.jpg)

---

## 🚀 Performance Optimization

### Best Practices for Accuracy

#### 1. Environmental Setup
- ✅ Consistent lighting (avoid direct sunlight)
- ✅ Stable seating position
- ✅ Camera at eye level
- ✅ Monitor at comfortable viewing distance
- ✅ Minimal background noise for voice commands

#### 2. Calibration Tips
- ✅ Calibrate in the lighting you'll use
- ✅ Sit in your normal working position
- ✅ Keep head still during calibration
- ✅ Take your time on each point
- ✅ Recalibrate if accuracy < 80%

#### 3. Usage Techniques
- ✅ Make deliberate eye movements (not quick darts)
- ✅ Blink one eye at a time for clicks
- ✅ Speak clearly for voice commands
- ✅ Keep face visible to camera

#### 4. System Optimization
- ✅ Close unnecessary applications
- ✅ Use a decent webcam (720p+ recommended)
- ✅ Ensure Python has camera/microphone permissions
- ✅ Run on AC power (not battery saver mode)

### Performance Tuning

For **high-performance** systems:
```python
SMOOTHING_FRAMES = 5
CALIBRATION_SAMPLES_PER_POINT = 50
```

For **low-end** systems:
```python
SMOOTHING_FRAMES = 15
cap.set(cv2.CAP_PROP_FPS, 15)  # Limit framerate
```

---

## 🔬 Technical Details

### Architecture

```
┌─────────────────────────────────────────────┐
│           Main Application Thread           │
├─────────────────────────────────────────────┤
│  ┌───────────────┐    ┌─────────────────┐  │
│  │ Video Thread  │    │  Audio Thread   │  │
│  │  (High FPS)   │    │   (Daemon)      │  │
│  ├───────────────┤    ├─────────────────┤  │
│  │ • Webcam      │    │ • Microphone    │  │
│  │ • Face Mesh   │    │ • Speech Recog  │  │
│  │ • Iris Track  │    │ • Wake Word     │  │
│  │ • Auth Check  │    │ • Commands      │  │
│  │ • Blink Detect│    │                 │  │
│  │ • Cursor Move │    │                 │  │
│  └───────────────┘    └─────────────────┘  │
└─────────────────────────────────────────────┘
```

### Key Technologies

#### 1. MediaPipe Face Mesh
- **468 facial landmarks** in 3D space
- **Iris landmarks**: 468-477 (5 points per eye)
- **Refined landmarks** mode for eye tracking
- **Real-time performance**: 30+ FPS

#### 2. Eye Aspect Ratio (EAR)
```
       vertical₁ + vertical₂
EAR = ─────────────────────
           2 × horizontal
```
- Detects eye openness
- Threshold-based blink detection
- Individual eye monitoring

#### 3. Calibration Algorithm
- **9-point grid calibration**
- **Least squares regression** for transformation matrix
- **Perspective transform** for non-linear mapping
- **Error metrics**: Average and maximum pixel deviation

#### 4. Facial Authentication
- **Feature extraction**: 78 pairwise distances between 13 key landmarks
- **Normalization**: Scale and position invariant
- **Euclidean distance matching** with configurable threshold

### Data Flow

```
Webcam → MediaPipe → Iris Position → Calibration Transform
                                            ↓
                                     Screen Coordinates
                                            ↓
                                    Moving Average Filter
                                            ↓
                                      PyAutoGUI.moveTo()
```

### File Structure

```
biometric-hands-free-tool/
├── biometric_tool_v3.py      # Main application
├── owner.jpg                  # (Optional) Owner photo for auth
├── eye_calibration.json       # Generated after calibration
├── README.md                  # This file
├── LICENSE                    # MIT License
├── requirements.txt           # Python dependencies
└── docs/                      # Additional documentation
    ├── CALIBRATION.md
    ├── TROUBLESHOOTING.md
    └── API.md
```

### Calibration File Format

```json
{
  "screen_points": [[100, 100], [960, 100], ...],
  "iris_points": [[0.45, 0.52], [0.62, 0.51], ...],
  "transform_matrix": [[...], [...]],
  "accuracy_score": 87.5,
  "sensitivity_x": 2.5,
  "sensitivity_y": 2.5,
  "offset_x": 0,
  "offset_y": 0
}
```

---

## 📊 Accuracy Benchmarks

### Typical Performance Metrics

| Metric | Good | Excellent |
|--------|------|-----------|
| Calibration Accuracy | 70-84% | 85-100% |
| Average Error | 50-80px | <50px |
| Maximum Error | 100-150px | <100px |
| Cursor Smoothness | Minimal jitter | No jitter |
| Blink Detection | 90%+ | 95%+ |

### Factors Affecting Accuracy

**Positive factors:**
- ✅ Good lighting (diffused, not direct)
- ✅ High-quality webcam (720p+)
- ✅ Close distance to camera (50-80cm)
- ✅ Proper calibration
- ✅ Stable head position

**Negative factors:**
- ❌ Poor lighting or backlighting
- ❌ Low-quality webcam
- ❌ Excessive head movement
- ❌ Wearing thick-framed glasses
- ❌ Camera positioned off-center

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Ideas

- [ ] Additional voice commands
- [ ] Multi-monitor support
- [ ] Gesture recognition
- [ ] Mouse acceleration curves
- [ ] Configuration GUI
- [ ] Improved authentication algorithms
- [ ] Platform-specific optimizations
- [ ] Accessibility profiles (ALS, cerebral palsy, etc.)

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex algorithms
- Include type hints where possible

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 Acknowledgments

- **MediaPipe** by Google for facial landmark detection
- **OpenCV** for computer vision capabilities
- **PyAutoGUI** for system automation
- **SpeechRecognition** for voice command processing
- The accessibility community for inspiration and feedback

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/real-rohit/Lucy-eye-control/issues)
- **Discussions**: [GitHub Discussions](https://github.com/real-rohit/Lucy-eye-control/discussions)
- **Email**: realrohitgoswami@gmail.com

---

## 🗺️ Roadmap

### v3.1 (Planned)
- [ ] Multi-monitor support
- [ ] Configurable voice commands
- [ ] Improved blink sensitivity auto-tuning
- [ ] Export/import calibration profiles

### v4.0 (Future)
- [ ] Head gesture recognition (nod, shake)
- [ ] Facial expression commands (smile, frown)
- [ ] Machine learning-based gaze prediction
- [ ] Mobile device support (Android/iOS)

---

## 📈 Changelog

### v3.0 (Current)
- ✨ Added full-screen 9-point calibration system
- ✨ Personalized eye-gaze transformation
- ✨ Real-time accuracy scoring
- ✨ Persistent calibration profiles
- 🐛 Fixed X-axis mirroring issue
- 🐛 Improved blink detection reliability
- 📝 Comprehensive documentation

### v2.1
- ✨ Lightweight facial authentication (removed dlib dependency)
- ✨ MediaPipe-based landmark matching
- 🐛 Fixed CMake installation issues

### v2.0
- ✨ Iris tracking (replaced nose tracking)
- ✨ Blink-to-click controls
- ✨ "Lucy" wake word system
- ✨ Owner authentication
- ✨ Green/red border visual feedback

### v1.0
- ✨ Initial release
- ✨ Basic head tracking
- ✨ Voice commands
- ✨ Simple mouse control

---

## ⭐ Star History

If this project helped you, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=real-rohit/Lucy-eye-control&type=Date)](https://star-history.com/#real-rohit/Lucy-eye-control&Date)

---

<div align="center">

**Made with ❤️ for the accessibility community**

[⬆ Back to Top](#-advanced-biometric-hands-free-accessibility-tool-v30)

</div>
