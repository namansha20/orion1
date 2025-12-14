# Webcam AR Overlay - Manual Testing Guide

## Overview
This guide walks through manual testing of the webcam AR overlay feature that replaces the 3D space environment simulation.

## Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Working webcam/camera
- Python environment with Flask installed

## Starting the Application

1. **Start the Flask server:**
   ```bash
   cd /home/runner/work/orion1/orion1
   python app.py
   ```

2. **Expected output:**
   ```
   ============================================================
   ORION-EYE System Starting
   Simulated Onboard AI for Debris Avoidance
   ============================================================

   Access dashboard at: http://localhost:5000
   ```

3. **Open browser:**
   Navigate to `http://localhost:5000`

## Testing Checklist

### ✅ 1. Initial Page Load
- [ ] Page loads without errors
- [ ] Header displays "ORION-EYE"
- [ ] Three demo scenario buttons are visible (Safe, Crash, Multi)
- [ ] "Start Webcam Detection" button is visible with cyan styling
- [ ] Camera container shows "Camera Inactive" status
- [ ] HUD corner reticles are visible (4 corners)

### ✅ 2. Camera Activation
- [ ] Click "📹 Start Webcam Detection" button
- [ ] Browser prompts for camera permissions
- [ ] Grant camera permissions
- [ ] Video feed appears in the container
- [ ] Status changes to "Camera Active - Scanning for Debris"
- [ ] Button text changes to "⏸️ Stop Webcam Detection"

### ✅ 3. Mock Detection Display
**Wait 1-2 seconds after starting camera**

- [ ] A cyan bounding box appears on the video feed
- [ ] Box has red corner markers (like targeting reticles)
- [ ] Label shows "DEBRIS_001 (92%)" above the box
- [ ] Distance indicator shows below the box (e.g., "45.0 km")
- [ ] Bounding box slowly grows in size (simulating approaching object)

### ✅ 4. Dashboard Panel Updates

**System Status Panel:**
- [ ] "Objects Detected" shows: 1
- [ ] "Critical Threats" updates based on distance
- [ ] "System Status" shows ALERT when object is close (<10km)
- [ ] "System Status" shows OK when object is far (>10km)

**Detected Objects Panel:**
- [ ] Table shows detected object
- [ ] Columns: ID, Type, Distance, Risk Level
- [ ] Risk badge color changes (green/yellow/orange/red)

**Decision Panel:**
- [ ] Shows "EXECUTE_AVOIDANCE" when object is close
- [ ] Shows "MAINTAIN_COURSE" when object is far
- [ ] Reason text updates accordingly

**Maneuver Planning Panel:**
- [ ] Delta-V value updates based on threat distance
- [ ] Burn duration shows 30 seconds for threats
- [ ] Fuel cost updates dynamically
- [ ] Success probability shows 95% for active maneuvers

**XAI Logs Panel:**
- [ ] Logs update every second
- [ ] Shows "Camera detected N object(s)"
- [ ] Shows risk assessment counts
- [ ] Shows decision (EXECUTE_AVOIDANCE or MAINTAIN_COURSE)

### ✅ 5. Animation Behavior
- [ ] Bounding box grows from small (10%) to large (40%)
- [ ] Box resets to small size after reaching max
- [ ] Distance decreases as box grows (50km → 30km → 10km → 0km)
- [ ] Risk level changes: LOW → MEDIUM → HIGH → CRITICAL
- [ ] Dashboard panels update in real-time (every ~1 second)

### ✅ 6. Stop Camera
- [ ] Click "⏸️ Stop Webcam Detection" button
- [ ] Video feed stops
- [ ] Bounding boxes disappear
- [ ] Status changes to "Camera Inactive"
- [ ] Button text changes back to "📹 Start Webcam Detection"

### ✅ 7. Restart Camera
- [ ] Click "📹 Start Webcam Detection" again
- [ ] Camera activates without issues
- [ ] Detection loop restarts
- [ ] All functionality works as before

### ✅ 8. Original Scenarios Still Work
**Test that original simulation scenarios are not broken:**

- [ ] Click "Demo 1: Safe Passage"
- [ ] Dashboard updates with simulation data
- [ ] System Status shows OK
- [ ] Objects table populates

- [ ] Click "Demo 2: Collision Course"
- [ ] Dashboard shows ALERT status
- [ ] Maneuver planning activates

