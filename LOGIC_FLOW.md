# ORION-EYE Logic Flow Documentation

## System Architecture Overview

ORION-EYE employs a sequential 10-layer architecture where each layer builds upon the output of the previous layer. This modular design ensures maintainability, testability, and extensibility.

## Detailed Logic Flow

### Phase 1: Environment Awareness

#### Layer 1: Space/Sensor Simulation
**Input:** Scenario configuration ('safe', 'crash', 'multi')

**Logic:**
1. Initialize spacecraft position in LEO (default: [0, 0, 400] km from Earth center)
2. Set sensor parameters (range: 100km, accuracy: 95%)
3. Generate debris field based on scenario:
   - **Safe:** 2 distant objects
   - **Crash:** 1 object on collision course
   - **Multi:** 8 objects with varied positions
4. For each object, generate:
   - Unique ID
   - 3D position vector (x, y, z)
   - 3D velocity vector (km/s)
   - Size (meters)
   - Type (debris or satellite)

**Output:** List of space objects with physical properties

**Key Decision Points:**
- Scenario selection determines threat level
- Random generation ensures varied testing
- Realistic LEO parameters used (orbital velocities 7-8 km/s)

---

#### Layer 2: Object Detection
**Input:** Raw sensor data from Layer 1

**Logic:**
1. Apply detection algorithm to each object
2. Calculate detection confidence using model accuracy (92% ± 5%)
3. Filter objects based on confidence threshold (>0.5)
4. Add detection timestamp
5. Preserve all object properties

**Output:** List of detected objects with confidence scores

**Key Decision Points:**
- Confidence threshold determines detection sensitivity
- Timestamp enables temporal tracking
- Some objects may be filtered out (simulates sensor limitations)

---

### Phase 2: Understanding

#### Layer 3: Classification
**Input:** Detected objects from Layer 2

**Logic:**
1. For each detected object:
   - Analyze size parameter
   - Calculate velocity magnitude
   - Apply classification rules:
     * Small + Fast → Likely debris (confidence: 0.85-0.95)
     * Large + Slow → Likely satellite (confidence: 0.80-0.95)
     * Other → Use original type (confidence: 0.75-0.85)
2. Add classification confidence score
3. Tag with classified_type

**Output:** Objects with type classification and confidence

**Key Decision Points:**
- Size/velocity patterns inform classification
- Confidence varies based on characteristic clarity
- Conservative approach for ambiguous cases

---

#### Layer 4: Trajectory Prediction
**Input:** Classified objects, spacecraft position

**Logic:**
1. For each object:
   - Extract current position and velocity
   - Define prediction horizon (300 seconds)
   - Divide into time steps (10 steps)
   - For each time step:
     * Calculate future position using linear motion
     * Calculate distance to spacecraft
     * Store trajectory point
2. Identify closest approach point (minimum distance)
3. Record time to closest approach

**Output:** Objects with predicted trajectories and closest approach data

**Key Decision Points:**
- Linear trajectory assumption (simplifies calculation)
- 300-second horizon balances foresight with accuracy
- Closest approach is critical for risk assessment

**Mathematical Model:**
```
future_position(t) = current_position + velocity * t
distance(t) = ||future_position(t) - spacecraft_position||
closest_approach = min(distance(t)) for all t
```

---

### Phase 3: Assessment

#### Layer 5: Risk Calculation
**Input:** Objects with trajectory predictions

**Logic:**
1. For each object:
   - Extract closest approach distance
   - Extract time to closest approach
   - Apply risk level rules:
     * Distance < 5 km → CRITICAL (score: 0.9-1.0)
     * Distance < 10 km → HIGH (score: 0.5-0.9)
     * Distance < 20 km → MEDIUM (score: 0.3-0.5)
     * Distance ≥ 20 km → LOW (score: 0.01-0.3)
2. Calculate risk score using distance-based formula
3. Set maneuver requirement flag for CRITICAL/HIGH risks
4. Package risk assessment data

**Output:** Objects with complete risk assessment

**Key Decision Points:**
- Distance thresholds based on spacecraft size and maneuver time
- Risk score provides numerical comparison
- Binary maneuver flag enables clear decision-making

**Risk Scoring Formula:**
```
For CRITICAL: score = 0.9 + min(0.1, (5 - distance)/5 * 0.1)
For HIGH: score = 0.5 + (10 - distance)/10 * 0.4
For MEDIUM: score = 0.3 + (20 - distance)/20 * 0.2
For LOW: score = max(0.01, 0.3 - (distance - 20)/100)
```

---

### Phase 4: Decision Making

#### Layer 6: Autonomous Decision
**Input:** All risk-assessed objects

**Logic:**
1. Filter objects requiring maneuvers (CRITICAL or HIGH risk)
2. Decision tree:
   - **If no high-risk objects:**
     * Decision: MAINTAIN_COURSE
     * Reason: No threats detected
     * Maneuver required: False
   - **If high-risk objects exist:**
     * Sort by risk score (descending)
     * Select highest risk as primary threat
     * Decision: EXECUTE_AVOIDANCE
     * Reason: Collision risk with primary threat
     * Maneuver required: True
     * List all priority objects

