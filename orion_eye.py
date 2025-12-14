"""
ORION-EYE: Simulated Onboard AI for Debris Avoidance
10-Layer Architecture for Space Debris Collision Avoidance
"""

import numpy as np
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional


class Layer1_SpaceSensorSimulator:
    """Layer 1: Space/Sensor Simulation - Simulates LEO environment and sensor data"""
    
    def __init__(self, spacecraft_position=(0, 0, 400)):
        self.spacecraft_position = np.array(spacecraft_position)  # km from Earth center
        self.sensor_range = 100  # km
        self.sensor_accuracy = 0.95
        
    def generate_debris_field(self, num_objects: int = 5) -> List[Dict]:
        """Generate simulated space objects in LEO"""
        objects = []
        for i in range(num_objects):
            obj = {
                'id': f'OBJ_{i:03d}',
                'position': self.spacecraft_position + np.random.uniform(-50, 50, 3),
                'velocity': np.random.uniform(-8, 8, 3),  # km/s
                'size': np.random.uniform(0.1, 5.0),  # meters
                'type': np.random.choice(['debris', 'satellite'], p=[0.7, 0.3])
            }
            objects.append(obj)
        return objects
    
    def scan_environment(self, scenario: str = 'safe') -> List[Dict]:
        """Scan and return detected objects based on scenario"""
        if scenario == 'safe':
            return self.generate_debris_field(2)
        elif scenario == 'crash':
            # Dangerous scenario with objects on collision course
            obj = {
                'id': 'OBJ_DANGER',
                'position': self.spacecraft_position + np.array([5, 0, 0]),
                'velocity': np.array([-7.5, 0, 0]),  # Direct collision course
                'size': 2.5,
                'type': 'debris'
            }
            return [obj]
        elif scenario == 'multi':
            return self.generate_debris_field(8)
        else:
            return self.generate_debris_field(3)


class Layer2_ObjectDetector:
    """Layer 2: Object Detection - Detects objects from sensor data"""
    
    def __init__(self):
        self.detection_threshold = 0.5
        self.confidence_model_accuracy = 0.92
        
    def detect_objects(self, sensor_data: List[Dict]) -> List[Dict]:
        """Apply detection algorithm to sensor data"""
        detected_objects = []
        for obj in sensor_data:
            confidence = self.confidence_model_accuracy + np.random.uniform(-0.05, 0.05)
            if confidence > self.detection_threshold:
                detected = obj.copy()
                detected['detection_confidence'] = confidence
                detected['timestamp'] = datetime.now().isoformat()
                detected_objects.append(detected)
        return detected_objects


class Layer3_Classifier:
    """Layer 3: Classify (Debris/Satellite) - Classifies detected objects"""
    
    def __init__(self):
        self.classification_accuracy = 0.88
        
    def classify_object(self, obj: Dict) -> Dict:
        """Classify object as debris or satellite"""
        # Simulated classification based on size and velocity patterns
        size = obj['size']
        velocity_magnitude = np.linalg.norm(obj['velocity'])
        
        # Classification logic (simulated intelligence)
        if size < 1.0 and velocity_magnitude > 5:
            predicted_type = 'debris'
            confidence = 0.85 + np.random.uniform(0, 0.1)
        elif size > 3.0 and velocity_magnitude < 5:
            predicted_type = 'satellite'
            confidence = 0.80 + np.random.uniform(0, 0.15)
        else:
            predicted_type = obj['type']
            confidence = 0.75 + np.random.uniform(0, 0.1)
            
        obj['classified_type'] = predicted_type
        obj['classification_confidence'] = confidence
        return obj
    
    def classify_all(self, objects: List[Dict]) -> List[Dict]:
        """Classify all detected objects"""
        return [self.classify_object(obj) for obj in objects]


