"""
Configuration Management for CapCut CLI
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess  # Needed for _check_command

class Config:
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self.config_data = {}
        self.load_config()
        self.load_environment_variables()
    
    def load_config(self):
        """Load configuration from JSON file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.config_data = json.load(f)
                print(f"✅ Loaded config from {self.config_path}")
            except json.JSONDecodeError as e:
                print(f"⚠️ Invalid JSON in config file: {e}")
                self.config_data = {}
            except Exception as e:
                print(f"⚠️ Failed to load config: {e}")
                self.config_data = {}
        else:
            print(f"⚠️ Config file not found: {self.config_path}")
            self.create_default_config()
    
    def load_environment_variables(self):
        """Load sensitive data from environment variables"""
        # Load .env file if it exists
        env_path = Path(".env")
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    def create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "capcut_mcp_url": "http://localhost:9000",
            "anthropic_model": "claude-3-sonnet-20240229",
            "output_dir": "output/drafts",
            "temp_dir": "temp",
            "ffmpeg_path": "ffmpeg",
            "ffprobe_path": "ffprobe",
            "capcut_drafts_folder": "",
            "editing_presets": {
                "social_media": {
                    "target_duration": 60,
                    "aspect_ratio": "9:16",
                    "style": "fast_paced",
                    "add_captions": True,
                    "music_volume": 0.3
                },
                "highlight_reel": {
                    "target_duration": 90,
                    "aspect_ratio": "16:9",
                    "style": "dynamic",
                    "add_captions": False,
                    "music_volume": 0.5
                },
                "tutorial": {
                    "target_duration": 300,
                    "aspect_ratio": "16:9",
                    "style": "clean",
                    "add_captions": True,
                    "music_volume": 0.1
                },
                "vlog": {
                    "target_duration": 180,
                    "aspect_ratio": "16:9", 
                    "style": "casual",
                    "add_captions": True,
                    "music_volume": 0.2
                }
            },
            "ai_settings": {
                "max_tokens": 2000,
                "temperature": 0.7,
                "analysis_detail_level": "medium"
            },
            "video_processing": {
                "max_file_size_mb": 500,
                "supported_formats": [".mp4", ".mov", ".avi", ".mkv", ".m4v"],
                "thumbnail_timestamp_ratio": 0.3
            }
        }
        # Create config directory if it doesn't exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        # Save default config
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        self.config_data = default_config
        print(f"✅ Created default config at {self.config_path}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation support"""
        keys = key.split('.')
        value = self.config_data
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value with dot notation support"""
        keys = key.split('.')
        config_ref = self.config_data
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref