import os
import shutil
from typing import Dict

class StorageManager:
    """
    Manages file storage, cleanup, and storage information.
    """
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.cache_dir = os.path.join(base_dir, "cache")
        self.downloads_dir = os.path.join(base_dir, "downloads")
        self.models_dir = os.path.join(base_dir, "models")
        self.rag_dir = os.path.join(base_dir, "rag")
        self.chat_history_dir = os.path.join(base_dir, "chat_history")
        
        # Ensure directories exist
        for dir_path in [self.cache_dir, self.downloads_dir, 
                        self.models_dir, self.rag_dir, self.chat_history_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def get_storage_info(self) -> Dict[str, int]:
        """Get storage usage for each directory in bytes."""
        return {
            "cache": self._get_dir_size(self.cache_dir),
            "downloads": self._get_dir_size(self.downloads_dir),
            "models": self._get_dir_size(self.models_dir),
            "rag": self._get_dir_size(self.rag_dir),
            "chat_history": self._get_dir_size(self.chat_history_dir),
            "total": sum([
                self._get_dir_size(self.cache_dir),
                self._get_dir_size(self.downloads_dir),
                self._get_dir_size(self.models_dir),
                self._get_dir_size(self.rag_dir),
                self._get_dir_size(self.chat_history_dir)
            ])
        }
    
    def clear_cache(self) -> bool:
        """Clear the cache directory."""
        try:
            if os.path.exists(self.cache_dir):
                shutil.rmtree(self.cache_dir)
                os.makedirs(self.cache_dir)
            return True
        except Exception as e:
            print(f"Failed to clear cache: {e}")
            return False
    
    def clear_downloads(self) -> bool:
        """Clear the downloads directory."""
        try:
            if os.path.exists(self.downloads_dir):
                shutil.rmtree(self.downloads_dir)
                os.makedirs(self.downloads_dir)
            return True
        except Exception as e:
            print(f"Failed to clear downloads: {e}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a specific file."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Failed to delete file: {e}")
            return False
    
    def _get_dir_size(self, path: str) -> int:
        """Get total size of a directory in bytes."""
        total = 0
        try:
            if os.path.exists(path):
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        if os.path.exists(filepath):
                            total += os.path.getsize(filepath)
        except Exception as e:
            print(f"Error calculating directory size: {e}")
        return total
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
