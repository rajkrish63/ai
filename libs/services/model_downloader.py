import os
import requests
import hashlib
import threading
from typing import Callable, Optional
from kivy.clock import Clock

class ModelDownloader:
    """
    Handles model downloading with progress tracking and checksum verification.
    """
    
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)
        self.current_download = None
        self.cancel_flag = False
    
    def download(self, url: str, save_path: str, 
                 progress_callback: Optional[Callable[[float], None]] = None,
                 completion_callback: Optional[Callable[[bool, str], None]] = None) -> None:
        """
        Download a file from URL with progress tracking.
        
        Args:
            url: Download URL
            save_path: Where to save the file
            progress_callback: Called with progress percentage (0-100)
            completion_callback: Called with (success, message) when done
        """
        def download_worker():
            try:
                response = requests.get(url, stream=True, timeout=30)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if self.cancel_flag:
                            if completion_callback:
                                Clock.schedule_once(
                                    lambda dt: completion_callback(False, "Download cancelled"), 0
                                )
                            return
                        
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if total_size > 0 and progress_callback:
                                progress = (downloaded / total_size) * 100
                                Clock.schedule_once(
                                    lambda dt, p=progress: progress_callback(p), 0
                                )
                
                if completion_callback:
                    Clock.schedule_once(
                        lambda dt: completion_callback(True, "Download complete"), 0
                    )
                    
            except Exception as e:
                if completion_callback:
                    Clock.schedule_once(
                        lambda dt: completion_callback(False, str(e)), 0
                    )
        
        self.cancel_flag = False
        thread = threading.Thread(target=download_worker, daemon=True)
        thread.start()
        self.current_download = thread
    
    def cancel_download(self) -> None:
        """Cancel the current download."""
        self.cancel_flag = True
    
    @staticmethod
    def verify_checksum(file_path: str, expected_sha256: str) -> bool:
        """
        Verify file integrity using SHA-256 checksum.
        
        Args:
            file_path: Path to file
            expected_sha256: Expected SHA-256 hash
            
        Returns:
            True if checksum matches, False otherwise
        """
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest() == expected_sha256
        except Exception as e:
            print(f"Checksum verification failed: {e}")
            return False
    
    @staticmethod
    def extract_archive(archive_path: str, destination: str) -> bool:
        """
        Extract a tar.gz archive.
        
        Args:
            archive_path: Path to archive file
            destination: Destination directory
            
        Returns:
            True if extraction succeeded, False otherwise
        """
        import tarfile
        try:
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(destination)
            return True
        except Exception as e:
            print(f"Extraction failed: {e}")
            return False
