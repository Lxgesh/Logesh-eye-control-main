"""
Advanced Biometric Hands-Free Accessibility Tool v3.0
NEW: Full-Screen Calibration System for Maximum Accuracy

Requirements:
pip install opencv-python mediapipe pyautogui SpeechRecognition pyaudio numpy

CALIBRATION PROCESS:
1. At startup, you'll see 9 calibration points (3x3 grid)
2. Look at each RED circle when it appears
3. The system learns YOUR specific eye-gaze patterns
4. After calibration, cursor tracking will be personalized to YOUR eyes

SETUP:
1. Place "owner.jpg" in the same directory (optional, for authentication)
2. Run the script
3. Complete the calibration by looking at each point
4. Use the system with your personalized settings!

Usage:
- Look around to move the cursor (iris tracking)
- Blink LEFT eye for left click
- Blink RIGHT eye for right click
- Say "Lucy [command]" for voice commands
- Press 'r' to recalibrate anytime
"""

import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import threading
import numpy as np
from collections import deque
import time
import os
import json

# ============ CONFIGURATION ============

# Initial sensitivity (will be adjusted by calibration)
BASE_SENSITIVITY = 2.5

# Smoothing
SMOOTHING_FRAMES = 10

# Screen boundaries
SCREEN_PADDING = 50

# Eye Aspect Ratio (EAR) threshold for blink detection
EAR_THRESHOLD = 0.21
BLINK_COOLDOWN = 0.5

# Authentication settings
AUTH_CHECK_INTERVAL = 30
FACE_MATCH_THRESHOLD = 0.2

# Wake word
WAKE_WORD = "lucy"

# Voice recognition settings
VOICE_TIMEOUT = 3
VOICE_PHRASE_TIME = 3

# Calibration settings
CALIBRATION_POINTS = 9  # 3x3 grid
CALIBRATION_SAMPLES_PER_POINT = 30  # Frames to collect per point
CALIBRATION_FILE = "eye_calibration.json"

# =======================================

# Global variables
running = True
owner_authenticated = False
calibration_mode = False
calibrated = False
screen_width, screen_height = pyautogui.size()
owner_face_landmarks = None

# Calibration data
calibration_data = {
    'screen_points': [],
    'iris_points': [],
    'transform_matrix': None,
    'sensitivity_x': BASE_SENSITIVITY,
    'sensitivity_y': BASE_SENSITIVITY,
    'offset_x': 0,
    'offset_y': 0,
    'accuracy_score': 0
}

# Blink timing
last_left_blink_time = 0
last_right_blink_time = 0

# PyAutoGUI settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Smoothing buffers
x_buffer = deque(maxlen=SMOOTHING_FRAMES)
y_buffer = deque(maxlen=SMOOTHING_FRAMES)


def save_calibration():
    """Save calibration data to file"""
    try:
        with open(CALIBRATION_FILE, 'w') as f:
            # Convert numpy arrays to lists for JSON serialization
            save_data = calibration_data.copy()
            if save_data['transform_matrix'] is not None:
                save_data['transform_matrix'] = save_data['transform_matrix'].tolist()
            json.dump(save_data, f, indent=2)
        print(f"✓ Calibration saved to {CALIBRATION_FILE}")
        return True
    except Exception as e:
        print(f"Error saving calibration: {e}")
        return False


def load_calibration():
    """Load calibration data from file"""
    global calibrated, calibration_data
    
    if not os.path.exists(CALIBRATION_FILE):
        return False
    
    try:
        with open(CALIBRATION_FILE, 'r') as f:
            loaded_data = json.load(f)
            
        # Convert lists back to numpy arrays
        if loaded_data['transform_matrix'] is not None:
            loaded_data['transform_matrix'] = np.array(loaded_data['transform_matrix'])
        
        calibration_data.update(loaded_data)
        calibrated = True
        print(f"✓ Calibration loaded from {CALIBRATION_FILE}")
        print(f"  Accuracy Score: {calibration_data['accuracy_score']:.1f}%")
        return True
    except Exception as e:
        print(f"Error loading calibration: {e}")
        return False


