"""
Video processing utilities compatible with capcut-mcp
"""

import subprocess
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

def get_video_info(video_path: str) -> Dict[str, Any]:
    """
    Quick video info extraction using ffprobe
    """
    
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
        audio_stream = next((s for s in data['streams'] if s['codec_type'] == 'audio'), None)
        
        if not video_stream:
            raise Exception("No video stream found")
        
        return {
            'duration': float(data['format']['duration']),
            'width': int(video_stream['width']),
            'height': int(video_stream['height']),
            'fps': eval(video_stream['r_frame_rate']),
            'has_audio': audio_stream is not None,
            'file_size': int(data['format']['size']),
            'format': data['format']['format_name']
        }
        
    except Exception as e:
        raise Exception(f"Failed to get video info: {e}")

def convert_to_capcut_compatible(input_path: str, output_path: str, 
                               target_width: int = 1920, target_height: int = 1080) -> bool:
    """
    Convert video to CapCut-compatible format if needed
    """
    
    # Check if conversion is needed
    info = get_video_info(input_path)
    
    needs_conversion = (
        info['width'] != target_width or 
        info['height'] != target_height or
        not input_path.lower().endswith('.mp4')
    )
    
    if not needs_conversion:
        # Just copy the file
        try:
            import shutil
            shutil.copy2(input_path, output_path)
            return True
        except Exception:
            return False
    
    # Convert using ffmpeg
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'scale={target_width}:{target_height}',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'fast',
        '-y',  # Overwrite output
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Video conversion failed: {e.stderr.decode()}")
        return False

def extract_audio_track(video_path: str, output_path: str) -> bool:
    """
    Extract audio track from video for separate processing
    """
    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vn',  # No video
        '-acodec', 'copy',
        '-y',
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_video_preview(video_path: str, output_path: str, 
                        duration: int = 10, start_time: int = 0) -> bool:
    """
    Create a short preview of the video
    """
    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-ss', str(start_time),
        '-t', str(duration),
        '-c', 'copy',
        '-y',
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_video_thumbnail(video_path: str, output_path: str, 
                       timestamp: Optional[float] = None) -> bool:
    """
    Extract a thumbnail image from video
    """
    
    if timestamp is None:
        # Get thumbnail from 30% into the video
        info = get_video_info(video_path)
        timestamp = info['duration'] * 0.3
    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-ss', str(timestamp),
        '-vframes', '1',
        '-q:v', '2',  # High quality
        '-y',
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def validate_video_integrity(video_path: str) -> Dict[str, Any]:
    """
    Validate video file integrity and provide diagnostic info
    """
    
    result = {
        'is_valid': False,
        'can_read': False,
        'has_video_stream': False,
        'has_audio_stream': False,
        'duration': 0,
        'file_exists': False,
        'file_size': 0,
        'errors': [],
        'warnings': []
    }
    
    # Check if file exists
    if not os.path.exists(video_path):
        result['errors'].append(f"File does not exist: {video_path}")
        return result
    
    result['file_exists'] = True
    result['file_size'] = os.path.getsize(video_path)
    
    # Check if file is empty
    if result['file_size'] == 0:
        result['errors'].append("File is empty")
        return result
    
    try:
        # Try to get basic video info
        info = get_video_info(video_path)
        result['can_read'] = True
        result['has_video_stream'] = True
        result['has_audio_stream'] = info['has_audio']
        result['duration'] = info['duration']
        
        # Additional validation checks
        if info['duration'] <= 0:
            result['errors'].append("Video duration is zero or negative")
        
        if info['width'] <= 0 or info['height'] <= 0:
            result['errors'].append("Invalid video dimensions")
        
        if not result['has_audio_stream']:
            result['warnings'].append("Video has no audio stream")
        
        # Check for common problematic formats
        problematic_formats = ['webm', 'mkv', 'avi']
        if any(fmt in info['format'].lower() for fmt in problematic_formats):
            result['warnings'].append(f"Format '{info['format']}' may need conversion for CapCut compatibility")
        
        # If we got here without errors, the video is valid
        if not result['errors']:
            result['is_valid'] = True
            
    except Exception as e:
        result['errors'].append(f"Failed to read video: {str(e)}")
    
    return result

