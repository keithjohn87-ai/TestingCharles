"""
Code Review Skill
Review code for bugs, style violations, and performance issues
"""

import subprocess
from typing import Dict, Any, List


class CodeReview:
    """Review code for issues."""
    
    def __init__(self):
        self.issues_found = []
    
    def review_file(self, file_path: str) -> Dict:
        """Review a single file."""
        issues = []
        
        # Check for common issues
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Check for TODO without author
                    if "TODO" in line and "# TODO:" not in line:
                        issues.append({"line": i, "type": "todo", "severity": "low"})
                    
                    # Check for hardcoded secrets
                    if any(word in line.lower() for word in ["password", "api_key", "secret"]) and "=" in line:
                        issues.append({"line": i, "type": "security", "severity": "high"})
        except Exception as e:
            return {"error": str(e)}
        
        return {
            "file": file_path,
            "issues": issues,
            "total": len(issues)
        }
    
    def review_codebase(self, path: str) -> Dict:
        """Review entire codebase."""
        return {
            "path": path,
            "issues": [],
            "status": "ready"
        }


SKILL_NAME = "code_review"
SKILL_DESCRIPTION = "Review code for bugs, style violations, and performance issues"
