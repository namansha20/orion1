# AADES Real-Time Camera Detection System Guide

## Overview
The AADES (Autonomous Approach Detection and Evasion System) is a real-time camera detection system that uses YOLO AI models for object detection with stabilized tracking, trajectory prediction, and collision avoidance warnings.

## What Changed
The `test_camera_api.py` file has been replaced with a fully-featured YOLO-based real-time camera detection system that performs actual object detection using a trained AI model.

### Previous Functionality
- Simple API endpoint tester
- Sent mock detection data to the server
- No actual camera or AI detection

### New Functionality
- Real-time camera feed processing
- YOLO AI model integration for object detection
- Stabilized tracking with heavy smoothing
- Velocity calculation and trajectory prediction
- Collision zone detection with visual warnings
- HUD-style interface with trails and overlays

## Prerequisites

### Hardware
- Webcam or camera device (USB or built-in)
- Sufficient processing power for real-time YOLO inference

### Software
- Python 3.8 or higher
- Trained YOLO model file (.pt format)
- Required dependencies (installed via requirements.txt):
  - opencv-python==4.8.1.78
  - ultralytics==8.0.196
  - numpy (already included)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your YOLO model:**
   - Train your own YOLO model, or
   - Download a pre-trained model
   - Place the model file in an accessible location

3. **Configure model path:**
   
   Option A - Environment Variable (Recommended):
   ```bash
   export YOLO_MODEL_PATH="/path/to/your/model/best.pt"
   ```
   
   Option B - Direct Edit:
   Edit line 19 in `test_camera_api.py`:
   ```python
   MODEL_PATH = os.environ.get('YOLO_MODEL_PATH', '/path/to/your/model/best.pt')
   ```

## Configuration

All configuration parameters are defined at the top of `test_camera_api.py`:

### 1. AI Model Configuration
```python
MODEL_PATH = os.environ.get('YOLO_MODEL_PATH', 'best.pt')
```
- Set via `YOLO_MODEL_PATH` environment variable
- Default: `best.pt` (in current directory)

### 2. Smoothing Settings
```python
SMOOTH_FACTOR = 0.15  # Lower = smoother, higher = more responsive
DEADZONE_PIXELS = 3   # Ignore movements smaller than this
```
- `SMOOTH_FACTOR`: Controls tracking smoothness (0.05-0.3 recommended)
- `DEADZONE_PIXELS`: Anti-vibration threshold

### 3. Physics Constants
```python
BUFFER_SIZE = 32          # History buffer size
PREDICTION_FRAMES = 15    # Frames to predict ahead
COLLISION_ZONE = 80       # Collision warning radius (pixels)
GROWTH_THRESHOLD = 0.5    # Growth rate threshold
MOVEMENT_THRESHOLD = 2    # Minimum movement to detect
VELOCITY_CALC_FRAMES = 5  # Frames for velocity calculation
```

### 4. Detection Filters
```python
CONFIDENCE_MIN = 0.25  # Minimum detection confidence
RATIO_MIN = 0.60       # Minimum aspect ratio
RATIO_MAX = 1.60       # Maximum aspect ratio
MAX_COAST_FRAMES = 10  # Prediction frames when target lost
```

### 5. Camera Settings
```python
EXPOSURE_VAL = -5.0            # Camera exposure value
camera_index = 0               # Camera device index
```
- Set camera index via `CAMERA_INDEX` environment variable

## Running the System

### Basic Usage
```bash
python test_camera_api.py
```

### With Environment Variables
```bash
export YOLO_MODEL_PATH="/path/to/model/best.pt"
export CAMERA_INDEX=0
python test_camera_api.py
```

### Expected Output
```
🔄 SYSTEM BOOT: Loading AI from /path/to/model/best.pt...
✅ AI BRAIN ONLINE.
🚀 AADES SENSOR ACTIVE. STABILIZER ENGAGED.
```

## Features

### 1. Real-Time Detection
- Uses YOLO model for object detection
- Processes video frames in real-time
- Confidence-based filtering

### 2. Stabilized Tracking
- **Exponential Moving Average**: Smooths position over time
- **Deadzone Filter**: Ignores micro-movements (jitter elimination)
- **Aspect Ratio Filter**: Filters out invalid detections

### 3. Trajectory Prediction
- Calculates velocity from position history
- Predicts future position based on current velocity
- Displays prediction arrow when object is moving

### 4. Collision Detection
- **Collision Zone**: Circular area around screen center
- **Warning System**: Visual alerts when object enters zone
- **Evasion Suggestion**: Displays recommended dodge direction

### 5. Visual Overlays
- **Bounding Box**: Green box around detected object
- **Trajectory Trail**: Red trail showing past positions
- **Prediction Arrow**: Cyan arrow showing predicted path
- **Collision Line**: Red line when object threatens collision
- **HUD Text**: Status information and warnings

### 6. Coasting (Momentum Prediction)
- When object temporarily lost (occlusion, low confidence)
- Continues tracking using last known velocity
- Displays "PREDICTING..." ghost box
- Maintains up to 10 frames of prediction

## Visual Interface

### Display Elements
1. **AADES STABILIZED TRACKING** - Title text (top-left)
2. **Green Box** - Detected object with smooth tracking
3. **Red Trail** - Object's recent path (fading with time)
4. **Cyan Arrow** - Predicted trajectory
5. **Gray Circle** - Collision zone boundary
6. **Cyan Text** - Evasion warnings ("THRUST LEFT/RIGHT")
7. **Ghost Box** - Prediction mode (gray, when coasting)

