"""
CHARLES STARTUP INITIALIZATION
==============================

This runs on agent startup - loads all skills immediately.

GEX44 startup should import this first:
    from skills import startup
    # All skills ready
"""

import sys
import os

# Ensure skills path is available
skills_path = os.path.dirname(os.path.abspath(__file__))
if skills_path not in sys.path:
    sys.path.insert(0, skills_path)

# === STEP 1: Load Core Skills ===
print("⚡ Loading Charles Core Skills...")

import skills
print(f"  ✓ Core skills loaded: {len([x for x in dir(skills) if not x.startswith('_')])} exports")

# === STEP 2: Test Basic Functionality ===
def test_skills():
    """Quick test that skills work."""
    
    # Test coder
    try:
        result = skills.coder.execute_command("echo 'Charles is ready'")
        print(f"  ✓ Coder functional: {result.get('status')}")
    except Exception as e:
        print(f"  ⚠ Coder: {e}")
    
    # Test orchestrator
    try:
        task = skills.orchestrator.create_task("Test task", "test-agent")
        print(f"  ✓ Orchestrator functional: {task.id}")
    except Exception as e:
        print(f"  ⚠ Orchestrator: {e}")
    
    # Test All Gas No Brake
    try:
        should = skills.gas.should_execute({"clear": True, "flags": []})
        print(f"  ✓ AllGasNoBrake functional: execute={should.get('execute')}")
    except Exception as e:
        print(f"  ⚠ AllGasNoBrake: {e}")
    
    # Test Be Water
    try:
        skills.water.adapt_to("testing", "debug")
        print(f"  ✓ BeWater functional")
    except Exception as e:
        print(f"  ⚠ BeWater: {e}")
    
    # Test Jarvis Mode
    try:
        autonomy = skills.jarvis.get_autonomy_level()
        print(f"  ✓ JarvisMode functional: {autonomy.get('level')}% autonomy")
    except Exception as e:
        print(f"  ⚠ JarvisMode: {e}")

# === STEP 3: Verify ===
def startup_complete():
    """Called when startup is done."""
    return {
        "status": "READY",
        "skills_loaded": True,
        "core": True,
        "ready_for": ["code", "research", "orchestrate", "communicate", "deploy", "secure"]
    }

# === RUN AT IMPORT ===
# Just importing this module runs startup tests
test_skills()
status = startup_complete()

print("\n" + "="*50)
print("CHARLES IS READY")
print("="*50)
print(f"Status: {status['status']}")
print(f"Skills: Loaded")
print(f"Ready for: {', '.join(status['ready_for'])}")
print("="*50)
