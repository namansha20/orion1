#!/usr/bin/env python3
"""
ORION-EYE System Verification Script
Comprehensive check of all components
"""

import os
import sys


def check_file(filename, description):
    """Check if file exists and report"""
    exists = os.path.exists(filename)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filename}")
    return exists


def check_module(module_name):
    """Check if Python module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ Module importable: {module_name}")
        return True
    except ImportError:
        print(f"❌ Module missing: {module_name}")
        return False


def main():
    print("="*70)
    print(" "*20 + "ORION-EYE SYSTEM VERIFICATION")
    print("="*70)
    
    all_good = True
    
    # Check core files
    print("\n📁 Core Files:")
    all_good &= check_file("orion_eye.py", "Core AI System")
    all_good &= check_file("app.py", "Web Server")
    all_good &= check_file("requirements.txt", "Dependencies")
    all_good &= check_file("templates/index.html", "Dashboard UI")
    
    # Check test files
    print("\n🧪 Test Files:")
    all_good &= check_file("test_demos.py", "Test Suite")
    all_good &= check_file("demo_xai.py", "XAI Demo")
    
    # Check documentation
    print("\n📚 Documentation:")
    all_good &= check_file("README.md", "Main README")
    all_good &= check_file("QUICK_START.md", "Quick Start Guide")
    all_good &= check_file("LOGIC_FLOW.md", "Logic Flow")
    all_good &= check_file("IMPLEMENTATION_GUIDE.md", "Implementation Guide")
    all_good &= check_file("PROJECT_SUMMARY.md", "Project Summary")
    
    # Check configuration
    print("\n⚙️  Configuration:")
    all_good &= check_file(".gitignore", "Git Ignore")
    
    # Check dependencies
    print("\n📦 Dependencies:")
    all_good &= check_module("flask")
    all_good &= check_module("flask_cors")
    all_good &= check_module("numpy")
    
    # Check core system
    print("\n🔍 System Components:")
    try:
        from orion_eye import OrionEyeSystem
        system = OrionEyeSystem()
        print("✅ OrionEyeSystem instantiable")
        
        # Check all layers exist
        layers = [
            'layer1', 'layer2', 'layer3', 'layer4', 'layer5',
            'layer6', 'layer7', 'layer8', 'layer9', 'layer10'
        ]
        for layer in layers:
            if hasattr(system, layer):
                print(f"✅ {layer.upper()} present")
            else:
                print(f"❌ {layer.upper()} missing")
                all_good = False
        
        # Test basic simulation
        result = system.run_simulation('safe')
        if 'scenario' in result and 'outcome' in result:
            print("✅ Simulation runs successfully")
        else:
            print("❌ Simulation output incomplete")
            all_good = False
            
    except Exception as e:
        print(f"❌ System error: {e}")
        all_good = False
    
    # Summary
    print("\n" + "="*70)
    if all_good:
        print("✅ ALL CHECKS PASSED - SYSTEM READY")
        print("\nYou can now:")
        print("  1. Run: python app.py")
        print("  2. Open: http://localhost:5000")
        print("  3. Test: python test_demos.py")
        print("  4. Demo: python demo_xai.py")
    else:
        print("❌ SOME CHECKS FAILED - REVIEW ISSUES ABOVE")
        return 1
    
    print("="*70)
    print("\n🚀 ORION-EYE: Ready for deployment!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