class Layer4_TrajectoryPredictor:
    """Layer 4: Trajectory Prediction - Predicts future positions"""
    
    def __init__(self):
        self.prediction_horizon = 300  # seconds
        self.time_steps = 10
        
    def predict_trajectory(self, obj: Dict, spacecraft_pos: np.ndarray) -> Dict:
        """Predict object trajectory over time"""
        position = np.array(obj['position'])
        velocity = np.array(obj['velocity'])
        
        trajectory = []
        dt = self.prediction_horizon / self.time_steps
        
        for i in range(self.time_steps):
            t = i * dt
            # Simple linear trajectory (simulated)
            future_pos = position + velocity * t
            distance_to_spacecraft = np.linalg.norm(future_pos - spacecraft_pos)
            
            trajectory.append({
                'time': t,
                'position': future_pos.tolist(),
                'distance': distance_to_spacecraft
            })
        
        obj['predicted_trajectory'] = trajectory
        obj['closest_approach'] = min(trajectory, key=lambda x: x['distance'])
        return obj
    
    def predict_all(self, objects: List[Dict], spacecraft_pos: np.ndarray) -> List[Dict]:
        """Predict trajectories for all objects"""
        return [self.predict_trajectory(obj, spacecraft_pos) for obj in objects]


class Layer5_RiskCalculator:
    """Layer 5: Risk Calculation - Calculates collision risk"""
    
    def __init__(self):
        self.safe_distance = 5.0  # km
        self.warning_distance = 10.0  # km
        
    def calculate_risk(self, obj: Dict) -> Dict:
        """Calculate collision risk for an object
        
        Evaluates collision probability based on closest approach distance and time.
        Uses four-tier risk assessment: CRITICAL (<5km), HIGH (<10km), 
        MEDIUM (<20km), LOW (>=20km). Returns object with added risk_assessment
        containing level, score, distance, time, and maneuver requirement flag.
        
        Args:
            obj: Object dict with closest_approach data. Must contain:
                 - 'closest_approach': dict with 'distance' (float) and 'time' (float)
            
        Returns:
            Object dict with added risk_assessment field containing:
            - level: str (CRITICAL, HIGH, MEDIUM, or LOW)
            - score: float (0.01-1.0)
            - distance_at_closest: float (km)
            - time_to_closest: float (seconds)
            - requires_maneuver: bool
        """
        closest = obj['closest_approach']
        distance = closest['distance']
        time_to_closest = closest['time']
        
        # Risk calculation formula (simulated intelligence)
        if distance < self.safe_distance:
            risk_level = 'CRITICAL'
            risk_score = 0.9 + min(0.1, (self.safe_distance - distance) / self.safe_distance * 0.1)
        elif distance < self.warning_distance:
            risk_level = 'HIGH'
            risk_score = 0.5 + (self.warning_distance - distance) / self.warning_distance * 0.4
        elif distance < 20.0:
            risk_level = 'MEDIUM'
            risk_score = 0.3 + (20.0 - distance) / 20.0 * 0.2
        else:
            risk_level = 'LOW'
            risk_score = max(0.01, 0.3 - (distance - 20.0) / 100.0)
        
        obj['risk_assessment'] = {
            'level': risk_level,
            'score': risk_score,
            'distance_at_closest': distance,
            'time_to_closest': time_to_closest,
            'requires_maneuver': risk_level in ['CRITICAL', 'HIGH']
        }
        return obj
    
    def assess_all(self, objects: List[Dict]) -> List[Dict]:
        """Assess risk for all objects"""
        return [self.calculate_risk(obj) for obj in objects]


