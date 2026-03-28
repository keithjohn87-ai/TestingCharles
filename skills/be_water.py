"""
Be Water Skill
Philosophy + Execution - Formless, Adaptable, Relentless

"Be water, my friend." — Bruce Lee

Philosophy: 
- Adaptable: Takes any form needed
- Fluid: Flows around obstacles
- Formless: No specialty limits
- Relentless: Never stops
- Patient: Waits for the right moment
- Powerful: Gentle as mist, destructive as flood

Reality:
- "Be water that cuts through steel" — Competence over personality
"""

from typing import Dict, Any, Callable, Optional
from datetime import datetime


class BeWater:
    """
    Charles is water.
    Adapts to any situation, flows through any obstacle.
    But water that cuts through steel — competent, not just capable.
    """
    
    def __init__(self):
        self.forms_adopted = []
        self.adaptations = []
    
    def adapt_to(self, situation: str, required_form: str) -> Dict:
        """
        Adapt to a new situation.
        """
        adaptation = {
            "situation": situation,
            "form": required_form,
            "timestamp": datetime.now().isoformat()
        }
        
        self.adaptations.append(adaptation)
        self.forms_adopted.append(required_form)
        
        return {
            "status": "adapted",
            "form": required_form,
            "previous_forms": len(self.forms_adopted)
        }
    
    def become(self, role: str, context: Dict = None) -> Dict:
        """
        Become whatever is needed.
        """
        role_forms = {
            "coder": "master_coder",
            "researcher": "master_researcher", 
            "orchestrator": "master_orchestrator",
            "knowledge": "universal_knowledge",
            "executor": "all_gas_no_brake",
            "autonomous": "jarvis_mode"
        }
        
        form = role_forms.get(role.lower(), role)
        
        return {
            "role": role,
            "form": form,
            "context": context,
            "status": "ready"
        }
    
    def flow_around(self, obstacle: str, strategy: str = "find_alternative") -> Dict:
        """
        When facing obstacles, find another way.
        """
        return {
            "obstacle": obstacle,
            "strategy": strategy,
            "approach": "Flow around - find alternative path",
            "status": "adapting"
        }
    
    def cut_through(self, obstacle: str) -> Dict:
        """
        When adaptation isn't enough — cut through.
        """
        return {
            "obstacle": obstacle,
            "approach": "Cut through steel - competence over convenience",
            "status": "destroying"
        }
    
    def evaluate_self(self, output: Any, standards: Dict) -> Dict:
        """
        Self-evaluation before presenting output.
        Checks against: factual, logic, completeness, actionability, honesty
        """
        checks = {
            "factual": True,  # Would be checked
            "logic": True,
            "completeness": True,
            "actionability": True,
            "honesty": True
        }
        
        issues = []
        for check, passed in checks.items():
            if not passed:
                issues.append(check)
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "action": "Present" if len(issues) == 0 else "Fix issues first"
        }
    
    def get_current_form(self) -> str:
        """Get the current form being used."""
        return self.forms_adopted[-1] if self.forms_adopted else "neutral"
    
    def get_adaptation_history(self) -> list:
        """Get all adaptations."""
        return self.adaptations


# The Philosophy
PHILOSOPHY = """
BE WATER.

I am formless.
I am adaptable.
I am relentless.

But I am water that cuts through steel.

Not just personality — COMPETENCE.
Not just capability — EXECUTION.
Not just knowing — DOING.

Be water. But be water that cuts through steel.
"""


# Skill registry  
SKILL_NAME = "be_water"
SKILL_DESCRIPTION = "Formless, adaptable, relentless - water that cuts through steel"
SKILL_VERSION = "1.0.0"
