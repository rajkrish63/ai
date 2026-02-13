"""
Unit tests for SettingsManager service.
"""
import unittest
import os
import tempfile
import shutil
from libs.services.settings_manager import SettingsManager


class TestSettingsManager(unittest.TestCase):
    """Test cases for SettingsManager."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.settings_file = os.path.join(self.test_dir, "test_settings.json")
        self.settings_manager = SettingsManager(settings_path=self.settings_file)
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_load_defaults(self):
        """Test loading default settings."""
        defaults = self.settings_manager.get_defaults()
        self.assertIn("selected_model", defaults)
        self.assertIn("temperature", defaults)
        self.assertIn("theme", defaults)
    
    def test_get_setting(self):
        """Test getting a setting value."""
        temperature = self.settings_manager.get("temperature")
        self.assertEqual(temperature, 0.7)
    
    def test_set_setting(self):
        """Test setting a value."""
        self.settings_manager.set("temperature", 0.9)
        self.assertEqual(self.settings_manager.get("temperature"), 0.9)
        
        # Verify persistence
        new_manager = SettingsManager(settings_path=self.settings_file)
        self.assertEqual(new_manager.get("temperature"), 0.9)
    
    def test_reset_settings(self):
        """Test resetting to defaults."""
        self.settings_manager.set("temperature", 0.5)
        self.settings_manager.reset()
        
        self.assertEqual(self.settings_manager.get("temperature"), 0.7)


if __name__ == '__main__':
    unittest.main()
