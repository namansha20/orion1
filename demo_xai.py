#!/usr/bin/env python3
"""
ORION-EYE XAI (Explainable AI) Demonstration
Shows the explainable decision-making process
"""

from orion_eye import OrionEyeSystem


def demo_xai_explanation(scenario_name, scenario_id):
    """Demonstrate XAI capabilities for a scenario"""
    print("\n" + "="*70)
    print(f"  {scenario_name}")
    print("="*70)
    
    system = OrionEyeSystem()
    result = system.run_simulation(scenario_id)
    
    # Show the full XAI explanation
    print("\n" + result['explanation'])
    
    # Show detailed logs
    print("\n" + "-"*70)
    print("DETAILED DECISION LOG:")
    print("-"*70)
    for log in result['dashboard_data']['logs']:
        print(f"[{log['phase'].upper():15s}] {log['message']}")
    
    # Show edge cases if any
    if result['edge_cases']:
        print("\n" + "-"*70)
        print("EDGE CASE ANALYSIS:")
        print("-"*70)
        for ec in result['edge_cases']:
            print(f"\n⚠️  {ec['type']} ({ec['severity']} severity)")
            print(f"   Description: {ec['description']}")
            print(f"   Mitigation: {ec['mitigation']}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Run XAI demonstrations"""
    print("\n" + "="*70)
    print(" "*15 + "ORION-EYE EXPLAINABLE AI DEMONSTRATION")
    print("="*70)
    print("\nThis demonstration shows how ORION-EYE provides transparent,")
    print("auditable decision-making for autonomous collision avoidance.")
    print("\nEvery decision is logged, explained, and justified in human-readable")
    print("format - critical for aerospace certification and mission safety.")
    
    # Demo 1: Safe scenario
    demo_xai_explanation("DEMO 1: SAFE PASSAGE - Nominal Operations", "safe")
    
    # Demo 2: Critical scenario
    demo_xai_explanation("DEMO 2: COLLISION COURSE - Critical Avoidance", "crash")
    
    # Demo 3: Complex scenario  
    demo_xai_explanation("DEMO 3: MULTIPLE OBJECTS - Complex Decision Making", "multi")
    
    # Summary
    print("="*70)
    print(" "*20 + "XAI DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nKey Takeaways:")
    print("  ✅ Every decision is logged with timestamps")
    print("  ✅ Natural language explanations for all actions")
    print("  ✅ Complete audit trail from detection to execution")
    print("  ✅ Edge cases automatically identified and documented")
    print("  ✅ Regulatory compliance ready (DO-178C, ECSS)")
    print("\nThis transparency is essential for:")
    print("  • Post-mission analysis")
    print("  • Failure investigation")
    print("  • Certification processes")
    print("  • Building trust in autonomous systems")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
