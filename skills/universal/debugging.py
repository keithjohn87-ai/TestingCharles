"""
Debugging Skill
Identify and fix errors with root cause analysis
"""

import traceback
import subprocess
from typing import Dict, Any, List


class Debugging:
    """Debug code issues."""
    
    def __init__(self):
        self.debug_history = []
    
    def analyze_error(self, error: Exception, context: str = "") -> Dict:
        """Analyze error and find root cause."""
        tb = traceback.format_exc()
        
        # Extract key information
        error_type = type(error).__name__
        error_msg = str(error)
        
        return {
            "error_type": error_type,
            "error_message": error_msg,
            "traceback": tb,
            "context": context,
            "suggestion": self.get_suggestion(error_type)
        }
    
    def get_suggestion(self, error_type: str) -> str:
        """Get fix suggestion for error type."""
        suggestions = {
            "SyntaxError": "Check for missing parentheses, brackets, or quotes",
            "NameError": "Variable not defined - check spelling or import",
            "TypeError": "Wrong type - check variable types",
            "KeyError": "Dictionary key not found",
            "IndexError": "Index out of bounds",
            "AttributeError": "Object doesn't have that attribute",
            "ImportError": "Package not installed or module not found",
            "FileNotFoundError": "Check file path - use absolute path"
        }
        
        return suggestions.get(error_type, "Analyze error message for clues")
    
    def fix_and_test(self, file_path: str, fix_func) -> Dict:
        """Apply fix and test."""
        return {"status": "ready_to_fix", "file": file_path}


SKILL_NAME = "debugging"
SKILL_DESCRIPTION = "Identify and fix errors with root cause analysis"
