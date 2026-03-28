"""
Tool Executor
=============

Executes tools based on user requests.
"""

import skills


class ToolExecutor:
    """Execute tools based on request type."""
    
    @staticmethod
    def execute(request: str) -> str:
        """Route request to appropriate tool."""
        request_lower = request.lower()
        
        # Code tools
        if "write code" in request_lower:
            from .handlers import CodeHandler
            return CodeHandler.handle_write_code(request)
        
        if "execute:" in request_lower:
            from .handlers import CodeHandler
            return CodeHandler.handle_execute(request)
        
        # Research tools
        if "research:" in request_lower:
            from .handlers import ResearchHandler
            return ResearchHandler.handle_research(request)
        
        # Task tools
        if "task:" in request_lower:
            from .handlers import TaskHandler
            return TaskHandler.handle_create_task(request)
        
        if "list tasks" in request_lower:
            from .handlers import TaskHandler
            return TaskHandler.handle_list_tasks(request)
        
        # No match
        return None


__all__ = ["ToolExecutor"]