### Color Coding
- 🟢 **Green** - Active detection, safe
- 🔴 **Red** - Collision threat, danger zone
- 🔵 **Cyan** - Predictions, trajectory arrows
- ⚪ **Gray** - Coasting/prediction mode

## Controls

- **'q' key** - Quit the application
- **ESC key** - Also quits (OpenCV default)

## Troubleshooting

### Model Loading Issues
```
❌ CRITICAL ERROR: Model file not found at best.pt
```
**Solution**: Set `YOLO_MODEL_PATH` environment variable or place model at correct path.

### Camera Issues
```
❌ ERROR: Could not open camera at index 0
```
**Solutions**:
- Check if camera is connected
- Try different camera index (set `CAMERA_INDEX=1`)
- Close other applications using the camera
- Check camera permissions (especially on macOS/Linux)

### No Detections Appearing
**Possible causes**:
- Model not trained for your objects
- Confidence threshold too high (lower `CONFIDENCE_MIN`)
- Aspect ratio filter too strict (adjust `RATIO_MIN`/`RATIO_MAX`)
- Poor lighting conditions

### Jittery Tracking
**Solutions**:
- Lower `SMOOTH_FACTOR` (e.g., 0.10 for more smoothing)
- Increase `DEADZONE_PIXELS` (e.g., 5 or 10)
- Increase `VELOCITY_CALC_FRAMES` for more stable velocity

### Sluggish Response
**Solutions**:
- Increase `SMOOTH_FACTOR` (e.g., 0.25 for faster response)
- Decrease `DEADZONE_PIXELS`
- Use faster hardware or smaller YOLO model

## Cross-Platform Compatibility

### Windows
- Uses DirectShow (`CAP_DSHOW`) backend automatically
- Better camera performance and stability

### Linux/macOS
- Uses default V4L2 (Linux) or AVFoundation (macOS)
- May require additional permissions on some systems

### Camera Permissions
- **macOS**: Grant Terminal/Python camera access in System Preferences
- **Linux**: User must be in `video` group: `sudo usermod -a -G video $USER`
- **Windows**: Usually works without additional permissions

## Integration with ORION-EYE

This camera detection system can be integrated with the main ORION-EYE application:

### Option 1: Standalone Mode (Current)
Run independently for real-time detection and tracking.

### Option 2: API Integration (Future)
Send detection data to ORION-EYE's `/api/camera-detection` endpoint:
```python
import requests

detections = {
    "detections": [{
        "id": "DEBRIS_001",
        "type": "debris",
        "x": normalized_x,
        "y": normalized_y,
        "size": normalized_size,
        "distance": estimated_distance,
        "velocity": {"x": vel_x, "y": vel_y},
        "confidence": confidence
    }]
}

response = requests.post('http://localhost:5000/api/camera-detection', json=detections)
```

## Performance Optimization

### Tips for Better Performance
1. **Use smaller YOLO model** (YOLOv8n instead of YOLOv8x)
2. **Reduce video resolution** (modify camera capture settings)
3. **Increase confidence threshold** (fewer false positives)
4. **Disable verbose mode** (already set in code)
5. **Use GPU** (CUDA-enabled PyTorch for ultralytics)

### GPU Acceleration
If you have NVIDIA GPU:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Advanced Configuration

### Tuning for Different Objects

**For Fast-Moving Objects:**
```python
SMOOTH_FACTOR = 0.25          # More responsive
PREDICTION_FRAMES = 20        # Predict further ahead
MAX_COAST_FRAMES = 5          # Less coasting
```

**For Slow-Moving Objects:**
```python
SMOOTH_FACTOR = 0.10          # Very smooth
PREDICTION_FRAMES = 10        # Less prediction
MAX_COAST_FRAMES = 15         # More coasting
```

**For Small Objects:**
```python
CONFIDENCE_MIN = 0.20         # Accept lower confidence
DEADZONE_PIXELS = 2           # Less deadzone
COLLISION_ZONE = 50           # Smaller collision zone
```

## Development Notes

### Code Structure
- **Initialization** (lines 48-58): Load YOLO model
- **Helper Functions** (lines 60-89): Dynamics calculation, direction labels
- **Main Loop** (lines 91-236): Camera capture, detection, visualization

### Key Algorithms
1. **Exponential Moving Average (EMA)**: Smooths tracking
   ```python
   smooth_x = (smooth_x * (1 - α)) + (raw_x * α)
   ```

2. **Velocity Calculation**: Uses multiple frames
   ```python
   dx = mean(pos[i-1] - pos[i]) for recent frames
   ```

3. **Growth Rate**: Recent radius vs old radius
   ```python
   growth_rate = mean(recent_radius) - mean(old_radius)
   ```

## Security Considerations

- No network communication (runs locally)
- No data storage or logging
- Model file should be from trusted source
- Camera access requires user permission

## Future Enhancements

Potential improvements:
- [ ] Multi-object tracking
- [ ] Object classification (debris types)
- [ ] Distance estimation using known object sizes
- [ ] API integration with ORION-EYE dashboard
- [ ] Recording and playback
- [ ] Custom training data collection
- [ ] Performance metrics and benchmarking

## Contributing

To modify or extend:
1. Fork the repository
2. Make changes to `test_camera_api.py`
3. Test thoroughly with your model and camera
4. Submit pull request with description

## License

Part of the ORION-EYE project. See main repository LICENSE.

## Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Test with different configuration parameters
4. Open issue in repository with:
   - Error message
   - Configuration used
   - System information
   - Steps to reproduce

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready  
**Tested On**: Windows 10/11, Ubuntu 20.04/22.04, macOS 12+
