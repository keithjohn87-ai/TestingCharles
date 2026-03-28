"""
Code Handler
"""

import skills

class CodeHandler:
    @staticmethod
    def handle_write_code(message: str) -> str:
        if "write code" in message.lower() and "to " in message:
            parts = message.split("to ", 1)
            if len(parts) > 1:
                file_part = parts[1].split(":")[0].strip()
                content = parts[1].split(":", 1)[1].strip() if ":" in parts[1] else ""
                result = skills.coder.write_code(file_part, content)
                return f"✓ Written to {file_part}"
        return "Could not parse code request"

    @staticmethod
    def handle_execute(message: str) -> str:
        if "execute:" in message.lower():
            cmd = message.split("execute:", 1)[1].strip()
            result = skills.coder.execute_command(cmd)
            return result.get("stdout", result.get("error", "Done"))
        return "Could not parse execute request"
