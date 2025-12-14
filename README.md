# 🛰️ ORION-EYE: Simulated Onboard AI for Debris Avoidance

**Autonomous Space Debris Collision Avoidance System**

ORION-EYE is a simulated onboard AI system designed for real-time space debris detection and autonomous collision avoidance in Low Earth Orbit (LEO). Built with a 10-layer architecture emphasizing logic over physics, this system demonstrates advanced simulated intelligence for spacecraft safety.

## 🎯 Overview

ORION-EYE provides autonomous, real-time debris avoidance capabilities without requiring ground station communication. The system detects, classifies, and autonomously responds to collision threats in the LEO environment.

**Key Features:**
- ✨ 10-Layer AI Architecture
- 🎮 3 Interactive Demo Scenarios
- 🌐 Real-time Web Dashboard
- 📊 Explainable AI Decision Logs
- 🚀 Autonomous Maneuver Planning
- ⚠️ Advanced Edge Case Handling
- 🌍 LEO Environmental Impact Analysis

## 🏗️ 10-Layer Architecture

### Layer 1: Space/Sensor Simulation
Simulates LEO environment and sensor data collection
- Generates realistic debris fields
- Simulates spacecraft sensors with configurable range and accuracy
- Produces various scenario configurations (safe, dangerous, multi-object)

### Layer 2: Object Detection
Applies AI detection algorithms to sensor data
- Confidence-based detection filtering
- Timestamp tracking for all detections
- High accuracy detection model (92% base accuracy)

### Layer 3: Classification (Debris/Satellite)
Classifies detected objects by type
- Distinguishes between debris and satellites
- Uses size and velocity pattern analysis
- Confidence scoring for each classification

### Layer 4: Trajectory Prediction
Predicts future object positions and closest approach
- Linear trajectory modeling over 300-second horizon
- Calculates closest approach distance and time
- Generates full trajectory paths for visualization

### Layer 5: Risk Calculation
Calculates collision probability and risk levels
- Four-tier risk assessment (LOW, MEDIUM, HIGH, CRITICAL)
- Distance-based risk scoring
- Time-to-collision analysis

### Layer 6: Autonomous Decision (Avoidance)
Makes autonomous decisions without ground station
- Real-time threat prioritization
- Automatic maneuver authorization
- Multi-object threat handling

### Layer 7: Maneuver Simulation
Calculates and simulates avoidance maneuvers
- Delta-V calculation for avoidance burns
- Fuel consumption estimation
- Success probability modeling
- Perpendicular avoidance vector calculation

### Layer 8: Explainable AI (XAI) Logs
Generates human-readable decision explanations
- Phase-by-phase logging (detection, classification, risk, decision, maneuver)
- Natural language explanations
- Audit trail for all autonomous decisions

### Layer 9: Web Dashboard
Real-time visualization and monitoring
- Live 3D space environment visualization
- Object tracking and trajectory display
- Risk level indicators
- Decision and maneuver details

### Layer 10: Edge Cases Handling
Manages unusual and complex scenarios
- Multiple simultaneous threats
- High delta-V requirements
- Time-critical situations
- Low confidence classifications
- Conflicting threat directions

## 🎮 Demo Scenarios

### Demo 1: Safe Passage ✅
**Scenario:** Nominal operations with distant objects
- 2 objects detected at safe distances
- No collision risk identified
- Spacecraft maintains course
- **Expected Outcome:** SAFE_PASSAGE

### Demo 2: Collision Course ⚠️
**Scenario:** Critical situation with imminent collision
- High-risk debris on direct collision course
- CRITICAL risk level triggered
- Autonomous avoidance maneuver executed
- **Expected Outcome:** AVOIDANCE_SUCCESSFUL

### Demo 3: Multiple Objects 🎯
**Scenario:** Complex environment with multiple threats
- 8 objects in various positions
- Multiple risk levels present
- Threat prioritization required
- **Expected Outcome:** COMPLEX_AVOIDANCE

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Modern web browser

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/namansha20/orion.git
cd orion
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Access the dashboard:**
Open your browser and navigate to:
```
http://localhost:5000
```

## 📊 Web Stack

### Backend
- **Flask 3.0.0** - Python web framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **NumPy 1.24.3** - Numerical computations and trajectory calculations

### Frontend
- **HTML5** - Structure and layout
- **CSS3** - Styling with modern gradients and animations
- **Vanilla JavaScript** - Interactive controls and visualization
- **Canvas API** - 3D space environment rendering

### Architecture Pattern
- RESTful API design
- Single Page Application (SPA)
- Real-time data updates
- Responsive design for various screen sizes

## 🔧 API Endpoints

### `POST /api/simulate`
Run simulation with specified scenario
```json
{
  "scenario": "safe" | "crash" | "multi"
}
```

**Response:**
```json
{
  "scenario": "string",
  "outcome": "string",
  "objects": [...],
  "decision": {...},
  "maneuver": {...},
  "explanation": "string",
  "edge_cases": [...],
  "dashboard_data": {...},
  "leo_impact": {...}
}
```

### `GET /api/scenarios`
Get available demo scenarios

### `GET /api/health`
System health check

## 🌍 LEO Impact Analysis

ORION-EYE includes comprehensive LEO environmental impact assessment:

- **Debris Tracking:** Monitors debris encounter rate
- **Collision Prevention:** Tracks avoidance success rate
- **Fuel Management:** Calculates mission impact of maneuvers
- **Sustainability Score:** Evaluates positive impact on LEO environment
- **Debris Generation:** Ensures no new debris created by avoidance actions

