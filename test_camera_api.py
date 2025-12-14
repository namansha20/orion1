#!/usr/bin/env python3
"""
AADES Real-Time Camera Detection System
Performs detection using YOLO AI model with stabilized tracking
"""

import cv2
import numpy as np
import os
import sys
import platform
from collections import deque
from ultralytics import YOLO

# --- CONFIGURATION ---

# 1. AI MODEL
# Default path - can be overridden via environment variable YOLO_MODEL_PATH
# Use 'best.pt' as a generic default that users should replace
MODEL_PATH = os.environ.get('YOLO_MODEL_PATH', 'best.pt')

# 2. SMOOTHING SETTINGS (TUNED FOR STABILITY)
# Lower = Smoother but slower. Higher = Faster but jittery.
# 0.15 is very smooth (like a cinematic camera).
SMOOTH_FACTOR = 0.15 

# 3. DEADZONE (Anti-Vibration)
# If the new position is within 3 pixels of the old one, DON'T MOVE.
DEADZONE_PIXELS = 3 

# 4. PHYSICS CONSTANTS
BUFFER_SIZE = 32         
PREDICTION_FRAMES = 15   
COLLISION_ZONE = 80      
GROWTH_THRESHOLD = 0.5   
MOVEMENT_THRESHOLD = 2
VELOCITY_CALC_FRAMES = 5  # Number of frames to use for velocity calculation

# 5. ANTI-FLICKER
MAX_COAST_FRAMES = 10     
CONFIDENCE_MIN = 0.25    
RATIO_MIN = 0.60         
RATIO_MAX = 1.60         

# 6. CAMERA
EXPOSURE_VAL = -5.0      

# --- INITIALIZATION ---
print(f"🔄 SYSTEM BOOT: Loading AI from {MODEL_PATH}...")
try:
    model = YOLO(MODEL_PATH)
    print("✅ AI BRAIN ONLINE.")
except FileNotFoundError as e:
    print(f"❌ CRITICAL ERROR: Model file not found at {MODEL_PATH}")
    print(f"   Please set YOLO_MODEL_PATH environment variable or update MODEL_PATH")
    sys.exit(1)
except Exception as e:
    print(f"❌ CRITICAL ERROR: Could not load model.\n{e}")
    sys.exit(1)

def calculate_dynamics(pos_history, radius_history):
    # Need at least 2*VELOCITY_CALC_FRAMES to avoid overlap in growth rate calculation
    min_frames = VELOCITY_CALC_FRAMES * 2
    if len(pos_history) < VELOCITY_CALC_FRAMES or len(radius_history) < min_frames:
        return (0, 0), 0
    
    # Calculate velocity using more frames for stability
    # Note: deque uses appendleft, so index 0 is newest, higher indices are older
    # Velocity = (newer_pos - older_pos), i.e., pos_history[i-1] - pos_history[i]
    dx = int(np.mean([pos_history[i-1][0] - pos_history[i][0] for i in range(1, VELOCITY_CALC_FRAMES)]))
    dy = int(np.mean([pos_history[i-1][1] - pos_history[i][1] for i in range(1, VELOCITY_CALC_FRAMES)]))

    # Calculate growth rate: recent (newest at index 0) vs old (oldest at end)
    # Ensure no overlap by requiring 2*VELOCITY_CALC_FRAMES
    r_now = np.mean(list(radius_history)[:VELOCITY_CALC_FRAMES])  # Most recent frames (index 0 to VELOCITY_CALC_FRAMES-1)
    r_old = np.mean(list(radius_history)[-VELOCITY_CALC_FRAMES:])  # Oldest frames (last VELOCITY_CALC_FRAMES)
    growth_rate = r_now - r_old 
    
    return (dx, dy), growth_rate

def get_direction_label(dx, dy):
    h_dir = ""
    v_dir = ""
    if dx > MOVEMENT_THRESHOLD: h_dir = "RIGHT"
    elif dx < -MOVEMENT_THRESHOLD: h_dir = "LEFT"
    if dy > MOVEMENT_THRESHOLD: v_dir = "DOWN"
    elif dy < -MOVEMENT_THRESHOLD: v_dir = "UP"
    if h_dir == "" and v_dir == "": return "STATIONARY"
    return f"{h_dir} {v_dir}".strip()