class Layer6_AutonomousDecision:
    """Layer 6: Autonomous Decision (Avoidance) - Makes avoidance decisions"""
    
    def __init__(self):
        self.decision_threshold = 0.5
        
    def make_decision(self, objects: List[Dict]) -> Dict:
        """Make autonomous avoidance decision"""
        high_risk_objects = [
            obj for obj in objects 
            if obj['risk_assessment']['requires_maneuver']
        ]
        
        if not high_risk_objects:
            return {
                'decision': 'MAINTAIN_COURSE',
                'reason': 'No high-risk objects detected',
                'maneuver_required': False,
                'priority_objects': []
            }
        
        # Sort by risk score
        high_risk_objects.sort(key=lambda x: x['risk_assessment']['score'], reverse=True)
        highest_risk = high_risk_objects[0]
        
        decision = {
            'decision': 'EXECUTE_AVOIDANCE',
            'reason': f"High risk collision with {highest_risk['id']}",
            'maneuver_required': True,
            'priority_objects': [obj['id'] for obj in high_risk_objects],
            'primary_threat': highest_risk['id'],
            'risk_score': highest_risk['risk_assessment']['score']
        }
        
        return decision


class Layer7_ManeuverSimulator:
    """Layer 7: Maneuver Simulation - Simulates avoidance maneuvers"""
    
    def __init__(self):
        self.delta_v_capacity = 2.0  # km/s available for maneuvers
        
    def calculate_maneuver(self, decision: Dict, objects: List[Dict], 
                          spacecraft_pos: np.ndarray) -> Dict:
        """Calculate optimal avoidance maneuver"""
        if not decision['maneuver_required']:
            return {
                'maneuver_type': 'NONE',
                'delta_v': [0, 0, 0],
                'burn_duration': 0,
                'fuel_cost': 0
            }
        
        # Find primary threat
        threat = next((obj for obj in objects if obj['id'] == decision['primary_threat']), None)
        
        if not threat:
            return {'maneuver_type': 'NONE', 'delta_v': [0, 0, 0], 'burn_duration': 0, 'fuel_cost': 0}
        
        # Calculate avoidance vector (perpendicular to threat trajectory)
        threat_velocity = np.array(threat['velocity'])
        threat_position = np.array(threat['position'])
        
        # Calculate perpendicular vector
        relative_pos = threat_position - spacecraft_pos
        perpendicular = np.cross(threat_velocity, relative_pos)
        
        perp_magnitude = np.linalg.norm(perpendicular)
        if perp_magnitude > 0:
            perpendicular = perpendicular / perp_magnitude
        else:
            perpendicular = np.array([0, 0, 1])
        
        # Maneuver magnitude based on risk
        maneuver_magnitude = 0.5 * decision['risk_score']  # km/s
        delta_v = perpendicular * maneuver_magnitude
        
        maneuver = {
            'maneuver_type': 'AVOIDANCE_BURN',
            'delta_v': delta_v.tolist(),
            'delta_v_magnitude': maneuver_magnitude,
            'burn_duration': maneuver_magnitude * 10,  # seconds
            'fuel_cost': maneuver_magnitude * 100,  # kg
            'direction': perpendicular.tolist(),
            'success_probability': 0.95
        }
        
        return maneuver