## 📈 Logic Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    ORION-EYE Logic Flow                     │
└─────────────────────────────────────────────────────────────┘

1. SENSOR SIMULATION (Layer 1)
   ↓ Generate environment based on scenario
   
2. OBJECT DETECTION (Layer 2)
   ↓ Apply confidence-based detection
   
3. CLASSIFICATION (Layer 3)
   ↓ Debris vs Satellite identification
   
4. TRAJECTORY PREDICTION (Layer 4)
   ↓ Calculate future positions
   
5. RISK CALCULATION (Layer 5)
   ↓ Assess collision probability
   
6. AUTONOMOUS DECISION (Layer 6)
   ↓ Determine if maneuver required
   
7. MANEUVER CALCULATION (Layer 7)
   ↓ Compute optimal avoidance
   
8. XAI LOGGING (Layer 8)
   ↓ Generate explanations
   
9. VISUALIZATION (Layer 9)
   ↓ Update dashboard
   
10. EDGE CASE HANDLING (Layer 10)
    ↓ Manage special scenarios
    
    → OUTCOME: Safe Operation or Successful Avoidance
```

## 🎓 Implementation Guide

### For Hackathon Success

1. **Demonstrate All 3 Scenarios:**
   - Start with Demo 1 (Safe) to show nominal operations
   - Progress to Demo 2 (Crash) to demonstrate critical response
   - Finish with Demo 3 (Multi) to showcase complex decision-making

2. **Highlight Key Features:**
   - **Autonomous Operation:** No ground station required
   - **Real-time Decisions:** Sub-second response time
   - **Explainable AI:** Clear reasoning for all decisions
   - **Edge Case Robustness:** Handles complex scenarios

3. **Technical Talking Points:**
   - 10-layer modular architecture enables easy extension
   - Simulated intelligence prioritizes logic over complex physics
   - Web-based interface provides universal accessibility
   - Comprehensive logging ensures audit trail

4. **LEO Impact Narrative:**
   - System actively prevents collisions, reducing debris cascade risk
   - Fuel-efficient maneuvers minimize mission impact
   - Sustainability scoring demonstrates environmental awareness

### Extension Opportunities

- **Machine Learning Integration:** Replace simulated intelligence with trained models
- **Multi-spacecraft Coordination:** Fleet-level collision avoidance
- **Ground Station Integration:** Add backup communication layer
- **Historical Data Analysis:** Learn from past encounters
- **Real Sensor Integration:** Connect to actual spacecraft sensors

## 📹 Real-Time Camera Object Detection

ORION now includes **AADES** (Autonomous Avoidance and Detection System) - a real-time camera-based object detection and tracking system.

### Features
- **Real-time object tracking** with OpenCV
- **Red object detection** with configurable HSV color ranges
- **3D motion analysis** (X, Y, Z axes)
- **Collision prediction** with visual warnings
- **Trajectory visualization** with trailing effects
- **HUD interface** with status indicators
- **Web-based live camera preview** integrated in the dashboard

### Running Camera Detection

**Option 1: Integrated Web Dashboard (Recommended)**

Access the live camera detection preview directly from the web dashboard:

1. Start the web application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Click the **"📹 Start Live Camera Detection"** button

4. The camera preview will appear with real-time debris detection overlay

**Option 2: Standalone Camera Application**

```bash
# Run the camera detection system
python camera_detection.py
```

**Controls:**
- Press `q` to quit the application

**Configuration:**
You can adjust detection parameters in `camera_detection.py`:
- `LOWER_RED1`, `UPPER_RED1`, `LOWER_RED2`, `UPPER_RED2`: HSV color ranges for red object detection
- `BUFFER_SIZE`: Length of the trajectory trail (default: 32)
- `COLLISION_ZONE`: Radius of collision detection zone in pixels (default: 80)
- `GROWTH_THRESHOLD`: Sensitivity for approaching/receding detection (default: 0.5)

**Requirements:**
- Webcam or camera device
- OpenCV Python (opencv-python)

## 🧪 Testing

Run the system with different scenarios:

```bash
# Test individual layers
python orion_eye.py

# Test web server
python app.py

# Test camera detection
python camera_detection.py
```

## 📝 License

This project is designed for educational and hackathon purposes.

## 🏆 Hackathon Strategy

**Winning Points:**
1. ✅ Complete 10-layer architecture implementation
2. ✅ All 3 demo scenarios functional
3. ✅ Professional web dashboard with visualization
4. ✅ Explainable AI with clear decision rationale
5. ✅ Edge case handling demonstrates robustness
6. ✅ LEO impact analysis shows environmental awareness
7. ✅ Clean, modular code structure
8. ✅ Comprehensive documentation

**Presentation Flow:**
1. Introduce the problem: Space debris threatens LEO operations
2. Demonstrate Demo 1: Show safe nominal operations
3. Demonstrate Demo 2: Show critical collision avoidance
4. Demonstrate Demo 3: Show complex multi-object handling
5. Explain architecture: Walk through 10-layer system
6. Show XAI logs: Emphasize explainability
7. Discuss LEO impact: Highlight sustainability
8. Q&A: Be ready to discuss extensions and real-world application

---

**Built for ORION by Aerospace Engineering Team**

*"Simulated Intelligence for Real Safety"*
