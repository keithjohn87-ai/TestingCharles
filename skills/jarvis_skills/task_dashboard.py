"""
Task Dashboard Skill
Web UI to view all active tasks, status, completion
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class TaskDashboard:
    """Task dashboard for John."""
    
    def __init__(self, dashboard_path: str = "/opt/charles/dashboard"):
        self.dashboard_path = Path(dashboard_path)
        self.dashboard_path.mkdir(parents=True, exist_ok=True)
    
    def get_status(self) -> Dict:
        """Get current dashboard status."""
        tasks_file = self.dashboard_path / "tasks.json"
        
        if not tasks_file.exists():
            return {"active": 0, "pending": 0, "completed": 0}
        
        with open(tasks_file, 'r') as f:
            tasks = json.load(f)
        
        active = sum(1 for t in tasks if t.get("status") == "in_progress")
        pending = sum(1 for t in tasks if t.get("status") == "pending")
        completed = sum(1 for t in tasks if t.get("status") == "completed")
        
        return {
            "active": active,
            "pending": pending,
            "completed": completed,
            "total": len(tasks)
        }
    
    def add_task(self, task_name: str, priority: str = "medium") -> Dict:
        """Add a task to dashboard."""
        tasks_file = self.dashboard_path / "tasks.json"
        
        if tasks_file.exists():
            with open(tasks_file, 'r') as f:
                tasks = json.load(f)
        else:
            tasks = []
        
        task = {
            "id": len(tasks) + 1,
            "name": task_name,
            "status": "pending",
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }
        
        tasks.append(task)
        
        with open(tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        return {"status": "added", "task": task}
    
    def update_task(self, task_id: int, status: str) -> Dict:
        """Update task status."""
        tasks_file = self.dashboard_path / "tasks.json"
        
        if not tasks_file.exists():
            return {"error": "No tasks"}
        
        with open(tasks_file, 'r') as f:
            tasks = json.load(f)
        
        for task in tasks:
            if task.get("id") == task_id:
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                break
        
        with open(tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        return {"status": "updated", "task_id": task_id, "new_status": status}
    
    def render_html(self) -> str:
        """Render dashboard HTML."""
        status = self.get_status()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Charles Dashboard</title>
            <style>
                body {{ font-family: -apple-system, sans-serif; background: #000; color: #fff; }}
                .card {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 12px; margin: 10px; }}
                .stat {{ font-size: 32px; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>Charles Dashboard</h1>
            <div class="card">
                <div>Active</div>
                <div class="stat">{status['active']}</div>
            </div>
            <div class="card">
                <div>Pending</div>
                <div class="stat">{status['pending']}</div>
            </div>
            <div class="card">
                <div>Completed</div>
                <div class="stat">{status['completed']}</div>
            </div>
        </body>
        </html>
        """
        return html


SKILL_NAME = "task_dashboard"
SKILL_DESCRIPTION = "Web UI to view all active tasks, status, completion"