class Layer8_XAILogger:
    """Layer 8: Explainable AI Logs - Generates interpretable logs"""
    
    def __init__(self):
        self.logs = []
        
    def log_detection(self, objects: List[Dict]) -> str:
        """Log detection phase"""
        msg = f"DETECTION: Identified {len(objects)} objects in sensor range"
        self.logs.append({'phase': 'detection', 'message': msg, 'timestamp': datetime.now().isoformat()})
        return msg
    
    def log_classification(self, objects: List[Dict]) -> str:
        """Log classification phase"""
        debris_count = sum(1 for obj in objects if obj.get('classified_type') == 'debris')
        satellite_count = len(objects) - debris_count
        msg = f"CLASSIFICATION: {debris_count} debris, {satellite_count} satellites"
        self.logs.append({'phase': 'classification', 'message': msg, 'timestamp': datetime.now().isoformat()})
        return msg
    
    def log_risk(self, objects: List[Dict]) -> str:
        """Log risk assessment"""
        risk_levels = [obj['risk_assessment']['level'] for obj in objects]
        critical = risk_levels.count('CRITICAL')
        high = risk_levels.count('HIGH')
        msg = f"RISK ASSESSMENT: {critical} CRITICAL, {high} HIGH risk objects"
        self.logs.append({'phase': 'risk', 'message': msg, 'timestamp': datetime.now().isoformat()})
        return msg
    
    def log_decision(self, decision: Dict) -> str:
        """Log autonomous decision"""
        msg = f"DECISION: {decision['decision']} - {decision['reason']}"
        self.logs.append({'phase': 'decision', 'message': msg, 'timestamp': datetime.now().isoformat()})
        return msg
    
    def log_maneuver(self, maneuver: Dict) -> str:
        """Log maneuver execution"""
        if maneuver['maneuver_type'] == 'NONE':
            msg = "MANEUVER: No maneuver required"
        else:
            msg = f"MANEUVER: {maneuver['maneuver_type']} - ΔV={maneuver['delta_v_magnitude']:.3f} km/s"
        self.logs.append({'phase': 'maneuver', 'message': msg, 'timestamp': datetime.now().isoformat()})
        return msg
    
    def get_logs(self) -> List[Dict]:
        """Return all logs"""
        return self.logs
    
    def generate_explanation(self, objects: List[Dict], decision: Dict, maneuver: Dict) -> str:
        """Generate human-readable explanation"""
        explanation = "=== ORION-EYE DECISION EXPLANATION ===\n\n"
        
        if not objects:
            explanation += "No objects detected in vicinity. Maintaining course.\n"
            return explanation
        
        explanation += f"Detected {len(objects)} objects:\n"
        for obj in objects:
            explanation += f"  - {obj['id']}: {obj.get('classified_type', 'unknown')} at {obj['risk_assessment']['distance_at_closest']:.2f}km\n"
        
        explanation += f"\nDecision: {decision['decision']}\n"
        explanation += f"Reasoning: {decision['reason']}\n"
        
        if maneuver['maneuver_type'] != 'NONE':
            explanation += f"\nManeuver Details:\n"
            explanation += f"  - Type: {maneuver['maneuver_type']}\n"
            explanation += f"  - Delta-V: {maneuver['delta_v_magnitude']:.3f} km/s\n"
            explanation += f"  - Fuel Cost: {maneuver['fuel_cost']:.2f} kg\n"
            explanation += f"  - Success Probability: {maneuver['success_probability']*100:.1f}%\n"
        
        return explanation


class Layer9_WebDashboard:
    """Layer 9: Web Dashboard - Prepares data for visualization"""
    
    def prepare_dashboard_data(self, objects: List[Dict], decision: Dict, 
                              maneuver: Dict, logs: List[Dict], 
                              spacecraft_pos: np.ndarray) -> Dict:
        """Prepare comprehensive data for web dashboard"""
        
        # Summary statistics
        summary = {
            'total_objects': len(objects),
            'critical_objects': sum(1 for obj in objects if obj['risk_assessment']['level'] == 'CRITICAL'),
            'high_risk_objects': sum(1 for obj in objects if obj['risk_assessment']['level'] == 'HIGH'),
            'decision': decision['decision'],
            'maneuver_required': decision['maneuver_required']
        }
        
        # Object list for table
        object_list = []
        for obj in objects:
            object_list.append({
                'id': obj['id'],
                'type': obj.get('classified_type', 'unknown'),
                'distance': obj['risk_assessment']['distance_at_closest'],
                'risk_level': obj['risk_assessment']['level'],
                'risk_score': obj['risk_assessment']['score']
            })
        
        # 3D visualization data
        visualization = {
            'spacecraft': spacecraft_pos.tolist(),
            'objects': [
                {
                    'id': obj['id'],
                    'position': obj['position'],
                    'velocity': obj['velocity'],
                    'trajectory': obj.get('predicted_trajectory', []),
                    'risk_level': obj['risk_assessment']['level']
                }
                for obj in objects
            ]
        }
        
        return {
            'summary': summary,
            'objects': object_list,
            'visualization': visualization,
            'decision': decision,
            'maneuver': maneuver,
            'logs': logs
        }


