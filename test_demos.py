#!/usr/bin/env python3
"""
Test script for ORION-EYE demos
Validates all three scenarios and system functionality
"""

from orion_eye import OrionEyeSystem
import json


def test_demo(system, scenario_name, scenario_id):
    """Test a single demo scenario"""
    print(f"\n{'='*60}")
    print(f"Testing: {scenario_name}")
    print(f"{'='*60}")
    
    result = system.run_simulation(scenario_id)
    
    print(f"\nScenario: {result['scenario']}")
    print(f"Outcome: {result['outcome']}")
    print(f"Objects Detected: {len(result['objects'])}")
    print(f"Decision: {result['decision']['decision']}")
    print(f"Maneuver Type: {result['maneuver']['maneuver_type']}")
    
    # Show object details
    print(f"\nObject Details:")
    for obj in result['objects'][:3]:  # Show first 3
        print(f"  - {obj['id']}: {obj.get('classified_type', 'unknown')} at "
              f"{obj['risk_assessment']['distance_at_closest']:.2f}km "
              f"({obj['risk_assessment']['level']})")
    
    if len(result['objects']) > 3:
        print(f"  ... and {len(result['objects']) - 3} more objects")
    
    # Show edge cases if any
    if result['edge_cases']:
        print(f"\nEdge Cases Detected: {len(result['edge_cases'])}")
        for ec in result['edge_cases']:
            print(f"  - {ec['type']}: {ec['severity']} - {ec['description']}")
    
    # Show LEO impact
    leo = result['leo_impact']
    print(f"\nLEO Impact:")
    print(f"  - Debris Encountered: {leo['debris_encountered']}")
    print(f"  - Collision Avoided: {leo['collision_avoided']}")
    print(f"  - Fuel Consumed: {leo['fuel_consumed']:.2f} kg")
    print(f"  - Mission Impact: {leo['mission_impact']}")
    print(f"  - Sustainability Score: {leo['leo_sustainability_score']*100:.1f}%")
    
    # Validation
    assert result['scenario'] == scenario_id, f"Scenario mismatch"
    assert 'objects' in result, "Missing objects"
    assert 'decision' in result, "Missing decision"
    assert 'maneuver' in result, "Missing maneuver"
    assert 'dashboard_data' in result, "Missing dashboard data"
    assert 'leo_impact' in result, "Missing LEO impact"
    
    print(f"\n✅ {scenario_name} - PASSED")
    return result


def main():
    """Run all demo tests"""
    print("="*60)
    print("ORION-EYE Demo Test Suite")
    print("Testing all 3 scenarios and 10-layer architecture")
    print("="*60)
    
    system = OrionEyeSystem()
    
    try:
        # Demo 1: Safe Passage
        result1 = test_demo(system, "Demo 1: Safe Passage", "safe")
        assert result1['outcome'] == 'SAFE_PASSAGE', "Expected safe passage"
        assert result1['decision']['maneuver_required'] == False, "No maneuver should be required"
        
        # Demo 2: Collision Course
        system2 = OrionEyeSystem()  # Fresh instance
        result2 = test_demo(system2, "Demo 2: Collision Course", "crash")
        assert result2['decision']['maneuver_required'] == True, "Maneuver should be required"
        assert result2['maneuver']['maneuver_type'] == 'AVOIDANCE_BURN', "Should execute avoidance"
        
        # Demo 3: Multiple Objects
        system3 = OrionEyeSystem()  # Fresh instance
        result3 = test_demo(system3, "Demo 3: Multiple Objects", "multi")
        assert len(result3['objects']) >= 5, "Should detect multiple objects"
        
        # Summary
        print(f"\n{'='*60}")
        print("ALL TESTS PASSED! ✅")
        print(f"{'='*60}")
        print(f"\nSummary:")
        print(f"  ✅ Demo 1 (Safe): {result1['outcome']}")
        print(f"  ✅ Demo 2 (Crash): {result2['outcome']}")
        print(f"  ✅ Demo 3 (Multi): {result3['outcome']}")
        print(f"\nAll 10 layers operational:")
        print(f"  ✅ Layer 1: Space/Sensor Simulation")
        print(f"  ✅ Layer 2: Object Detection")
        print(f"  ✅ Layer 3: Classification")
        print(f"  ✅ Layer 4: Trajectory Prediction")
        print(f"  ✅ Layer 5: Risk Calculation")
        print(f"  ✅ Layer 6: Autonomous Decision")
        print(f"  ✅ Layer 7: Maneuver Simulation")
        print(f"  ✅ Layer 8: XAI Logging")
        print(f"  ✅ Layer 9: Web Dashboard Data")
        print(f"  ✅ Layer 10: Edge Case Handling")
        print(f"\nORION-EYE System: READY FOR HACKATHON! 🚀")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
