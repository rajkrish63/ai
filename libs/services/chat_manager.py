import json
import os
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChatManager:
    """
    Manages chat history storage and retrieval.
    """
    
    def __init__(self, history_dir: str = "chat_history"):
        self.history_dir = history_dir
        os.makedirs(self.history_dir, exist_ok=True)
    
    def create_chat(self, model: str = "unknown") -> str:
        """Create a new chat session and return its ID."""
        chat_id = f"chat_{int(time.time() * 1000)}"
        chat_data = {
            "id": chat_id,
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "messages": []
        }
        self._save_chat(chat_id, chat_data)
        return chat_id
    
    def add_message(self, chat_id: str, role: str, content: str) -> None:
        """Add a message to a chat."""
        chat_data = self.load_chat(chat_id)
        if chat_data:
            chat_data["messages"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            self._save_chat(chat_id, chat_data)
    
    def load_chat(self, chat_id: str) -> Optional[Dict[str, Any]]:
        """Load a chat by ID."""
        path = os.path.join(self.history_dir, f"{chat_id}.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        return None
    
    def list_chats(self) -> List[Dict[str, Any]]:
        """List all chat sessions."""
        chats = []
        if os.path.exists(self.history_dir):
            for filename in os.listdir(self.history_dir):
                if filename.endswith('.json'):
                    chat_id = filename[:-5]  # Remove .json
                    chat_data = self.load_chat(chat_id)
                    if chat_data:
                        chats.append({
                            "id": chat_data["id"],
                            "timestamp": chat_data["timestamp"],
                            "model": chat_data.get("model", "unknown"),
                            "message_count": len(chat_data["messages"])
                        })
        return sorted(chats, key=lambda x: x["timestamp"], reverse=True)
    
    def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat session."""
        path = os.path.join(self.history_dir, f"{chat_id}.json")
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except OSError:
                return False
        return False
    
    def _save_chat(self, chat_id: str, chat_data: Dict[str, Any]) -> None:
        """Save chat data to file."""
        path = os.path.join(self.history_dir, f"{chat_id}.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Failed to save chat: {e}")
    
    def export_chat(self, chat_id: str, export_path: str) -> bool:
        """Export a chat to a specified path."""
        chat_data = self.load_chat(chat_id)
        if chat_data:
            try:
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(chat_data, f, indent=2, ensure_ascii=False)
                return True
            except IOError:
                return False
        return False
