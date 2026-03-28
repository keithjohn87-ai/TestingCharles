"""
CHARLES LOCAL MEMORY SYSTEM
===========================
Self-persisting memory for Charles.
Remembers facts, preferences, and conversation context.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class CharlesMemory:
    """Charles's local memory - remembers everything."""
    
    def __init__(self, memory_path: str = None):
        if memory_path is None:
            # Default to user's home directory for portability
            memory_path = os.path.expanduser("~/Charles5.0_AIBot/memory")
        
        self.memory_path = memory_path
        os.makedirs(memory_path, exist_ok=True)
        
        self.memory_file = os.path.join(memory_path, "memory.json")
        self.conversations_file = os.path.join(memory_path, "conversations.json")
        
        # Load existing memory or create new
        self.memory = self._load_memory()
        self.conversations = self._load_conversations()
        
        print(f"🧠 Charles memory loaded: {len(self.memory.get('facts', []))} facts, {len(self.conversations)} messages")
    
    def _load_memory(self) -> Dict:
        """Load long-term memory."""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {
            "facts": [],
            "preferences": {},
            "context": {},
            "important": []
        }
    
    def _save_memory(self):
        """Save long-term memory."""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def _load_conversations(self) -> List[Dict]:
        """Load conversation history."""
        if os.path.exists(self.conversations_file):
            with open(self.conversations_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_conversations(self):
        """Save conversation history."""
        with open(self.conversations_file, 'w') as f:
            json.dump(self.conversations, f, indent=2)
    
    def remember(self, key: str, value: Any, important: bool = False):
        """Remember a fact or piece of information."""
        # Check if already exists
        for fact in self.memory["facts"]:
            if fact["key"] == key:
                fact["value"] = value
                fact["updated"] = datetime.now().isoformat()
                self._save_memory()
                return
        
        # Add new fact
        self.memory["facts"].append({
            "key": key,
            "value": value,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        })
        
        if important:
            self.memory["important"].append(key)
        
        self._save_memory()
        print(f"🧠 Remembered: {key}")
    
    def recall(self, key: str) -> Any:
        """Recall a remembered fact."""
        for fact in self.memory["facts"]:
            if fact["key"] == key:
                return fact["value"]
        return None
    
    def all_facts(self) -> List[Dict]:
        """Recall all remembered facts."""
        return self.memory["facts"]
    
    def set_preference(self, key: str, value: Any):
        """Remember a user preference."""
        self.memory["preferences"][key] = value
        self._save_memory()
        print(f"🧠 Preference set: {key} = {value}")
    
    def get_preference(self, key: str) -> Any:
        """Get a user preference."""
        return self.memory["preferences"].get(key)
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        # role = "user" or "charles"
        self.conversations.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 100 messages
        if len(self.conversations) > 100:
            self.conversations = self.conversations[-100:]
        
        self._save_conversations()
    
    def get_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation context."""
        return self.conversations[-limit:]
    
    def search_memory(self, query: str) -> List[Dict]:
        """Search memory for a query."""
        results = []
        query_lower = query.lower()
        
        for fact in self.memory["facts"]:
            if query_lower in fact["key"].lower() or query_lower in str(fact["value"]).lower():
                results.append(fact)
        
        return results
    
    def get_important(self) -> List[Dict]:
        """Get all important things to remember."""
        important = []
        for fact in self.memory["facts"]:
            if fact["key"] in self.memory["important"]:
                important.append(fact)
        return important


# Global memory instance
_memory = None

def get_memory() -> CharlesMemory:
    """Get the global memory instance."""
    global _memory
    if _memory is None:
        _memory = CharlesMemory()
    return _memory
