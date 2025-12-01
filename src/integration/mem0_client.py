"""
Mem0 Client for GSW
===================

Handles persistent memory operations using Mem0.
"""

import os
from typing import Dict, Any, List, Optional
from mem0 import MemoryClient

class GSWMemory:
    """Wrapper around Mem0 MemoryClient."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MEM0_API_KEY")
        if not self.api_key:
            print("[Warning] MEM0_API_KEY not set. Memory features will be disabled.")
            self.client = None
        else:
            self.client = MemoryClient(api_key=self.api_key)

    def add_memory(self, text: str, user_id: str, metadata: Optional[Dict] = None) -> Dict:
        """Add a memory."""
        if not self.client:
            return {}
        
        try:
            return self.client.add(text, user_id=user_id, metadata=metadata or {})
        except Exception as e:
            print(f"[Mem0] Add failed: {e}")
            return {}

    def search_memory(self, query: str, user_id: str, limit: int = 5) -> List[Dict]:
        """Search memories."""
        if not self.client:
            return []
            
        try:
            return self.client.search(query, user_id=user_id, limit=limit)
        except Exception as e:
            print(f"[Mem0] Search failed: {e}")
            return []

    def get_all_memories(self, user_id: str) -> List[Dict]:
        """Get all memories for a user."""
        if not self.client:
            return []
            
        try:
            return self.client.get_all(user_id=user_id)
        except Exception as e:
            print(f"[Mem0] Get all failed: {e}")
            return []

# Global instance
_memory = None

def get_memory_client() -> GSWMemory:
    global _memory
    if _memory is None:
        _memory = GSWMemory()
    return _memory

