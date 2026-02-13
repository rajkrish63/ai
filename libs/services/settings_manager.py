import json
import os
from typing import Dict, Any

class SettingsManager:
    """
    Manages application settings with JSON persistence.
    """
    
    def __init__(self, settings_path: str = "settings.json"):
        self.settings_path = settings_path
        self.settings = self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load settings from file or return defaults."""
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.get_defaults()
        return self.get_defaults()
    
    def save(self) -> None:
        """Save current settings to file."""
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError as e:
            print(f"Failed to save settings: {e}")
    
    def get_defaults(self) -> Dict[str, Any]:
        """Return default settings."""
        return {
            "selected_model": "smollm2-135m",
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.9,
            "max_tokens": 512,
            "theme": "dark"
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a setting value and save."""
        self.settings[key] = value
        self.save()
    
    def reset(self) -> None:
        """Reset all settings to defaults."""
        self.settings = self.get_defaults()
        self.save()