def generate_calibration_points():
    """Generate 3x3 grid of calibration points across the screen"""
    points = []
    margin = 100  # Pixels from edge
    
    cols = 3
    rows = 3
    
    for row in range(rows):
        for col in range(cols):
            x = margin + (screen_width - 2 * margin) * col / (cols - 1)
            y = margin + (screen_height - 2 * margin) * row / (rows - 1)
            points.append((int(x), int(y)))
    
    return points


def get_iris_position(face_landmarks):
    """Get normalized iris position (averaged from both eyes)"""
    left_iris = face_landmarks.landmark[469]
    right_iris = face_landmarks.landmark[474]
    
    avg_x = (left_iris.x + right_iris.x) / 2
    avg_y = (left_iris.y + right_iris.y) / 2
    
    return avg_x, avg_y


def perform_calibration():
    """
    Full-screen calibration routine
    Returns: True if successful, False otherwise
    """
    global calibration_data, calibrated
    
    print("\n" + "=" * 60)
    print("CALIBRATION MODE")
    print("=" * 60)
    print("Instructions:")
    print("1. Look at each RED circle when it appears")
    print("2. Keep your head still, move only your eyes")
    print("3. Try to look at the CENTER of each circle")
    print("4. Hold your gaze steady for 1 second per point")
    print("=" * 60)
    print("\nStarting calibration in 3 seconds...")
    time.sleep(3)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam!")
        return False
    
    # Generate calibration points
    screen_points = generate_calibration_points()
    collected_iris_points = []
    collected_screen_points = []
    
    for point_idx, (target_x, target_y) in enumerate(screen_points):
        print(f"\nCalibration Point {point_idx + 1}/{len(screen_points)}")
        print(f"Look at: ({target_x}, {target_y})")
        
        samples = []
        frame_count = 0
        
        while frame_count < CALIBRATION_SAMPLES_PER_POINT:
            success, frame = cap.read()
            if not success:
                continue
            
            frame = cv2.flip(frame, 1)
            
            # Create a full-screen calibration display
            calib_display = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
            
            # Draw all calibration points (gray)
            for px, py in screen_points:
                cv2.circle(calib_display, (px, py), 30, (100, 100, 100), 2)
            
            # Draw current target point (red, pulsing)
            pulse = int(20 + 15 * np.sin(frame_count * 0.3))
            cv2.circle(calib_display, (target_x, target_y), pulse, (0, 0, 255), -1)
            cv2.circle(calib_display, (target_x, target_y), pulse + 10, (0, 0, 255), 3)
            
            # Add crosshair
            cv2.line(calib_display, (target_x - 20, target_y), (target_x + 20, target_y), (255, 255, 255), 2)
            cv2.line(calib_display, (target_x, target_y - 20), (target_x, target_y + 20), (255, 255, 255), 2)
            
            # Progress bar
            progress = frame_count / CALIBRATION_SAMPLES_PER_POINT
            bar_width = 400
            bar_height = 30
            bar_x = (screen_width - bar_width) // 2
            bar_y = screen_height - 100
            
            cv2.rectangle(calib_display, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), 2)
            cv2.rectangle(calib_display, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)
            
            # Instructions
            cv2.putText(calib_display, f"Point {point_idx + 1} of {len(screen_points)}", 
                       (bar_x, bar_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(calib_display, "Look at the RED circle", 
                       (bar_x, bar_y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
            
            # Process face mesh
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                iris_x, iris_y = get_iris_position(face_landmarks)
                samples.append((iris_x, iris_y))
                frame_count += 1
            
            cv2.imshow('Calibration', calib_display)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return False
        
        # Average the samples for this point
        if samples:
            avg_iris_x = np.mean([s[0] for s in samples])
            avg_iris_y = np.mean([s[1] for s in samples])
            collected_iris_points.append([avg_iris_x, avg_iris_y])
            collected_screen_points.append([target_x, target_y])
            print(f"✓ Collected: iris=({avg_iris_x:.3f}, {avg_iris_y:.3f})")
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Calculate transformation matrix
    if len(collected_iris_points) >= 4:
        iris_points = np.array(collected_iris_points, dtype=np.float32)
        screen_pts = np.array(collected_screen_points, dtype=np.float32)
        
        # Calculate perspective transform
        # Add homogeneous coordinate
        iris_points_homo = np.column_stack([iris_points, np.ones(len(iris_points))])
        
        # Solve for transformation matrix using least squares
        transform_x, _, _, _ = np.linalg.lstsq(iris_points_homo, screen_pts[:, 0], rcond=None)
        transform_y, _, _, _ = np.linalg.lstsq(iris_points_homo, screen_pts[:, 1], rcond=None)
        
        transform_matrix = np.array([transform_x, transform_y])
        
        # Test accuracy
        predicted_points = []
        for iris_pt in iris_points:
            pred_x = transform_x[0] * iris_pt[0] + transform_x[1] * iris_pt[1] + transform_x[2]
            pred_y = transform_y[0] * iris_pt[0] + transform_y[1] * iris_pt[1] + transform_y[2]
            predicted_points.append([pred_x, pred_y])
        
        predicted_points = np.array(predicted_points)
        errors = np.linalg.norm(predicted_points - screen_pts, axis=1)
        avg_error = np.mean(errors)
        max_error = np.max(errors)
        
        # Calculate accuracy score (inverse of normalized error)
        accuracy_score = max(0, 100 * (1 - avg_error / (screen_width / 2)))
        
        calibration_data['screen_points'] = collected_screen_points
        calibration_data['iris_points'] = collected_iris_points
        calibration_data['transform_matrix'] = transform_matrix
        calibration_data['accuracy_score'] = accuracy_score
        
        calibrated = True
        
        print("\n" + "=" * 60)
        print("CALIBRATION RESULTS")
        print("=" * 60)
        print(f"Points Collected: {len(collected_iris_points)}")
        print(f"Average Error: {avg_error:.1f} pixels")
        print(f"Maximum Error: {max_error:.1f} pixels")
        print(f"Accuracy Score: {accuracy_score:.1f}%")
        print("=" * 60)
        
        # Evaluate calibration quality
        if accuracy_score >= 85:
            print("✓ EXCELLENT calibration! Very accurate tracking expected.")
        elif accuracy_score >= 70:
            print("✓ GOOD calibration! Accurate tracking expected.")
        elif accuracy_score >= 50:
            print("⚠ FAIR calibration. Consider recalibrating for better accuracy.")
        else:
            print("✗ POOR calibration. Please recalibrate.")
        
        save_calibration()
        return True
    else:
        print("ERROR: Not enough calibration points collected!")
        return False


def apply_calibration(iris_x, iris_y):
    """Apply calibration transformation to iris position"""
    if not calibrated or calibration_data['transform_matrix'] is None:
        # Fallback to basic mapping
        screen_x = screen_width - int(iris_x * BASE_SENSITIVITY * screen_width)
        screen_y = int(iris_y * BASE_SENSITIVITY * screen_height)
    else:
        # Use calibrated transformation
        transform = calibration_data['transform_matrix']
        screen_x = transform[0][0] * iris_x + transform[0][1] * iris_y + transform[0][2]
        screen_y = transform[1][0] * iris_x + transform[1][1] * iris_y + transform[1][2]
    
    # Clamp to screen boundaries
    screen_x = max(SCREEN_PADDING, min(screen_width - SCREEN_PADDING, int(screen_x)))
    screen_y = max(SCREEN_PADDING, min(screen_height - SCREEN_PADDING, int(screen_y)))
    
    return screen_x, screen_y


def extract_face_features(face_landmarks):
    """Extract key facial landmarks for authentication"""
    key_indices = [1, 33, 133, 362, 263, 61, 291, 199, 10, 152, 70, 300]
    
    points = []
    for idx in key_indices:
        landmark = face_landmarks.landmark[idx]
        points.append([landmark.x, landmark.y, landmark.z])
    
    points = np.array(points)
    
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = np.linalg.norm(points[i] - points[j])
            distances.append(dist)
    
    return np.array(distances)


def load_owner_face():
    """Load owner face from owner.jpg"""
    global owner_face_landmarks
    
    owner_image_path = "owner.jpg"
    
    if not os.path.exists(owner_image_path):
        print("⚠ owner.jpg not found - running without authentication")
        return False
    
    try:
        owner_image = cv2.imread(owner_image_path)
        if owner_image is None:
            return False
        
        rgb_image = cv2.cvtColor(owner_image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)
        
        if not results.multi_face_landmarks:
            print("ERROR: No face in owner.jpg")
            return False
        
        face_landmarks = results.multi_face_landmarks[0]
        owner_face_landmarks = extract_face_features(face_landmarks)
        
        print("✓ Owner face loaded")
        return True
    except Exception as e:
        print(f"Error loading owner.jpg: {e}")
        return False


def authenticate_face(face_landmarks):
    """Authenticate face against owner"""
    global owner_face_landmarks
    
    if owner_face_landmarks is None:
        return False
    
    try:
        current_features = extract_face_features(face_landmarks)
        norm_owner = owner_face_landmarks / np.linalg.norm(owner_face_landmarks)
        norm_current = current_features / np.linalg.norm(current_features)
        distance = np.linalg.norm(norm_owner - norm_current)
        
        return distance < FACE_MATCH_THRESHOLD
    except Exception as e:
        return False


def calculate_ear(eye_landmarks):
    """Calculate Eye Aspect Ratio"""
    vertical_1 = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
    vertical_2 = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
    horizontal = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
    
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear


def detect_blink(left_ear, right_ear):
    """Detect individual eye blinks"""
    global last_left_blink_time, last_right_blink_time
    
    current_time = time.time()
    
    if left_ear < EAR_THRESHOLD and right_ear > EAR_THRESHOLD:
        if current_time - last_left_blink_time > BLINK_COOLDOWN:
            last_left_blink_time = current_time
            return "left"
    
    if right_ear < EAR_THRESHOLD and left_ear > EAR_THRESHOLD:
        if current_time - last_right_blink_time > BLINK_COOLDOWN:
            last_right_blink_time = current_time
            return "right"
    
    return None


def smooth_coordinates(x, y):
    """Apply moving average smoothing"""
    x_buffer.append(x)
    y_buffer.append(y)
    
    smooth_x = int(np.mean(x_buffer))
    smooth_y = int(np.mean(y_buffer))
    
    return smooth_x, smooth_y


def get_eye_landmarks(face_landmarks, frame_width, frame_height, eye_type="left"):
    """Extract eye landmarks for EAR calculation"""
    if eye_type == "left":
        indices = [33, 160, 158, 133, 153, 144]
    else:
        indices = [362, 385, 387, 263, 373, 380]
    
    landmarks = []
    for idx in indices:
        landmark = face_landmarks.landmark[idx]
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        landmarks.append((x, y))
    
    return landmarks


def draw_border(frame, color, thickness=10):
    """Draw colored border"""
    height, width = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (width, height), color, thickness)


def video_tracking_thread():
    """Main video tracking thread"""
    global running, owner_authenticated, calibration_mode
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("ERROR: Cannot open webcam!")
        running = False
        return
    
    print("\n[VIDEO] Tracking started")
    
    frame_count = 0
    
    while running:
        try:
            success, frame = cap.read()
            if not success:
                break
            
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)
            
            # Authentication check
            if results.multi_face_landmarks and frame_count % AUTH_CHECK_INTERVAL == 0:
                face_landmarks = results.multi_face_landmarks[0]
                owner_authenticated = authenticate_face(face_landmarks)
            
            frame_count += 1
            
            # Draw border
            if owner_authenticated:
                draw_border(frame, (0, 255, 0), 15)
            else:
                draw_border(frame, (0, 0, 255), 15)
            
            if results.multi_face_landmarks and owner_authenticated:
                face_landmarks = results.multi_face_landmarks[0]
                
                # Get iris position
                iris_x, iris_y = get_iris_position(face_landmarks)
                
                # Apply calibration
                screen_x, screen_y = apply_calibration(iris_x, iris_y)
                
                # Smooth
                smooth_x, smooth_y = smooth_coordinates(screen_x, screen_y)
                
                # Move cursor
                pyautogui.moveTo(smooth_x, smooth_y)
                
                # Blink detection
                left_eye = get_eye_landmarks(face_landmarks, frame_width, frame_height, "left")
                right_eye = get_eye_landmarks(face_landmarks, frame_width, frame_height, "right")
                
                left_ear = calculate_ear(left_eye)
                right_ear = calculate_ear(right_eye)
                
                blink = detect_blink(left_ear, right_ear)
                
                if blink == "left":
                    print("👁️ Left Blink → Click")
                    pyautogui.click()
                elif blink == "right":
                    print("👁️ Right Blink → Right Click")
                    pyautogui.click(button='right')
                
                # Visual feedback
                left_iris = face_landmarks.landmark[469]
                right_iris = face_landmarks.landmark[474]
                
                cv2.circle(frame, (int(left_iris.x * frame_width), int(left_iris.y * frame_height)), 5, (255, 0, 0), -1)
                cv2.circle(frame, (int(right_iris.x * frame_width), int(right_iris.y * frame_height)), 5, (255, 0, 0), -1)
            
            # Display info
            status = "AUTHENTICATED" if owner_authenticated else "LOCKED"
            status_color = (0, 255, 0) if owner_authenticated else (0, 0, 255)
            calib_status = "CALIBRATED" if calibrated else "NOT CALIBRATED"
            calib_color = (0, 255, 0) if calibrated else (255, 0, 0)
            
            cv2.putText(frame, f"Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            cv2.putText(frame, f"Calibration: {calib_status}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, calib_color, 2)
            
            if calibrated:
                cv2.putText(frame, f"Accuracy: {calibration_data['accuracy_score']:.0f}%", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.putText(frame, "Press 'r' to recalibrate", (10, frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('Biometric Accessibility Tool v3.0', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                running = False
            elif key == ord('r'):
                print("\n[RECALIBRATION] Starting...")
                perform_calibration()
                
        except pyautogui.FailSafeException:
            print("\n[FAILSAFE] Stopping...")
            running = False
            break
        except Exception as e:
            print(f"Video error: {e}")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("[VIDEO] Stopped")


def voice_command_thread():
    """Voice recognition thread"""
    global running, owner_authenticated
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("\n[VOICE] Calibrating...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    
    print(f'[VOICE] Ready! Say "{WAKE_WORD.upper()} [command]"')
    
    while running:
        try:
            with microphone as source:
                audio = recognizer.listen(source, timeout=VOICE_TIMEOUT, phrase_time_limit=VOICE_PHRASE_TIME)
            
            command = recognizer.recognize_google(audio).lower()
            
            if not command.startswith(WAKE_WORD):
                continue
            
            command = command[len(WAKE_WORD):].strip()
            print(f'[VOICE] "{WAKE_WORD} {command}"')
            
            if not owner_authenticated:
                print("[VOICE] Locked")
                continue
            
            if "click" in command and "double" not in command and "right" not in command:
                pyautogui.click()
            elif "right" in command:
                pyautogui.rightClick()
            elif "double" in command:
                pyautogui.doubleClick()
            elif "scroll" in command:
                pyautogui.scroll(300 if "up" in command else -300)
            elif "type" in command:
                pyautogui.typewrite("Hello World", interval=0.05)
            elif "stop" in command:
                running = False
                break
            
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            pass
        except Exception as e:
            if running:
                print(f"[VOICE] Error: {e}")
            time.sleep(0.5)
    
    print("[VOICE] Stopped")


def main():
    """Main function"""
    global running, owner_authenticated
    
    print("=" * 60)
    print("Advanced Biometric Accessibility Tool v3.0")
    print("With Full-Screen Calibration System")
    print("=" * 60)
    
    # Load owner face
    has_owner = load_owner_face()
    if not has_owner:
        owner_authenticated = True  # Skip auth if no owner.jpg
    
    # Try to load existing calibration
    if not load_calibration():
        print("\n⚠ No calibration found. Starting calibration process...")
        time.sleep(2)
        if not perform_calibration():
            print("Calibration failed. Using default settings.")
    
    print("\n[CONTROLS]")
    print("- Look around: Move cursor")
    print("- Left eye blink: Left click")
    print("- Right eye blink: Right click")
    print("- Say 'Lucy [command]': Voice control")
    print("- Press 'r': Recalibrate")
    print("- Press 'q': Quit")
    print()
    
    # Start threads
    video_thread = threading.Thread(target=video_tracking_thread, daemon=False)
    audio_thread = threading.Thread(target=voice_command_thread, daemon=True)
    
    video_thread.start()
    time.sleep(1)
    audio_thread.start()
    
    try:
        video_thread.join()
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Stopping...")
        running = False
    
    time.sleep(0.5)
    print("\n" + "=" * 60)
    print("Program terminated")
    print("=" * 60)


if __name__ == "__main__":
    main()