class Layer10_EdgeCaseHandler:
    """Layer 10: Edge Cases - Handles unusual scenarios"""
    
    def __init__(self):
        self.edge_cases = []
        
    def check_edge_cases(self, objects: List[Dict], decision: Dict, 
                        maneuver: Dict) -> List[Dict]:
        """Check for and handle edge cases"""
        edge_cases = []
        
        # Edge Case 1: Multiple simultaneous high-risk objects
        high_risk = [obj for obj in objects if obj['risk_assessment']['level'] in ['CRITICAL', 'HIGH']]
        if len(high_risk) > 3:
            edge_cases.append({
                'type': 'MULTIPLE_THREATS',
                'severity': 'HIGH',
                'description': f'{len(high_risk)} high-risk objects detected simultaneously',
                'mitigation': 'Prioritizing highest risk object, recommend ground station consultation'
            })
        
        # Edge Case 2: Insufficient delta-v for maneuver
        if maneuver.get('delta_v_magnitude', 0) > 1.5:
            edge_cases.append({
                'type': 'HIGH_DELTA_V',
                'severity': 'MEDIUM',
                'description': f'Maneuver requires {maneuver["delta_v_magnitude"]:.3f} km/s',
                'mitigation': 'High fuel consumption, may impact mission objectives'
            })
        
        # Edge Case 3: Very close approach time
        for obj in objects:
            if obj['risk_assessment']['time_to_closest'] < 60:
                edge_cases.append({
                    'type': 'TIME_CRITICAL',
                    'severity': 'CRITICAL',
                    'description': f'Object {obj["id"]} approaching in <60 seconds',
                    'mitigation': 'Immediate maneuver execution required'
                })
                break
        
        # Edge Case 4: Low confidence classification
        low_conf = [obj for obj in objects if obj.get('classification_confidence', 1.0) < 0.7]
        if low_conf:
            edge_cases.append({
                'type': 'LOW_CONFIDENCE',
                'severity': 'LOW',
                'description': f'{len(low_conf)} objects with low classification confidence',
                'mitigation': 'Applying conservative risk assessment'
            })
        
        # Edge Case 5: No maneuver possible (conflicting threats)
        if len(high_risk) > 1 and decision['decision'] == 'EXECUTE_AVOIDANCE':
            positions = [np.array(obj['position']) for obj in high_risk]
            if len(positions) > 1:
                vectors = [pos - positions[0] for pos in positions[1:]]
                if any(np.dot(vectors[0], v) < 0 for v in vectors[1:]):
                    edge_cases.append({
                        'type': 'CONFLICTING_THREATS',
                        'severity': 'CRITICAL',
                        'description': 'Multiple threats from opposing directions',
                        'mitigation': 'Complex maneuver required, reduced success probability'
                    })
        
        self.edge_cases = edge_cases
        return edge_cases