**Output:** Autonomous decision with justification

**Key Decision Points:**
- Highest risk object gets priority
- Clear reasoning provided for auditability
- Binary decision (avoid or maintain) for simplicity
- Multi-object scenarios handled through prioritization

---

### Phase 5: Execution Planning

#### Layer 7: Maneuver Simulation
**Input:** Decision, risk-assessed objects, spacecraft position

**Logic:**
1. Check maneuver requirement:
   - **If not required:**
     * Return null maneuver (no action)
   - **If required:**
     * Identify primary threat object
     * Calculate relative position vector
     * Calculate threat velocity vector
     * Compute perpendicular avoidance direction:
       - Use cross product: perpendicular = threat_velocity × relative_position
       - Normalize to unit vector
     * Scale by risk score: delta_v = perpendicular * 0.5 * risk_score
     * Calculate burn duration: 10 * delta_v_magnitude seconds
     * Estimate fuel cost: 100 * delta_v_magnitude kg
     * Set success probability: 95%

**Output:** Maneuver plan with delta-V, duration, fuel cost, and probability

**Key Decision Points:**
- Perpendicular avoidance minimizes delta-V requirement
- Risk-proportional response (higher risk = larger maneuver)
- Success probability acknowledges execution uncertainty

**Maneuver Calculation:**
```
relative_position = threat_position - spacecraft_position
perpendicular = normalize(threat_velocity × relative_position)
delta_v_magnitude = 0.5 * risk_score  # km/s
delta_v_vector = perpendicular * delta_v_magnitude
burn_time = 10 * delta_v_magnitude  # seconds
fuel = 100 * delta_v_magnitude  # kg
```

---

### Phase 6: Explanation & Monitoring

#### Layer 8: Explainable AI Logging
**Input:** All layer outputs

**Logic:**
1. Log each phase with timestamp:
   - Detection: Number of objects identified
   - Classification: Debris vs satellite counts
   - Risk: Count by risk level
   - Decision: Chosen action and reason
   - Maneuver: Type and delta-V requirement
2. Generate natural language explanation:
   - List all detected objects
   - Explain decision rationale
   - Detail maneuver parameters
   - Provide success probability

**Output:** Comprehensive log entries and human-readable explanation

**Key Decision Points:**
- All decisions logged for audit trail
- Human-readable format for transparency
- Timestamps enable temporal analysis

---

#### Layer 9: Web Dashboard Preparation
**Input:** All system data

**Logic:**
1. Calculate summary statistics:
   - Total objects detected
   - Critical/high-risk counts
   - Decision status
   - Maneuver requirement
2. Format object list for table display:
   - ID, type, distance, risk level
3. Prepare 3D visualization data:
   - Spacecraft position
   - Object positions and velocities
   - Trajectory paths
   - Risk-based color coding
4. Package decision and maneuver details
5. Include XAI logs

**Output:** Structured data for web dashboard rendering

**Key Decision Points:**
- Data formatted for efficient web rendering
- Color coding enhances visual threat identification
- All information accessible in single data structure

---

#### Layer 10: Edge Case Handling
**Input:** Objects, decision, maneuver

**Logic:**
1. Check for edge cases:
   - **Multiple Threats (>3 high-risk objects):**
     * Flag as HIGH severity
     * Recommend ground consultation
   - **High Delta-V (>1.5 km/s):**
     * Flag as MEDIUM severity
     * Note mission impact
   - **Time Critical (<60 seconds to closest):**
     * Flag as CRITICAL severity
     * Require immediate action
   - **Low Confidence (<0.7 classification):**
     * Flag as LOW severity
     * Apply conservative assessment
   - **Conflicting Threats (opposite directions):**
     * Flag as CRITICAL severity
     * Note complex maneuver required
2. For each edge case, generate:
   - Type identifier
   - Severity level
   - Description
   - Mitigation strategy

**Output:** List of edge cases with mitigations

**Key Decision Points:**
- Proactive identification of complex scenarios
- Severity-based prioritization
- Mitigation strategies for each case
- No edge case halts system operation

---

## Decision Trees

### Primary Decision Tree
```
START
  ↓
Scan Environment (Layer 1)
  ↓
Objects Detected? (Layer 2)
  ├─ NO → MAINTAIN_COURSE
  └─ YES → Continue
      ↓
Classify Objects (Layer 3)
      ↓
Predict Trajectories (Layer 4)
      ↓
Calculate Risk (Layer 5)
      ↓
High Risk Objects?
      ├─ NO → MAINTAIN_COURSE
      └─ YES → EXECUTE_AVOIDANCE
          ↓
Calculate Maneuver (Layer 7)
          ↓
Check Edge Cases (Layer 10)
          ↓
Execute & Log (Layer 8)
          ↓
Update Dashboard (Layer 9)
          ↓
END
```

