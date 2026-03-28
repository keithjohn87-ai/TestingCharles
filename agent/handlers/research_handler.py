"""
Research Handler
"""

import skills

class ResearchHandler:
    @staticmethod
    def handle_research(message: str) -> str:
        if "research:" in message.lower():
            topic = message.split("research:", 1)[1].strip()
            result = skills.research.research(topic)
            return f"Research complete: {topic}"
        return "Could not parse research request"