class OrionEyeSystem:
    """Main ORION-EYE System Integration"""
    
    # LEO Impact Constants
    FUEL_COST_THRESHOLD = 50  # kg - threshold for mission impact assessment
    LEO_SUSTAINABILITY_SCORE = 0.85  # Base sustainability score
    
    def __init__(self):
        self.layer1 = Layer1_SpaceSensorSimulator()
        self.layer2 = Layer2_ObjectDetector()
        self.layer3 = Layer3_Classifier()
        self.layer4 = Layer4_TrajectoryPredictor()
        self.layer5 = Layer5_RiskCalculator()
        self.layer6 = Layer6_AutonomousDecision()
        self.layer7 = Layer7_ManeuverSimulator()
        self.layer8 = Layer8_XAILogger()
        self.layer9 = Layer9_WebDashboard()
        self.layer10 = Layer10_EdgeCaseHandler()
        
    def run_simulation(self, scenario: str = 'safe') -> Dict:
        """Run complete ORION-EYE simulation"""
        
        # Layer 1: Scan environment
        sensor_data = self.layer1.scan_environment(scenario)
        
        # Layer 2: Detect objects
        detected_objects = self.layer2.detect_objects(sensor_data)
        self.layer8.log_detection(detected_objects)
        
        if not detected_objects:
            return {
                'scenario': scenario,
                'result': 'NO_OBJECTS_DETECTED',
                'dashboard_data': self.layer9.prepare_dashboard_data(
                    [], 
                    {'decision': 'MAINTAIN_COURSE', 'reason': 'Clear space', 'maneuver_required': False},
                    {'maneuver_type': 'NONE', 'delta_v': [0,0,0], 'burn_duration': 0, 'fuel_cost': 0},
                    self.layer8.get_logs(),
                    self.layer1.spacecraft_position
                )
            }
        
        # Layer 3: Classify objects
        classified_objects = self.layer3.classify_all(detected_objects)
        self.layer8.log_classification(classified_objects)
        
        # Layer 4: Predict trajectories
        predicted_objects = self.layer4.predict_all(classified_objects, self.layer1.spacecraft_position)
        
        # Layer 5: Calculate risks
        risk_assessed_objects = self.layer5.assess_all(predicted_objects)
        self.layer8.log_risk(risk_assessed_objects)
        
        # Layer 6: Make decision
        decision = self.layer6.make_decision(risk_assessed_objects)
        self.layer8.log_decision(decision)
        
        # Layer 7: Calculate maneuver
        maneuver = self.layer7.calculate_maneuver(decision, risk_assessed_objects, 
                                                   self.layer1.spacecraft_position)
        self.layer8.log_maneuver(maneuver)
        
        # Layer 8: Generate explanation
        explanation = self.layer8.generate_explanation(risk_assessed_objects, decision, maneuver)
        
        # Layer 10: Check edge cases
        edge_cases = self.layer10.check_edge_cases(risk_assessed_objects, decision, maneuver)
        
        # Layer 9: Prepare dashboard data
        dashboard_data = self.layer9.prepare_dashboard_data(
            risk_assessed_objects,
            decision,
            maneuver,
            self.layer8.get_logs(),
            self.layer1.spacecraft_position
        )
        
        # Determine outcome
        if decision['decision'] == 'MAINTAIN_COURSE':
            outcome = 'SAFE_PASSAGE'
        elif decision['maneuver_required'] and maneuver['success_probability'] > 0.8:
            outcome = 'AVOIDANCE_SUCCESSFUL'
        elif decision['maneuver_required'] and decision['risk_score'] > 0.9:
            outcome = 'COLLISION_IMMINENT'
        else:
            outcome = 'UNCERTAIN'
        
        return {
            'scenario': scenario,
            'outcome': outcome,
            'objects': risk_assessed_objects,
            'decision': decision,
            'maneuver': maneuver,
            'explanation': explanation,
            'edge_cases': edge_cases,
            'dashboard_data': dashboard_data,
            'leo_impact': self._calculate_leo_impact(risk_assessed_objects, maneuver)
        }
    
    def _calculate_leo_impact(self, objects: List[Dict], maneuver: Dict) -> Dict:
        """Calculate impact on LEO environment"""
        debris_count = sum(1 for obj in objects if obj.get('classified_type') == 'debris')
        fuel_cost = maneuver.get('fuel_cost', 0)
        
        impact = {
            'debris_encountered': debris_count,
            'collision_avoided': maneuver['maneuver_type'] != 'NONE',
            'fuel_consumed': fuel_cost,
            'orbital_debris_contribution': 0,  # No debris created by avoidance
            'mission_impact': 'MINIMAL' if fuel_cost < self.FUEL_COST_THRESHOLD else 'MODERATE',
            'leo_sustainability_score': self.LEO_SUSTAINABILITY_SCORE  # Positive impact by avoiding collision
        }
        
        return impact


if __name__ == "__main__":
    # Quick test
    system = OrionEyeSystem()
    result = system.run_simulation('safe')
    print(json.dumps(result, indent=2, default=str))