### Risk Assessment Decision Tree
```
Closest Approach Distance
  ├─ < 5 km → CRITICAL → Require Maneuver
  ├─ < 10 km → HIGH → Require Maneuver
  ├─ < 20 km → MEDIUM → Monitor
  └─ ≥ 20 km → LOW → Monitor
```

### Maneuver Type Decision Tree
```
Threat Detection
  ├─ No Threat → NULL Maneuver
  └─ Threat Detected
      ├─ Single Threat → Standard Avoidance
      ├─ Multiple Aligned Threats → Prioritized Avoidance
      └─ Conflicting Threats → Complex Maneuver + Edge Case
```

## Data Flow Diagram

```
┌─────────────────┐
│   Scenario      │
│  Configuration  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Layer 1: Sim   │──── Sensor Data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Layer 2: Det   │──── Detected Objects
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Layer 3: Class │──── Classified Objects
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Layer 4: Traj  │──── Trajectory Data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Layer 5: Risk  │──── Risk Assessments
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Layer 6: Dec   │──── Decision
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Layer 7: Man   │──── Maneuver Plan
└────────┬────────┘
         │
         ├────────────────┐
         │                │
         ▼                ▼
┌─────────────────┐  ┌──────────────┐
│  Layer 8: XAI   │  │ Layer 10: EC │
└────────┬────────┘  └──────┬───────┘
         │                  │
         └─────────┬────────┘
                   │
                   ▼
         ┌─────────────────┐
         │  Layer 9: Dash  │
         └─────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │  Web Interface  │
         └─────────────────┘
```

## State Transitions

### System States
1. **IDLE:** Awaiting scenario selection
2. **SCANNING:** Layer 1 active, generating environment
3. **DETECTING:** Layer 2 active, processing sensor data
4. **ANALYZING:** Layers 3-5 active, classification and risk assessment
5. **DECIDING:** Layer 6 active, autonomous decision-making
6. **PLANNING:** Layer 7 active, maneuver calculation
7. **LOGGING:** Layer 8 active, generating explanations
8. **DISPLAYING:** Layer 9 active, updating dashboard
9. **MONITORING:** Layer 10 active, checking edge cases
10. **COMPLETE:** Results ready for display

### State Transition Triggers
- User scenario selection → IDLE to SCANNING
- Sensor data ready → SCANNING to DETECTING
- Objects detected → DETECTING to ANALYZING
- Risk assessment complete → ANALYZING to DECIDING
- Decision made → DECIDING to PLANNING
- Maneuver calculated → PLANNING to LOGGING
- Logs generated → LOGGING to DISPLAYING
- Dashboard updated → DISPLAYING to MONITORING
- Edge cases checked → MONITORING to COMPLETE

## Performance Characteristics

### Time Complexity
- Layer 1: O(n) where n = number of objects
- Layer 2: O(n)
- Layer 3: O(n)
- Layer 4: O(n*t) where t = time steps (10)
- Layer 5: O(n)
- Layer 6: O(n log n) due to sorting
- Layer 7: O(1)
- Layer 8: O(n)
- Layer 9: O(n)
- Layer 10: O(n)

**Overall:** O(n*t) dominated by trajectory prediction

### Space Complexity
- Object storage: O(n)
- Trajectory storage: O(n*t)
- Logs: O(l) where l = number of log entries

**Overall:** O(n*t)

### Response Time
- Typical execution: < 100ms for n ≤ 10 objects
- Real-time suitable for onboard processing
- No network latency (autonomous operation)

## Error Handling

### Detection Failures
- If no objects detected: System returns MAINTAIN_COURSE
- If detection confidence low: Edge case flagged

### Classification Uncertainty
- Low confidence classifications flagged in Layer 10
- Conservative risk assessment applied

### Trajectory Prediction Limitations
- Linear approximation acknowledged
- Edge case for rapid maneuvers flagged

### Maneuver Constraints
- Delta-V capacity: 2.0 km/s maximum
- High delta-V requirements flagged as edge case
- Fuel cost tracked and reported

### Edge Case Responses
- System never halts due to edge cases
- All edge cases logged with mitigations
- Critical edge cases prioritized for display

## Validation & Testing

### Unit Testing Points
1. Layer 1: Verify object generation for each scenario
2. Layer 2: Test confidence filtering
3. Layer 3: Validate classification logic
4. Layer 4: Check trajectory calculations
5. Layer 5: Verify risk level assignments
6. Layer 6: Test decision logic for all cases
7. Layer 7: Validate maneuver calculations
8. Layer 8: Check log generation
9. Layer 9: Verify data formatting
10. Layer 10: Test edge case detection

### Integration Testing
- End-to-end scenario execution
- Data flow between all layers
- Dashboard rendering validation

### Scenario Coverage
- Safe passage (no threats)
- Single threat (collision course)
- Multiple threats (prioritization)
- Edge cases (complex scenarios)

---

*This logic flow documentation ensures complete understanding of the ORION-EYE decision-making process for development, testing, and presentation purposes.*