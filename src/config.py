"""
Configuration Management for CapCut CLI
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

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
            config_ref = config_ref[k]
        
        # Set the final value
        config_ref[keys[-1]] = value
    
    def save(self):
        """Save current configuration to file"""
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=2)
            print(f"✅ Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
    
    def get_editing_preset(self, style: str) -> Dict[str, Any]:
        """Get editing preset for a specific style"""
        
        presets = self.get('editing_presets', {})
        return presets.get(style, presets.get('social_media', {}))
    
    def get_capcut_drafts_folder(self) -> str:
        """Get CapCut drafts folder path"""
        
        configured_path = self.get('capcut_drafts_folder')
        if configured_path and Path(configured_path).exists():
            return configured_path
        
        # Try to auto-detect CapCut drafts folder
        possible_paths = [
            # Windows
            os.path.expanduser('~/AppData/Local/CapCut/User Data/Projects'),
            os.path.expanduser('~/Documents/CapCut'),
            # macOS
            os.path.expanduser('~/Library/Containers/com.lemon.lvoverseas/Data/Library/Application Support/CapCut/Projects'),
            os.path.expanduser('~/Movies/CapCut'),
            # Linux (if CapCut runs via Wine or AppImage)
            os.path.expanduser('~/.capcut/projects'),
            # Generic fallback
            os.path.expanduser('~/Videos/CapCut')
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                self.set('capcut_drafts_folder', path)
                self.save()
                return path
        
        # Return default if none found
        return os.path.expanduser('~/Videos/CapCut')
    
    @property
    def output_dir(self) -> str:
        """Get output directory path"""
        return self.get('output_dir', 'output/drafts')
    
    @property
    def temp_dir(self) -> str:
        """Get temporary directory path"""
        return self.get('temp_dir', 'temp')
    
    def validate_setup(self) -> Dict[str, bool]:
        """Validate that all required dependencies and paths are available"""
        
        validation = {
            'ffmpeg': self._check_command('ffmpeg'),
            'ffprobe': self._check_command('ffprobe'),
            'anthropic_api_key': bool(os.getenv('ANTHROPIC_API_KEY')),
            'capcut_mcp_available': Path('capcut-mcp').exists(),
            'output_dir_writable': self._check_writable(self.output_dir)
        }
        
        return validation
    
    def _check_command(self, command: str) -> bool:
        """Check if a command is available in PATH"""
        
        try:
            subprocess.run([command, '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _check_writable(self, directory: str) -> bool:
        """Check if directory is writable"""
        
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            test_file = Path(directory) / '.test_write'
            test_file.touch()
            test_file.unlink()
            return True
        except Exception:
            return False