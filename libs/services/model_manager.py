import os
import json
from typing import List, Dict, Optional

class ModelManager:
    """
    Manages AI model metadata, listing, and selection.
    """
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        os.makedirs(self.models_dir, exist_ok=True)
    
    def list_available_models(self) -> List[Dict]:
        """
        Get list of models available for download.
        Returns mock data for now - will be replaced with actual model registry.
        """
        return [
            {
                "id": "smollm2-135m",
                "name": "SmolLM2-135M",
                "description": "Lightweight, fast, good for general chat",
                "size_mb": 95,
                "min_ram_gb": 2,
                "accuracy": "moderate",
                "speed": "fast",
                "download_url": "https://example.com/smollm2-135m.tar.gz",
                "sha256": "a1b2c3d4e5f6..."
            },
            {
                "id": "smollm2-360m",
                "name": "SmolLM2-360M",
                "description": "Balanced performance and accuracy",
                "size_mb": 250,
                "min_ram_gb": 3,
                "accuracy": "good",
                "speed": "medium",
                "download_url": "https://example.com/smollm2-360m.tar.gz",
                "sha256": "b2c3d4e5f6a7..."
            },
            {
                "id": "gemma-1b-instruct",
                "name": "Gemma-1B-Instruct",
                "description": "High accuracy for complex tasks",
                "size_mb": 650,
                "min_ram_gb": 4,
                "accuracy": "high",
                "speed": "slow",
                "download_url": "https://example.com/gemma-1b.tar.gz",
                "sha256": "c3d4e5f6a7b8..."
            }
        ]
    
    def list_installed_models(self) -> List[Dict]:
        """Get list of locally installed models."""
        installed = []
        if os.path.exists(self.models_dir):
            for model_dir in os.listdir(self.models_dir):
                model_path = os.path.join(self.models_dir, model_dir)
                if os.path.isdir(model_path):
                    manifest_path = os.path.join(model_path, "manifest.json")
                    if os.path.exists(manifest_path):
                        try:
                            with open(manifest_path, 'r') as f:
                                manifest = json.load(f)
                                installed.append({
                                    "id": model_dir,
                                    "name": manifest.get("name", model_dir),
                                    "path": model_path,
                                    **manifest
                                })
                        except Exception as e:
                            print(f"Failed to load manifest for {model_dir}: {e}")
        return installed
    
    def get_model_info(self, model_id: str) -> Optional[Dict]:
        """Get information about a specific model."""
        # Check installed models first
        for model in self.list_installed_models():
            if model["id"] == model_id:
                return model
        
        # Check available models
        for model in self.list_available_models():
            if model["id"] == model_id:
                return model
        
        return None
    
    def is_model_downloaded(self, model_id: str) -> bool:
        """Check if a model is downloaded and ready to use."""
        model_path = os.path.join(self.models_dir, model_id)
        if not os.path.exists(model_path):
            return False
        
        # Check for required files
        required_files = ["model_int8.onnx", "tokenizer.json", "config.json"]
        for file in required_files:
            if not os.path.exists(os.path.join(model_path, file)):
                return False
        
        return True
    
    def get_model_path(self, model_id: str) -> Optional[str]:
        """Get the path to a model's directory."""
        model_path = os.path.join(self.models_dir, model_id)
        if self.is_model_downloaded(model_id):
            return model_path
        return None
    
    def delete_model(self, model_id: str) -> bool:
        """Delete a downloaded model."""
        import shutil
        model_path = os.path.join(self.models_dir, model_id)
        if os.path.exists(model_path):
            try:
                shutil.rmtree(model_path)
                return True
            except Exception as e:
                print(f"Failed to delete model: {e}")
                return False
        return False
    
    def create_manifest(self, model_id: str, metadata: Dict) -> bool:
        """Create a manifest file for a model."""
        model_path = os.path.join(self.models_dir, model_id)
        os.makedirs(model_path, exist_ok=True)
        
        manifest_path = os.path.join(model_path, "manifest.json")
        try:
            with open(manifest_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to create manifest: {e}")
            return False
