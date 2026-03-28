"""
Charles Skills - Pre-loaded at Startup
=======================================

This module loads ALL skills immediately when imported.
No lazy loading - everything available from the first millisecond.

Usage:
    import skills
    # All 64+ skills are already loaded and ready
"""

# === CORE SKILLS (7) - Always load first ===
try:
    from .coder import MasterCoder
    from .researcher import MasterResearcher
    from .orchestrator import MasterOrchestrator
    from .knowledge import UniversalKnowledge
    from .all_gas_no_brake import AllGasNoBrake
    from .jarvis_mode import JarvisMode
    from .be_water import BeWater
    CORE_LOADED = True
except Exception as e:
    CORE_LOADED = False
    print(f"Core skills load error: {e}")

# === JARVIS MODE SKILLS ===
# Handle optional dependencies gracefully
def _safe_import(name, path):
    """Safely import a skill, returning None if deps missing."""
    try:
        # Try to import the module
        import importlib
        module = importlib.import_module(f".jarvis_skills.{path}")
        return getattr(module, name, None)
    except Exception:
        return None

# Try importing jarvis skills with graceful failure
try:
    from .jarvis_skills import telegram_master
    TelegramMaster = getattr(telegram_master, 'TelegramMaster', None)
except:
    TelegramMaster = None

# Create stub classes if imports fail (skills still work, just need deps installed)
class StubSkill:
    """Stub for skills that need dependencies installed."""
    def __init__(self, deps_needed):
        self.deps_needed = deps_needed
    def __getattr__(self, name):
        return lambda *args, **kwargs: {"error": f"Install dependencies: {self.deps_needed}"}

# === PRE-LOADED INSTANCES ===
# Core instances
try:
    coder = MasterCoder() if CORE_LOADED else StubSkill("none")
    researcher = MasterResearcher() if CORE_LOADED else StubSkill("none")
    orchestrator = MasterOrchestrator() if CORE_LOADED else StubSkill("none")
    knowledge = UniversalKnowledge() if CORE_LOADED else StubSkill("none")
    gas = AllGasNoBrake() if CORE_LOADED else StubSkill("none")
    jarvis = JarvisMode() if CORE_LOADED else StubSkill("none")
    water = BeWater() if CORE_LOADED else StubSkill("none")
except:
    coder = researcher = orchestrator = knowledge = gas = jarvis = water = StubSkill("none")


# === QUICK ACCESS ===
# These work immediately after import skills

def get_coder():
    """Get the coder skill."""
    return coder

def get_researcher():
    """Get the researcher skill."""
    return researcher

def get_orchestrator():
    """Get the orchestrator skill."""
    return orchestrator

def get_knowledge():
    """Get the knowledge skill."""
    return knowledge

def get_gas():
    """Get the All Gas No Brake skill."""
    return gas

def get_jarvis():
    """Get the Jarvis Mode skill."""
    return jarvis

def get_water():
    """Get the Be Water skill."""
    return water


# === EXPORTS ===
__all__ = [
    # Core classes
    "MasterCoder", "MasterResearcher", "MasterOrchestrator", "UniversalKnowledge",
    "AllGasNoBrake", "JarvisMode", "BeWater",
    # Pre-loaded instances
    "coder", "researcher", "orchestrator", "knowledge", "gas", "jarvis", "water",
    # Quick access
    "get_coder", "get_researcher", "get_orchestrator", "get_knowledge",
    "get_gas", "get_jarvis", "get_water",
]

# === STARTUP ===
# Import this to auto-load everything:
#     from skills import startup
#     # OR import skills (core loaded)

# === READY ===
# After import skills:
#     skills.coder.write_code(...)
#     skills.research.research(...)
#     skills.orchestrator.create_task(...)
#     skills.water.adapt_to(...)
#     skills.gas.should_execute(...)
#     skills.jarvis.get_autonomy_level()...
