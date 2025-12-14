#!/usr/bin/env python3
"""
Test script for camera detection API endpoint
Validates the new /api/camera-detection endpoint
"""

import requests
import json


def test_camera_detection_endpoint():
    """Test the camera detection API endpoint"""
    print("\n" + "="*60)
    print("Testing Camera Detection API Endpoint")
    print("="*60)
    
    url = "http://localhost:5000/api/camera-detection"
    
    # Test data simulating camera detections
    test_detections = {
        "detections": [
            {
                "id": "DEBRIS_001",
                "type": "debris",
                "x": 0.3,
                "y": 0.4,
                "size": 0.15,
                "distance": 8.5,
                "velocity": {"x": 0.002, "y": 0.001},
                "confidence": 0.92
            },
            {
                "id": "DEBRIS_002",
                "type": "debris",
                "x": 0.6,
                "y": 0.5,
                "size": 0.08,
                "distance": 25.3,
                "velocity": {"x": -0.001, "y": 0.003},
                "confidence": 0.87
            }
        ]
    }
    
    try:
        response = requests.post(url, json=test_detections)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Success!")
            print(f"  Objects Detected: {result['objects_detected']}")
            print(f"  Timestamp: {result['timestamp']}")
            print("\nTest PASSED: Camera detection endpoint working correctly")
            return True
        else:
            print(f"✗ Error: {response.text}")
            print("\nTest FAILED")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to server")
        print("  Make sure Flask server is running on http://localhost:5000")
        print("\nTest FAILED")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        print("\nTest FAILED")
        return False


def test_health_endpoint():
    """Test the health endpoint to ensure server is running"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    url = "http://localhost:5000/api/health"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Server is operational: {result['system']}")
            return True
        else:
            print(f"✗ Unexpected status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Server not running")
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("ORION-EYE Camera Detection API Test Suite")
    print("="*60)
    
    # Test health first
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("\n⚠️  Please start the Flask server first:")
        print("   python app.py")
        exit(1)
    
    # Test camera detection
    camera_ok = test_camera_detection_endpoint()
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Health Endpoint: {'✓ PASS' if health_ok else '✗ FAIL'}")
    print(f"Camera Detection: {'✓ PASS' if camera_ok else '✗ FAIL'}")
    print("="*60)
    
    if health_ok and camera_ok:
        print("\n✓ All tests passed!")
        exit(0)
    else:
        print("\n✗ Some tests failed")
        exit(1)
