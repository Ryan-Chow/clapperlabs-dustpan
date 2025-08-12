"""
File utilities for CapCut CLI
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from typing import List, Dict

def validate_video_file(file_path: str) -> bool:
    """Validate that a file is a supported video format"""
    
    if not os.path.exists(file_path):
        return False
    
    supported_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.m4v', '.wmv', '.flv', '.webm']
    file_ext = Path(file_path).suffix.lower()
    
    return file_ext in supported_extensions

def ensure_output_dir(directory: str) -> str:
    """Ensure output directory exists and return the path"""
    
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return str(path)

def generate_unique_name(base_name: str) -> str:
    """Generate a unique name based on timestamp and base name"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}"

def get_file_hash(file_path: str) -> str:
    """Get MD5 hash of a file for deduplication"""
    
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return ""

def copy_file_safely(src: str, dst: str) -> bool:
    """Copy file with error handling"""
    
    try:
        # Ensure destination directory exists
        Path(dst).parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"⚠️ Failed to copy {src} to {dst}: {e}")
        return False

def clean_temp_files(temp_dir: str, max_age_hours: int = 24):
    """Clean up temporary files older than specified hours"""
    
    if not Path(temp_dir).exists():
        return
    
    import time
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for file_path in Path(temp_dir).rglob('*'):
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                except Exception:
                    pass

def find_videos_in_directory(directory: str, recursive: bool = False) -> List[str]:
    """Find all video files in a directory"""
    
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.m4v', '.wmv', '.flv', '.webm']
    video_files = []
    
    search_path = Path(directory)
    
    if recursive:
        pattern = '**/*'
    else:
        pattern = '*'
    
    for file_path in search_path.glob(pattern):
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            video_files.append(str(file_path))
    
    return sorted(video_files)

def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes"""
    
    try:
        size_bytes = Path(file_path).stat().st_size
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0

def validate_capcut_draft_structure(draft_path: str) -> bool:
    """Validate that a directory has the correct CapCut draft structure"""
    
    draft_dir = Path(draft_path)
    if not draft_dir.exists() or not draft_dir.is_dir():
        return False
    
    # Check for required CapCut files (basic validation)
    required_files = ['draft_content.json', 'draft_meta_info.json']
    
    for required_file in required_files:
        if not (draft_dir / required_file).exists():
            return False
    
    return True

def backup_draft(draft_path: str, backup_dir: str = "backups") -> Optional[str]:
    """Create a backup of a CapCut draft"""
    
    if not validate_capcut_draft_structure(draft_path):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    draft_name = Path(draft_path).name
    backup_name = f"{draft_name}_backup_{timestamp}"
    backup_path = Path(backup_dir) / backup_name
    
    try:
        shutil.copytree(draft_path, backup_path)
        return str(backup_path)
    except Exception as e:
        print(f"⚠️ Backup failed: {e}")
        return None

def organize_output_files(output_dir: str):
    """Organize output files by date and type"""
    
    output_path = Path(output_dir)
    if not output_path.exists():
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    organized_dir = output_path / "organized" / today
    organized_dir.mkdir(parents=True, exist_ok=True)
    
    # Move draft folders to organized directory
    for item in output_path.iterdir():
        if item.is_dir() and item.name.startswith('dfd_') and item.parent.name != "organized":
            try:
                destination = organized_dir / item.name
                if not destination.exists():
                    shutil.move(str(item), str(destination))
            except Exception as e:
                print(f"⚠️ Failed to organize {item.name}: {e}")

class FileManager:
    """Helper class for managing files throughout the editing process"""
    
    def __init__(self, config):
        self.config = config
        self.temp_dir = Path(config.temp_dir)
        self.output_dir = Path(config.output_dir)
        
        # Ensure directories exist
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def prepare_video_for_editing(self, video_path: str) -> str:
        """Prepare video file for editing (copy to temp if needed)"""
        
        video_file = Path(video_path)
        
        # If file is already in a good location, return as-is
        if video_file.exists() and self._is_accessible(video_path):
            return str(video_file.absolute())
        
        # Copy to temp directory with unique name
        temp_name = f"{generate_unique_name(video_file.stem)}{video_file.suffix}"
        temp_path = self.temp_dir / temp_name
        
        if copy_file_safely(video_path, str(temp_path)):
            return str(temp_path)
        else:
            raise Exception(f"Failed to prepare video file: {video_path}")
    
    def _is_accessible(self, file_path: str) -> bool:
        """Check if file is accessible and not locked"""
        
        try:
            with open(file_path, 'rb') as f:
                f.read(1024)  # Try to read a small portion
            return True
        except Exception:
            return False
    
    def cleanup_temp_files(self):
        """Clean up temporary files created during editing"""
        
        clean_temp_files(str(self.temp_dir))
    
    def get_output_path(self, name: str) -> str:
        """Get full output path for a draft"""
        
        return str(self.output_dir / f"dfd_{name}")
    
    def list_recent_drafts(self, limit: int = 10) -> List[Dict[str, str]]:
        """List recent draft outputs"""
        
        drafts = []
        
        for draft_dir in self.output_dir.glob('dfd_*'):
            if draft_dir.is_dir():
                stat = draft_dir.stat()
                drafts.append({
                    'name': draft_dir.name,
                    'path': str(draft_dir),
                    'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M'),
                    'size_mb': sum(f.stat().st_size for f in draft_dir.rglob('*') if f.is_file()) / (1024*1024)
                })
        
        # Sort by creation time, newest first
        drafts.sort(key=lambda x: x['created'], reverse=True)
        
        return drafts[:limit]