#!/usr/bin/env python3
"""
Verification script for webcam AR overlay feature
Tests that all components are integrated correctly
"""

import requests
import time


def verify_server_running():
    """Verify Flask server is running"""
    print("\n" + "="*70)
    print("1. Verifying Server Status")
    print("="*70)
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            print("✓ Server is running and responsive")
            return True
        else:
            print(f"✗ Server returned unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server on http://localhost:5000")
        print("  Please start the server with: python app.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def verify_html_contains_webcam_elements():
    """Verify HTML contains webcam UI elements"""
    print("\n" + "="*70)
    print("2. Verifying Webcam UI Elements in HTML")
    print("="*70)
    
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        html = response.text
        
        required_elements = [
            ("webcam-container", "Webcam container div"),
            ("webcam-video", "Video element for camera feed"),
            ("overlay-canvas", "Canvas overlay for AR drawings"),
            ("toggleWebcam", "Webcam toggle function"),
            ("runDetectionLoop", "Detection loop function"),
            ("drawDetections", "Drawing function for bounding boxes"),
            ("updateDashboardFromDetections", "Dashboard update function"),
            ("hud-reticle", "HUD corner reticles"),
            ("Start Webcam Detection", "Start button text"),
        ]
        
        all_found = True
        for element_id, description in required_elements:
            if element_id in html:
                print(f"  ✓ Found: {description}")
            else:
                print(f"  ✗ Missing: {description}")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"✗ Error fetching HTML: {e}")
        return False


def verify_camera_api_endpoint():
    """Verify camera detection API endpoint works"""
    print("\n" + "="*70)
    print("3. Verifying Camera Detection API Endpoint")
    print("="*70)
    
    test_data = {
        "detections": [
            {
                "id": "TEST_DEBRIS_001",
                "type": "debris",
                "x": 0.5,
                "y": 0.5,
                "size": 0.2,
                "distance": 12.5,
                "velocity": {"x": 0.001, "y": -0.002},
                "confidence": 0.95
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/api/camera-detection",
            json=test_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ API endpoint responds correctly")
            print(f"  ✓ Processed {result['objects_detected']} detection(s)")
            print(f"  ✓ Response timestamp: {result['timestamp']}")
            return True
        else:
            print(f"  ✗ API returned status {response.status_code}")
            print(f"     Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error calling API: {e}")
        return False


def verify_old_scenarios_still_work():
    """Verify original simulation scenarios still function"""
    print("\n" + "="*70)
    print("4. Verifying Original Simulation Scenarios")
    print("="*70)
    
    scenarios = ["safe", "crash", "multi"]
    all_work = True
    
    for scenario in scenarios:
        try:
            response = requests.post(
                "http://localhost:5000/api/simulate",
                json={"scenario": scenario},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✓ {scenario.capitalize()} scenario: {data.get('outcome', 'N/A')}")
            else:
                print(f"  ✗ {scenario.capitalize()} scenario failed")
                all_work = False
                
        except Exception as e:
            print(f"  ✗ Error testing {scenario}: {e}")
            all_work = False
    
    return all_work


def verify_dashboard_panels_present():
    """Verify all dashboard panels are present"""
    print("\n" + "="*70)
    print("5. Verifying Dashboard Panels")
    print("="*70)
    
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        html = response.text
        
        panels = [
            ("System Status", "system-status"),
            ("Detected Objects", "objects-table"),
            ("Maneuver Planning", "maneuver-details"),
            ("XAI Logs", "xai-logs"),
            ("Real-Time Camera Detection", "Real-Time Camera Detection")
        ]
        
        all_found = True
        for panel_name, panel_id in panels:
            if panel_id in html:
                print(f"  ✓ Panel present: {panel_name}")
            else:
                print(f"  ✗ Panel missing: {panel_name}")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all verification tests"""
    print("\n" + "="*70)
    print("ORION-EYE WEBCAM FEATURE VERIFICATION")
    print("="*70)
    print("\nThis script verifies that the webcam AR overlay feature")
    print("has been successfully integrated into ORION-EYE.")
    
    results = {}
    
    # Run all verification tests
    results["Server Running"] = verify_server_running()
    
    if not results["Server Running"]:
        print("\n" + "="*70)
        print("❌ VERIFICATION FAILED")
        print("="*70)
        print("\nServer is not running. Please start it with:")
        print("  python app.py")
        return False
    
    results["Webcam UI Elements"] = verify_html_contains_webcam_elements()
    results["Camera API Endpoint"] = verify_camera_api_endpoint()
    results["Original Scenarios"] = verify_old_scenarios_still_work()
    results["Dashboard Panels"] = verify_dashboard_panels_present()
    
    # Print summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL VERIFICATIONS PASSED")
        print("="*70)
        print("\nThe webcam AR overlay feature is successfully integrated!")
        print("\nNext steps:")
        print("  1. Open http://localhost:5000 in your browser")
        print("  2. Click 'Start Webcam Detection' button")
        print("  3. Grant camera permissions")
        print("  4. Hold an object in front of camera to test detection")
        print("  5. Observe dashboard panels updating with detection data")
    else:
        print("❌ SOME VERIFICATIONS FAILED")
        print("="*70)
        print("\nPlease review the failures above and fix them.")
    
    print("="*70)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
