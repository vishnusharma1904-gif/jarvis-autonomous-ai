"""
Enhanced Memory System with Session Management
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class MemoryManager:
    """Enhanced conversation memory with persistence"""
    
    def __init__(self, data_dir: str = "backend/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_file = self.data_dir / "sessions.json"
        self.sessions = self._load_sessions()
    
    def _load_sessions(self) -> Dict:
        """Load sessions from file"""
        if self.sessions_file.exists():
            try:
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_sessions(self):
        """Save sessions to file"""
        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(self.sessions, f, indent=2, ensure_ascii=False)
    
    def create_session(self, title: str = "New Chat") -> str:
        """Create new conversation session"""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        
        self.sessions[session_id] = {
            "id": session_id,
            "title": title,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": []
        }
        
        self._save_sessions()
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def list_sessions(self) -> List[Dict]:
        """List all sessions"""
        sessions_list = list(self.sessions.values())
        # Sort by updated_at, most recent first
        sessions_list.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return sessions_list
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self._save_sessions()
            return True
        return False
    
    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Add message to session"""
        if session_id not in self.sessions:
            return False
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        if metadata:
            message["metadata"] = metadata
        
        self.sessions[session_id]["messages"].append(message)
        self.sessions[session_id]["updated_at"] = datetime.now().isoformat()
        
        # Update title if first message
        if len(self.sessions[session_id]["messages"]) == 1:
            # Use first 50 chars of first message as title
            title = content[:50] + "..." if len(content) > 50 else content
            self.sessions[session_id]["title"] = title
        
        self._save_sessions()
        return True
    
    def get_messages(self, session_id: str) -> List[Dict]:
        """Get all messages from session"""
        session = self.get_session(session_id)
        if session:
            return session.get("messages", [])
        return []
    
    def get_conversation_history(
        self,
        session_id: str,
        max_messages: int = 20
    ) -> List[Dict]:
        """
        Get conversation history formatted for LLM
        
        Args:
            session_id: Session ID
            max_messages: Maximum number of messages to return
        
        Returns:
            List of messages in LLM format
        """
        messages = self.get_messages(session_id)
        
        # Take only last max_messages
        if len(messages) > max_messages:
            messages = messages[-max_messages:]
        
        # Format for LLM
        formatted = []
        for msg in messages:
            formatted.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return formatted
    
    def search_messages(self, query: str) -> List[Dict]:
        """Search messages across all sessions"""
        results = []
        query_lower = query.lower()
        
        for session in self.sessions.values():
            for message in session.get("messages", []):
                if query_lower in message.get("content", "").lower():
                    results.append({
                        "session_id": session["id"],
                        "session_title": session.get("title", "Untitled"),
                        "message": message
                    })
        
        return results
    
    def clear_all_sessions(self):
        """Clear all sessions (use with caution)"""
        self.sessions = {}
        self._save_sessions()

    # ==================== Long-term Memory (RAG) ====================

    def store_long_term_memory(self, text: str) -> str:
        """Store a fact or memory in the vector database"""
        from core.rag import rag_system
        if not rag_system.enabled:
            return "Memory system disabled (RAG not active)"
            
        try:
            # Add to RAG with metadata
            doc_id = rag_system.add_document(
                text, 
                metadata={
                    "type": "memory", 
                    "timestamp": datetime.now().isoformat()
                }
            )
            return f"Memory stored successfully (ID: {doc_id})"
        except Exception as e:
            return f"Failed to store memory: {e}"

    def search_memories(self, query: str, limit: int = 3) -> List[str]:
        """Search long-term memories"""
        from core.rag import rag_system
        if not rag_system.enabled:
            return []
            
        try:
            results = rag_system.search(query, n_results=limit)
            memories = [res["content"] for res in results]
            return memories
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []

# Global instance
memory_manager = MemoryManager()
