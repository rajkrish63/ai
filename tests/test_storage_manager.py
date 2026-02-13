"""
Unit tests for StorageManager service.
"""
import unittest
import os
import tempfile
import shutil
from libs.services.storage_manager import StorageManager


class TestStorageManager(unittest.TestCase):
    """Test cases for StorageManager."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.storage_manager = StorageManager(base_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_directories_created(self):
        """Test that directories are created."""
        self.assertTrue(os.path.exists(self.storage_manager.cache_dir))
        self.assertTrue(os.path.exists(self.storage_manager.downloads_dir))
        self.assertTrue(os.path.exists(self.storage_manager.models_dir))
    
    def test_get_storage_info(self):
        """Test getting storage information."""
        info = self.storage_manager.get_storage_info()
        
        self.assertIn("cache", info)
        self.assertIn("models", info)
        self.assertIn("total", info)
        self.assertIsInstance(info["total"], int)
    
    def test_clear_cache(self):
        """Test clearing cache directory."""
        # Create a test file in cache
        test_file = os.path.join(self.storage_manager.cache_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        # Clear cache
        result = self.storage_manager.clear_cache()
        self.assertTrue(result)
        
        # Verify cache is empty
        self.assertEqual(len(os.listdir(self.storage_manager.cache_dir)), 0)
    
    def test_format_size(self):
        """Test size formatting."""
        self.assertEqual(StorageManager.format_size(1024), "1.00 KB")
        self.assertEqual(StorageManager.format_size(1048576), "1.00 MB")
        self.assertEqual(StorageManager.format_size(500), "500.00 B")


if __name__ == '__main__':
    unittest.main()
