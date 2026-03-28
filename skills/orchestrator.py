"""
Master Orchestrator Skill
Task management, sub-agent direction, and validation for Charles
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class Task:
    """Represents a single task."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    
    def __init__(self, task_id: str, name: str, assigned_to: str = None):
        self.id = task_id
        self.name = name
        self.assigned_to = assigned_to
        self.status = self.PENDING
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.completed_at = None
        self.error = None
        self.model_used = None
        self.log = []
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "error": self.error,
            "model_used": self.model_used,
            "log": self.log
        }


class MasterOrchestrator:
    """
    Charles as a master orchestrator.
    Manages tasks, directs sub-agents, validates outputs.
    """
    
    def __init__(self, tracker_path: str = "/opt/charles/tracker"):
        self.tracker_path = tracker_path
        self.tasks = {}
        self.task_counter = 0
    
    def create_task(self, name: str, assigned_to: str = None) -> Task:
        """Create a new task."""
        self.task_counter += 1
        task_id = f"task-{self.task_counter:04d}"
        task = Task(task_id, name, assigned_to)
        self.tasks[task_id] = task
        return task
    
    def assign_task(self, task_id: str, sub_agent_id: str, instructions: str) -> Dict:
        """Assign a task to a sub-agent with instructions."""
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        
        task = self.tasks[task_id]
        task.assigned_to = sub_agent_id
        task.status = Task.IN_PROGRESS
        task.updated_at = datetime.now().isoformat()
        task.log.append({
            "timestamp": datetime.now().isoformat(),
            "event": "assigned",
            "to": sub_agent_id,
            "instructions": instructions
        })
        
        return {"status": "assigned", "task_id": task_id, "sub_agent": sub_agent_id}
    
    def complete_task(self, task_id: str, result: Any = None) -> Dict:
        """Mark a task as completed."""
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        
        task = self.tasks[task_id]
        task.status = Task.COMPLETED
        task.completed_at = datetime.now().isoformat()
        task.updated_at = datetime.now().isoformat()
        task.log.append({
            "timestamp": datetime.now().isoformat(),
            "event": "completed",
            "result": result
        })
        
        return {"status": "completed", "task_id": task_id}
    
    def fail_task(self, task_id: str, error: str) -> Dict:
        """Mark a task as failed."""
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        
        task = self.tasks[task_id]
        task.status = Task.FAILED
        task.error = error
        task.updated_at = datetime.now().isoformat()
        task.log.append({
            "timestamp": datetime.now().isoformat(),
            "event": "failed",
            "error": error
        })
        
        return {"status": "failed", "task_id": task_id, "error": error}
    
    def redirect_task(self, task_id: str, feedback: str) -> Dict:
        """Redirect a task with specific feedback."""
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        
        task = self.tasks[task_id]
        task.status = Task.IN_PROGRESS  # Reset to in progress
        task.updated_at = datetime.now().isoformat()
        task.log.append({
            "timestamp": datetime.now().isoformat(),
            "event": "redirected",
            "feedback": feedback
        })
        
        return {"status": "redirected", "task_id": task_id, "feedback": feedback}
    
    def validate_output(self, task_id: str, output: Any, requirements: List[str]) -> Dict:
        """
        Validate task output against requirements.
        Returns: {"valid": bool, "issues": []}
        """
        issues = []
        
        for req in requirements:
            # Simple validation checks
            if "not empty" in req.lower() and (not output or output == ""):
                issues.append(f"Requirement not met: {req}")
            if "error" in output.lower() and "error" in req.lower():
                issues.append(f"Output contains error: {req}")
        
        is_valid = len(issues) == 0
        
        # Log the validation
        if task_id in self.tasks:
            self.tasks[task_id].log.append({
                "timestamp": datetime.now().isoformat(),
                "event": "validated",
                "valid": is_valid,
                "issues": issues
            })
        
        return {"valid": is_valid, "issues": issues}
    
    def get_task_status(self, task_id: str) -> Dict:
        """Get status of a task."""
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        return self.tasks[task_id].to_dict()
    
    def get_queue_status(self) -> Dict:
        """Get overall queue status."""
        pending = sum(1 for t in self.tasks.values() if t.status == Task.PENDING)
        in_progress = sum(1 for t in self.tasks.values() if t.status == Task.IN_PROGRESS)
        completed = sum(1 for t in self.tasks.values() if t.status == Task.COMPLETED)
        failed = sum(1 for t in self.tasks.values() if t.status == Task.FAILED)
        
        return {
            "total": len(self.tasks),
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "failed": failed
        }
    
    def log_to_tracker(self, sub_agent_id: str, sub_agent_name: str, project_id: str,
                       event_type: str, task_id: str = "", description: str = "",
                       severity: str = "low", resolution: str = "", model_used: str = "") -> Dict:
        """
        Log event to the sub-agent tracker.
        This would call the tracker.py script.
        """
        # This is a placeholder - actual execution would call the tracker CLI
        return {
            "action": "log_to_tracker",
            "sub_agent_id": sub_agent_id,
            "event_type": event_type,
            "note": "Execute tracker.py log command"
        }


# Skill registry
SKILL_NAME = "master_orchestrator"
SKILL_DESCRIPTION = "Task management, sub-agent direction, validation loop"
SKILL_VERSION = "1.0.0"