def batch_process_videos(input_dir: str, output_dir: str, 
                        operation: str = 'convert', **kwargs) -> Dict[str, Any]:
    """
    Process multiple videos in a directory
    
    Args:
        input_dir: Directory containing input videos
        output_dir: Directory for processed videos
        operation: 'convert', 'thumbnail', 'preview', or 'validate'
        **kwargs: Additional arguments for the specific operation
    """
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        return {'error': f"Input directory does not exist: {input_dir}"}
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all video files
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(input_path.glob(f"*{ext}"))
        video_files.extend(input_path.glob(f"*{ext.upper()}"))
    
    results = {
        'total_files': len(video_files),
        'processed': 0,
        'failed': 0,
        'results': []
    }
    
    for video_file in video_files:
        try:
            if operation == 'convert':
                output_file = output_path / f"{video_file.stem}_converted.mp4"
                success = convert_to_capcut_compatible(
                    str(video_file), 
                    str(output_file),
                    **kwargs
                )
                
            elif operation == 'thumbnail':
                output_file = output_path / f"{video_file.stem}_thumb.jpg"
                success = get_video_thumbnail(
                    str(video_file), 
                    str(output_file),
                    **kwargs
                )
                
            elif operation == 'preview':
                output_file = output_path / f"{video_file.stem}_preview.mp4"
                success = create_video_preview(
                    str(video_file), 
                    str(output_file),
                    **kwargs
                )
                
            elif operation == 'validate':
                validation_result = validate_video_integrity(str(video_file))
                success = validation_result['is_valid']
                results['results'].append({
                    'file': video_file.name,
                    'validation': validation_result
                })
                
            else:
                success = False
                
            if success:
                results['processed'] += 1
            else:
                results['failed'] += 1
                
            if operation != 'validate':
                results['results'].append({
                    'file': video_file.name,
                    'success': success,
                    'output': str(output_file) if success else None
                })
                
        except Exception as e:
            results['failed'] += 1
            results['results'].append({
                'file': video_file.name,
                'success': False,
                'error': str(e)
            })
    
    return results

def get_supported_formats() -> Dict[str, List[str]]:
    """
    Return lists of supported input and output formats
    """
    
    return {
        'input_formats': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp'],
        'capcut_preferred': ['.mp4'],
        'audio_formats': ['.mp3', '.wav', '.aac', '.m4a'],
        'image_formats': ['.jpg', '.jpeg', '.png', '.bmp']
    }

def estimate_processing_time(video_path: str, operation: str = 'convert') -> Dict[str, Any]:
    """
    Estimate processing time for video operations
    """
    
    try:
        info = get_video_info(video_path)
        duration = info['duration']
        file_size_mb = info['file_size'] / (1024 * 1024)
        
        # Rough estimates based on typical processing speeds
        estimates = {
            'convert': duration * 0.5,  # Usually faster than real-time
            'thumbnail': 2,  # Quick operation
            'preview': duration * 0.1,  # Copying segments is fast
            'validate': 1  # Very quick
        }
        
        base_time = estimates.get(operation, duration * 0.5)
        
        # Adjust for file size (larger files take longer per second)
        size_factor = max(1.0, file_size_mb / 100)  # Scale up for files > 100MB
        estimated_time = base_time * size_factor
        
        return {
            'operation': operation,
            'estimated_seconds': round(estimated_time, 1),
            'estimated_minutes': round(estimated_time / 60, 1),
            'video_duration': duration,
            'file_size_mb': round(file_size_mb, 1)
        }
        
    except Exception as e:
        return {'error': f"Could not estimate processing time: {e}"}