def main():
    # Try to open camera - use CAP_DSHOW on Windows, default on other platforms
    camera_index = int(os.environ.get('CAMERA_INDEX', 0))
    try:
        if platform.system() == 'Windows':
            cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(camera_index)
    except Exception:
        cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"❌ ERROR: Could not open camera at index {camera_index}")
        sys.exit(1)
    
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) 
    cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE_VAL) 
    
    pos_pts = deque(maxlen=BUFFER_SIZE)
    rad_pts = deque(maxlen=BUFFER_SIZE)

    # VARIABLES FOR SMOOTHING
    smooth_x, smooth_y, smooth_r = None, None, None
    coast_count = 0
    last_dx, last_dy = 0, 0

    print("🚀 AADES SENSOR ACTIVE. STABILIZER ENGAGED.")

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        center_x, center_y = w // 2, h // 2
        
        results = model(frame, stream=True, verbose=False, conf=CONFIDENCE_MIN)
        
        target_found = False
        
        # --- 1. AI DETECTION & STABILIZATION ---
        for r in results:
            boxes = r.boxes
            for box in boxes:
                confidence = float(box.conf[0])
                if confidence < CONFIDENCE_MIN: continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                obj_w = x2 - x1
                obj_h = y2 - y1
                aspect_ratio = obj_w / float(obj_h)

                if aspect_ratio < RATIO_MIN or aspect_ratio > RATIO_MAX:
                    continue

                # Raw measurements
                raw_x = x1 + (obj_w // 2)
                raw_y = y1 + (obj_h // 2)
                raw_r = max(obj_w, obj_h) // 2

                # === HEAVY SMOOTHING LOGIC ===
                if smooth_x is None:
                    smooth_x, smooth_y, smooth_r = float(raw_x), float(raw_y), float(raw_r)
                else:
                    # 1. Calculate how far it moved
                    dist_moved = np.linalg.norm(np.array((raw_x, raw_y)) - np.array((smooth_x, smooth_y)))
                    
                    # 2. Deadzone Check: If it barely moved, ignore the jitter
                    if dist_moved > DEADZONE_PIXELS:
                        # 3. Heavy Smoothing (Exponential Moving Average)
                        smooth_x = (smooth_x * (1 - SMOOTH_FACTOR)) + (raw_x * SMOOTH_FACTOR)
                        smooth_y = (smooth_y * (1 - SMOOTH_FACTOR)) + (raw_y * SMOOTH_FACTOR)
                        smooth_r = (smooth_r * (1 - SMOOTH_FACTOR)) + (raw_r * SMOOTH_FACTOR)
                    # Else: Keep smooth_x exactly the same (Vibration Killer)

                target_found = True
                coast_count = 0 
                
                # Convert to integer for drawing
                x, y, radius = int(smooth_x), int(smooth_y), int(smooth_r)
                
                # Update History
                pos_pts.appendleft((x, y))
                rad_pts.appendleft(radius)
                
                # Calculate Dynamics
                (dx, dy), growth_rate = calculate_dynamics(pos_pts, rad_pts)
                last_dx, last_dy = dx, dy
                
                # Draw Box (Green) - Uses smoothed coordinates
                cv2.rectangle(frame, (x-radius, y-radius), (x+radius, y+radius), (0, 255, 0), 2)

        # --- 2. COASTING (Momentum) ---
        if not target_found and coast_count < MAX_COAST_FRAMES and smooth_x is not None:
            coast_count += 1
            
            # Continue moving using last known velocity
            smooth_x += last_dx
            smooth_y += last_dy
            
            x, y, radius = int(smooth_x), int(smooth_y), int(smooth_r)
            
            pos_pts.appendleft((x, y))
            rad_pts.appendleft(radius)
            
            # Visualize "Ghost" (Gray)
            cv2.rectangle(frame, (x-radius, y-radius), (x+radius, y+radius), (100, 100, 100), 1)
            cv2.putText(frame, "PREDICTING...", (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
            
            target_found = True 
            dx, dy = last_dx, last_dy
            growth_rate = 0 

        # --- 3. LOGIC & HUD ---
        if target_found:
            direction_label = get_direction_label(dx, dy)
            
            pred_x = int(x + (dx * PREDICTION_FRAMES))
            pred_y = int(y + (dy * PREDICTION_FRAMES))
            dist_future = np.linalg.norm(np.array((pred_x, pred_y)) - np.array((center_x, center_y)))
            
            is_intercept = dist_future < COLLISION_ZONE
            is_approaching = growth_rate > GROWTH_THRESHOLD

            if is_intercept:
                status_color = (0, 0, 255)
                dodge = "LEFT" if dx > 0 else "RIGHT"
                cv2.putText(frame, f"THRUST {dodge}", (50, h//2 + 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                cv2.line(frame, (x, y), (center_x, center_y), status_color, 2)
            else:
                status_color = (0, 255, 0)

            if abs(dx) > 1 or abs(dy) > 1:
                cv2.arrowedLine(frame, (x, y), (pred_x, pred_y), (0, 255, 255), 3)

        # --- 4. TRAILS & HUD ---
        for i in range(1, len(pos_pts)):
            if pos_pts[i - 1] is None or pos_pts[i] is None: continue
            thickness = int(np.sqrt(BUFFER_SIZE / float(i + 1)) * 2.5)
            cv2.line(frame, pos_pts[i - 1], pos_pts[i], (0, 0, 255), thickness)

        cv2.circle(frame, (center_x, center_y), COLLISION_ZONE, (100, 100, 100), 2)
        cv2.putText(frame, "AADES STABILIZED TRACKING", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        
        cv2.imshow("AADES Final", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
