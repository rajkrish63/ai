"""
Unit tests for ChatManager service.
"""
import unittest
import os
import json
import tempfile
import shutil
from libs.services.chat_manager import ChatManager


class TestChatManager(unittest.TestCase):
    """Test cases for ChatManager."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.chat_manager = ChatManager(history_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_create_chat(self):
        """Test creating a new chat."""
        chat_id = self.chat_manager.create_chat(model="test-model")
        self.assertIsNotNone(chat_id)
        self.assertTrue(chat_id.startswith("chat_"))
        
        # Verify chat file exists
        chat_file = os.path.join(self.test_dir, f"{chat_id}.json")
        self.assertTrue(os.path.exists(chat_file))
    
    def test_add_message(self):
        """Test adding messages to a chat."""
        chat_id = self.chat_manager.create_chat()
        
        # Add user message
        self.chat_manager.add_message(chat_id, "user", "Hello, AI!")
        
        # Add assistant message
        self.chat_manager.add_message(chat_id, "assistant", "Hello! How can I help?")
        
        # Load and verify
        chat_data = self.chat_manager.load_chat(chat_id)
        self.assertEqual(len(chat_data["messages"]), 2)
        self.assertEqual(chat_data["messages"][0]["role"], "user")
        self.assertEqual(chat_data["messages"][1]["role"], "assistant")
    
    def test_load_chat(self):
        """Test loading a chat."""
        chat_id = self.chat_manager.create_chat()
        self.chat_manager.add_message(chat_id, "user", "Test message")
        
        loaded_chat = self.chat_manager.load_chat(chat_id)
        self.assertIsNotNone(loaded_chat)
        self.assertEqual(loaded_chat["id"], chat_id)
        self.assertEqual(len(loaded_chat["messages"]), 1)
    
    def test_list_chats(self):
        """Test listing all chats."""
        # Create multiple chats
        chat1 = self.chat_manager.create_chat()
        chat2 = self.chat_manager.create_chat()
        
        chats = self.chat_manager.list_chats()
        self.assertEqual(len(chats), 2)
    
    def test_delete_chat(self):
        """Test deleting a chat."""
        chat_id = self.chat_manager.create_chat()
        self.assertTrue(self.chat_manager.delete_chat(chat_id))
        
        # Verify deletion
        chat_file = os.path.join(self.test_dir, f"{chat_id}.json")
        self.assertFalse(os.path.exists(chat_file))
    
    def test_export_chat(self):
        """Test exporting a chat."""
        chat_id = self.chat_manager.create_chat()
        self.chat_manager.add_message(chat_id, "user", "Export test")
        
        export_path = os.path.join(self.test_dir, "exported_chat.json")
        result = self.chat_manager.export_chat(chat_id, export_path)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(export_path))


if __name__ == '__main__':
    unittest.main()
