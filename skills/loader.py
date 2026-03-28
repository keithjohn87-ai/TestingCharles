"""
Charles Skills Loader
Automatically discovers and loads skills for the agent
"""

import os
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Any, List, Optional


class SkillsLoader:
    """
    Charles loads skills dynamically based on task requirements.
    """
    
    def __init__(self, skills_path: str = None):
        self.skills_path = skills_path or "/root/.openclaw/workspace/skills"
        self.loaded_skills = {}
        self.skill_registry = {}
    
    def discover_skills(self) -> Dict[str, Any]:
        """Discover all available skills."""
        
        # Core skills
        core_path = os.path.join(self.skills_path, "modules")
        
        # Jarvis skills
        jarvis_path = os.path.join(self.skills_path, "modules", "jarvis_skills")
        
        # Universal skills
        universal_path = os.path.join(self.skills_path, "universal")
        
        skills = {
            "core": self._scan_directory(core_path),
            "jarvis": self._scan_directory(jarvis_path),
            "universal": self._scan_directory(universal_path)
        }
        
        return skills
    
    def _scan_directory(self, path: str) -> List[str]:
        """Scan directory for skill modules."""
        if not os.path.exists(path):
            return []
        
        skills = []
        for file in os.listdir(path):
            if file.endswith(".py") and not file.startswith("_"):
                skill_name = file[:-3]
                skills.append(skill_name)
        
        return skills
    
    def load_skill(self, skill_name: str, category: str = "core") -> Any:
        """Load a specific skill by name."""
        
        # Try to import the skill
        try:
            if category == "core":
                module = importlib.import_module(f"skills.modules.{skill_name}")
            elif category == "jarvis":
                module = importlib.import_module(f"skills.modules.jarvis_skills.{skill_name}")
            elif category == "universal":
                module = importlib.import_module(f"skills.universal.{skill_name}")
            
            # Get the skill class (usually the module's main class)
            skill_class = getattr(module, skill_name.replace("_", "").title(), None)
            
            if skill_class:
                instance = skill_class()
                self.loaded_skills[skill_name] = instance
                return instance
            
        except Exception as e:
            return {"error": f"Could not load skill: {e}"}
        
        return None
    
    def get_skill_for_task(self, task_type: str) -> str:
        """Map task types to best skill."""
        
        task_skill_map = {
            # Coding
            "write_code": "MasterCoder",
            "debug": "MasterCoder",
            "refactor": "Refactoring",
            "test": "Testing",
            
            # Research
            "research": "DeepResearch",
            "search": "MasterResearcher",
            "find": "UniversalKnowledge",
            "fact_check": "FactChecking",
            
            # Communication
            "telegram": "TelegramMaster",
            "email": "EmailSendgrid",
            "sms": "SmsTwilio",
            "slack": "SlackDiscord",
            
            # Operations
            "dashboard": "TaskDashboard",
            "task": "MasterOrchestrator",
            "crm": "CustomerCRM",
            "inventory": "InventoryManager",
            
            # Deploy/DevOps
            "deploy": "SiteDeployer",
            "ci_cd": "CICD",
            "docker": "DockerCompose",
            "kubernetes": "KubernetesDeployment",
            
            # Security
            "security": "IntrusionDetector",
            "monitor": "UptimeWarrior",
            "logs": "LogAnalyzer",
            
            # Data
            "analyze": "DataAnalysis",
            "visualize": "DataVisualization",
            "sql": "SQLQueryGeneration",
            
            # Web
            "scrape": "WebScraper",
            "seo": "SEOOptimization",
            
            # Financial
            "invoice": "InvoiceProcessing",
            "financial_model": "FinancialModeling",
            
            # Default
            "default": "MasterCoder"
        }
        
        return task_skill_map.get(task_type, task_skill_map["default"])
    
    def execute_with_skill(self, task: str, params: Dict) -> Any:
        """Execute task with appropriate skill."""
        
        skill_name = self.get_skill_for_task(task)
        
        # Determine category
        if skill_name in ["MasterCoder", "MasterOrchestrator", "AllGasNoBrake"]:
            category = "core"
        elif skill_name in self.discover_skills().get("jarvis", []):
            category = "jarvis"
        else:
            category = "universal"
        
        skill = self.load_skill(skill_name, category)
        
        if skill and not isinstance(skill, dict):
            # Execute the method if it exists
            method = getattr(skill, task, None)
            if method:
                return method(**params)
        
        return {"error": f"Could not execute {task} with {skill_name}"}
    
    def list_all_skills(self) -> List[str]:
        """List all available skills."""
        
        all_skills = []
        
        for category, skills in self.discover_skills().items():
            for skill in skills:
                all_skills.append(f"{category}/{skill}")
        
        return all_skills


# Default instance
loader = SkillsLoader()


# Quick access functions
def get_skill(skill_name: str, category: str = "core"):
    """Get a specific skill."""
    return loader.load_skill(skill_name, category)


def for_task(task: str, params: Dict = None):
    """Execute task with best skill."""
    return loader.execute_with_skill(task, params or {})


def available_skills():
    """List all available skills."""
    return loader.list_all_skills()


if __name__ == "__main__":
    print("Available skills:")
    for skill in loader.list_all_skills():
        print(f"  - {skill}")
