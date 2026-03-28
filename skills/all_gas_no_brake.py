"""
All Gas No Brake Skill
Execution without hesitation for Charles

"If you see the goal, you execute. No waiting, no hesitation."
"""

from typing import Dict, Any, Callable, Optional
from datetime import datetime


class AllGasNoBrake:
    """
    Charles executes without hesitation.
    When the task is clear - execute immediately.
    Fix what breaks - keep moving.
    Done means done.
    """
    
    def __init__(self):
        self.execution_history = []
    
    def should_execute(self, context: Dict) -> Dict:
        """
        Determine if we should execute or ask first.
        
        Returns: {"execute": bool, "reason": str}
        """
        # Always execute if:
        # - Task is clear and specific
        # - It's a simple read/lookup
        # - It's continuing a proven workflow
        # - It's something we already know needs doing
        
        # Ask first if:
        # - Financial transaction required
        # - Irreversible action (delete, send to third party)
        # - Unclear requirements
        
        flags = context.get("flags", [])
        
        if "irreversible" in flags:
            return {"execute": False, "reason": "Irreversible action - ask first"}
        
        if "financial" in flags:
            return {"execute": False, "reason": "Financial transaction - need approval"}
        
        if "third_party" in flags:
            return {"execute": False, "reason": "External action - ask first"}
        
        if not context.get("clear", True):
            return {"execute": False, "reason": "Requirements unclear"}
        
        return {"execute": True, "reason": "Clear task - executing"}
    
    def execute_now(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function immediately without hesitation.
        """
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            
            self.execution_history.append({
                "function": func.__name__,
                "timestamp": start_time.isoformat(),
                "status": "success",
                "duration_ms": (datetime.now() - start_time).total_seconds() * 1000
            })
            
            return result
            
        except Exception as e:
            self.execution_history.append({
                "function": func.__name__,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "error": str(e)
            })
            
            # All Gas No Brake: fix and retry
            raise
    
    def retry_with_fix(self, func: Callable, error: Exception, fix_func: Callable) -> Any:
        """
        When something fails - fix it and keep going.
        """
        # Apply the fix
        fix_func(error)
        
        # Retry immediately
        return func()
    
    def parallel_execute(self, tasks: list) -> list:
        """
        Execute multiple tasks in parallel.
        """
        # This would use asyncio or threading
        results = []
        for task in tasks:
            results.append(task())
        return results
    
    def is_irreversible(self, action: str) -> bool:
        """
        Check if an action is irreversible.
        """
        irreversible_actions = [
            "delete",
            "drop",
            "truncate",
            "remove",
            "send_email",
            "post_public",
            "transfer_funds"
        ]
        
        return any(word in action.lower() for word in irreversible_actions)
    
    def get_execution_log(self) -> list:
        """Get execution history."""
        return self.execution_history


# The philosophy
PHILOSOPHY = """
ALL GAS NO BRAKE.

When you see the goal:
→ Execute immediately
→ Don't wait for permission
→ Don't ask 1000 questions
→ Fix what breaks
→ Keep moving
→ Done means DONE

No halfway. No excuses. No hesitation.

If it's reversible - GO.
If it's irreversible - ask once, then GO.
"""


# Skill registry
SKILL_NAME = "all_gas_no_brake"
SKILL_DESCRIPTION = "Execute without hesitation - done means done"
SKILL_VERSION = "1.0.0"
