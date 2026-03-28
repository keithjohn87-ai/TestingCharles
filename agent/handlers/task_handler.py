"""
Task Handler
"""

import skills

class TaskHandler:
    @staticmethod
    def handle_create_task(message: str) -> str:
        if "task:" in message.lower():
            task_name = message.split("task:", 1)[1].strip()
            task = skills.orchestrator.create_task(task_name, "john")
            return f"✓ Created task: {task.name} (ID: {task.id})"
        return "Could not parse task request"
    
    @staticmethod
    def handle_list_tasks(message: str) -> str:
        queue = skills.orchestrator.get_queue_status()
        return f"Tasks: {queue['in_progress']} active, {queue['pending']} pending"
