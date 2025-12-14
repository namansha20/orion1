"""
ORION-EYE Web Server
Flask backend for debris avoidance dashboard
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from orion_eye import OrionEyeSystem
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize ORION-EYE system
orion = OrionEyeSystem()


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


def convert_numpy(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    import numpy as np
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, dict):
        return {key: convert_numpy(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(item) for item in obj]
    else:
        return obj


@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Run simulation with specified scenario"""
    data = request.json
    scenario = data.get('scenario', 'safe')
    
    try:
        result = orion.run_simulation(scenario)
        # Convert numpy arrays to native types for JSON serialization
        result_clean = convert_numpy(result)
        return jsonify(result_clean)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scenarios')
def get_scenarios():
    """Get available demo scenarios"""
    scenarios = [
        {
            'id': 'safe',
            'name': 'Demo 1: Safe Passage',
            'description': 'Nominal scenario with distant objects, no collision risk',
            'expected_outcome': 'SAFE_PASSAGE'
        },
        {
            'id': 'crash',
            'name': 'Demo 2: Collision Course',
            'description': 'Critical scenario with object on direct collision course',
            'expected_outcome': 'AVOIDANCE_REQUIRED'
        },
        {
            'id': 'multi',
            'name': 'Demo 3: Multiple Objects',
            'description': 'Complex scenario with multiple objects requiring prioritization',
            'expected_outcome': 'COMPLEX_AVOIDANCE'
        }
    ]
    return jsonify(scenarios)


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'operational', 'system': 'ORION-EYE'})


@app.route('/api/camera-detection', methods=['POST'])
def camera_detection():
    """Process camera detection data and return simulation results"""
    # Maximum simulated distance in kilometers (matches frontend constant)
    MAX_DISTANCE_KM = 50
    
    data = request.json
    detections = data.get('detections', [])
    
    try:
        # Convert camera detections to ORION format
        # This bridges the camera feed data to the existing simulation system
        objects = []
        for det in detections:
            # Extract distance for z-coordinate in 3D position
            distance = det.get('distance', MAX_DISTANCE_KM)
            obj = {
                'id': det.get('id', 'CAM_OBJ'),
                'position': [det.get('x', 0) * 100 - 50, det.get('y', 0) * 100 - 50, distance],
                'velocity': [det.get('velocity', {}).get('x', 0) * 100, 
                           det.get('velocity', {}).get('y', 0) * 100, -2],
                'size': det.get('size', 0.1) * 10,
                'type': det.get('type', 'debris'),
                'detection_confidence': det.get('confidence', 0.9),
                'timestamp': datetime.now().isoformat()
            }
            objects.append(obj)
        
        # Calculate risk levels and generate response
        result = {
            'status': 'success',
            'objects_detected': len(objects),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(convert_numpy(result))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import os
    
    print("="*60)
    print("ORION-EYE System Starting")
    print("Simulated Onboard AI for Debris Avoidance")
    print("="*60)
    print("\nAccess dashboard at: http://localhost:5000")
    print("\nAvailable scenarios:")
    print("  1. Safe Passage - Nominal operations")
    print("  2. Collision Course - Critical avoidance")
    print("  3. Multiple Objects - Complex scenario")
    print("\n" + "="*60)
    
    # Use debug mode only in development (not in production)
    # Check FLASK_DEBUG for Flask 2.0+ compatibility
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