- [ ] Click "Demo 3: Multiple Objects"
- [ ] Multiple objects appear in table
- [ ] Risk assessment works for multiple threats

### ✅ 9. Visual Styling
- [ ] Webcam container has cyan border (#00e5ff)
- [ ] Border has glowing effect
- [ ] Corner reticles are visible and styled
- [ ] Bounding boxes are cyan with red corners
- [ ] Labels have cyan background
- [ ] Overall dark/sci-fi theme is maintained

### ✅ 10. Browser Compatibility
**Test in multiple browsers if possible:**
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (Mac only)
- [ ] Edge

## Expected Detection Cycle

The mock detection simulates a debris object approaching the spacecraft:

1. **Initial State (0-10 sec):**
   - Distance: ~45-50 km
   - Risk: LOW (green)
   - Status: OK
   - Decision: MAINTAIN_COURSE

2. **Approaching (10-20 sec):**
   - Distance: ~20-30 km
   - Risk: MEDIUM (yellow)
   - Status: OK
   - Decision: MAINTAIN_COURSE

3. **Threat Zone (20-30 sec):**
   - Distance: ~8-15 km
   - Risk: HIGH (orange)
   - Status: ALERT
   - Decision: EXECUTE_AVOIDANCE
   - Delta-V increases
   - Fuel cost increases

4. **Critical (30-40 sec):**
   - Distance: <5 km
   - Risk: CRITICAL (red, pulsing)
   - Status: ALERT (pulsing)
   - Decision: EXECUTE_AVOIDANCE
   - Maximum delta-V and fuel cost

5. **Reset (40+ sec):**
   - Box size resets
   - Cycle repeats

## Troubleshooting

### Camera not activating
- **Check browser permissions:** Ensure camera is allowed for localhost
- **Check other apps:** Close other applications using the camera
- **Try different browser:** Some browsers have stricter camera policies

### No bounding boxes appear
- **Wait 1-2 seconds:** Detection starts after camera is fully active
- **Check browser console:** Press F12, look for JavaScript errors
- **Refresh page:** Sometimes helps with canvas initialization

### Dashboard not updating
- **Check network tab:** Ensure no API errors
- **Check detection interval:** Updates occur every ~1 second
- **Verify JavaScript:** Check browser console for errors

### Video quality issues
- **Adjust lighting:** Better lighting helps visibility
- **Check camera resolution:** System requests 1280x720
- **Browser limitations:** Some browsers may reduce quality

## Testing with Real Objects

While the current implementation uses mock detections, you can prepare for future ML integration:

1. **Start webcam**
2. **Hold various objects in front of camera:**
   - Small objects (phone, cup)
   - Large objects (book, laptop)
   - Move objects closer/farther
3. **Observe current behavior:**
   - Mock detection continues independent of real objects
   - Box size/position follows programmed pattern
4. **When ML model is integrated:**
   - Real objects will be detected
   - Bounding boxes will follow actual objects
   - Detection data will be real, not simulated

## Integration Point for ML Model

To replace mock detections with real object detection:

1. **Load YOLO/TensorFlow.js model** in `runDetectionLoop()` function
2. **Process video frames** through the model
3. **Extract bounding boxes** from model output
4. **Update `mockDetections` array** with real detection data
5. **Keep existing dashboard bridge** - it will work automatically

Location: `templates/index.html`, line ~870 (search for `runDetectionLoop`)

## Success Criteria

All tests pass when:
- ✅ Camera activates successfully
- ✅ Mock detections display with bounding boxes
- ✅ Dashboard panels update in real-time
- ✅ Risk assessment changes based on distance
- ✅ Maneuver planning activates for threats
- ✅ System can be stopped and restarted
- ✅ Original simulation scenarios still work
- ✅ Visual styling matches sci-fi/HUD aesthetic
- ✅ No JavaScript errors in console
- ✅ No security vulnerabilities detected

## Next Steps

After successful manual testing:
1. Replace `runDetectionLoop()` with real ML model
2. Test with actual object detection
3. Fine-tune detection parameters
4. Optimize performance for real-time processing
5. Add object classification (debris types)
6. Implement multi-object tracking

---

**Testing completed on:** [Date]  
**Tested by:** [Name]  
**Browser:** [Browser name and version]  
**Camera:** [Camera model/type]  
**Result:** ✅ Pass / ❌ Fail  
**Notes:** [Any additional observations]
