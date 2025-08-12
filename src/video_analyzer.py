"""
Video Analyzer - Extract video information and content analysis
Fixed version with proper JSON serialization for numpy types
"""

import subprocess
import json
import os
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV not available. Install with: pip install opencv-python")


def convert_numpy_types(obj):
    """
    Recursively convert numpy types to native Python types for JSON serialization
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_numpy_types(item) for item in obj)
    else:
        return obj


class VideoAnalyzer:
    def __init__(self, config):
        self.config = config
        self.ffmpeg_path = config.get('ffmpeg_path', 'ffmpeg')
        self.ffprobe_path = config.get('ffprobe_path', 'ffprobe')
    
    def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """
        Comprehensive video analysis using ffprobe and optional CV2
        """
        
        try:
            # Get basic video info with ffprobe
            basic_info = self._get_video_info_ffprobe(video_path)
            
            # Enhanced analysis with OpenCV if available
            if CV2_AVAILABLE:
                enhanced_info = self._analyze_with_opencv(video_path)
                basic_info.update(enhanced_info)
            
            # Content analysis
            content_analysis = self._analyze_content_patterns(video_path, basic_info)
            basic_info.update(content_analysis)
            
            # Convert all numpy types to native Python types
            return convert_numpy_types(basic_info)
            
        except Exception as e:
            raise Exception(f"Video analysis failed: {e}")
    
    def _get_video_info_ffprobe(self, video_path: str) -> Dict[str, Any]:
        """
        Extract video metadata using ffprobe
        """
        
        cmd = [
            self.ffprobe_path,
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            probe_data = json.loads(result.stdout)
            
            # Extract video stream info
            video_stream = None
            audio_stream = None
            
            for stream in probe_data['streams']:
                if stream['codec_type'] == 'video' and not video_stream:
                    video_stream = stream
                elif stream['codec_type'] == 'audio' and not audio_stream:
                    audio_stream = stream
            
            if not video_stream:
                raise Exception("No video stream found")
            
            # Parse video info - ensure all values are native Python types
            info = {
                'duration': float(probe_data['format']['duration']),
                'width': int(video_stream['width']),
                'height': int(video_stream['height']),
                'fps': float(eval(video_stream['r_frame_rate'])),  # Convert fraction to float
                'codec': video_stream['codec_name'],
                'bitrate': int(probe_data['format'].get('bit_rate', 0)),
                'file_size': int(probe_data['format']['size']),
                'format': probe_data['format']['format_name']
            }
            
            # Audio info
            if audio_stream:
                info.update({
                    'has_audio': True,
                    'audio_codec': audio_stream['codec_name'],
                    'audio_channels': int(audio_stream.get('channels', 0)),
                    'sample_rate': int(audio_stream.get('sample_rate', 0))
                })
            else:
                info['has_audio'] = False
            
            # Calculate aspect ratio
            aspect_ratio = info['width'] / info['height']
            if abs(aspect_ratio - 16/9) < 0.1:
                info['aspect_ratio'] = '16:9'
            elif abs(aspect_ratio - 9/16) < 0.1:
                info['aspect_ratio'] = '9:16'
            elif abs(aspect_ratio - 1) < 0.1:
                info['aspect_ratio'] = '1:1'
            elif abs(aspect_ratio - 4/3) < 0.1:
                info['aspect_ratio'] = '4:3'
            else:
                info['aspect_ratio'] = f'{info["width"]}:{info["height"]}'
            
            return info
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"ffprobe failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse ffprobe output: {e}")
    
    def _analyze_with_opencv(self, video_path: str) -> Dict[str, Any]:
        """
        Enhanced analysis using OpenCV for content detection
        """
        
        if not CV2_AVAILABLE:
            return {}
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return {}
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = float(cap.get(cv2.CAP_PROP_FPS))  # Convert to native float
            
            # Sample frames for analysis
            sample_frames = []
            sample_intervals = max(1, frame_count // 10)  # Sample 10 frames
            
            for i in range(0, frame_count, sample_intervals):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret:
                    sample_frames.append((float(i / fps), frame))  # Ensure timestamp is native float
            
            cap.release()
            
            # Analyze sampled frames
            analysis = {
                'frame_count': int(frame_count),  # Ensure native int
                'brightness_analysis': self._analyze_brightness(sample_frames),
                'motion_analysis': self._analyze_motion_intensity(sample_frames),
                'color_analysis': self._analyze_colors(sample_frames),
                'scene_changes': self._detect_scene_changes(sample_frames)
            }
            
            # Convert all numpy types in the analysis
            return convert_numpy_types(analysis)
            
        except Exception as e:
            print(f"⚠️ OpenCV analysis failed: {e}")
            return {}
    
    def _analyze_brightness(self, frames: List[tuple]) -> Dict[str, Any]:
        """Analyze brightness levels across frames"""
        
        if not frames:
            return {}
        
        brightness_values = []
        for timestamp, frame in frames:
            # Convert to grayscale and calculate mean
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = float(gray.mean())  # Convert numpy float to Python float
            brightness_values.append(brightness)
        
        avg_brightness = float(sum(brightness_values) / len(brightness_values))
        
        return {
            'average_brightness': avg_brightness,
            'brightness_category': 'dark' if avg_brightness < 80 else 'normal' if avg_brightness < 180 else 'bright',
            'brightness_variance': float(max(brightness_values) - min(brightness_values))
        }
    
    def _analyze_motion_intensity(self, frames: List[tuple]) -> Dict[str, Any]:
        """Analyze motion/activity in the video"""
        
        if len(frames) < 2:
            return {}
        
        motion_scores = []
        
        for i in range(1, len(frames)):
            prev_frame = cv2.cvtColor(frames[i-1][1], cv2.COLOR_BGR2GRAY)
            curr_frame = cv2.cvtColor(frames[i][1], cv2.COLOR_BGR2GRAY)
            
            # Calculate frame difference
            diff = cv2.absdiff(prev_frame, curr_frame)
            motion_score = float(diff.mean())  # Convert numpy float to Python float
            motion_scores.append(motion_score)
        
        avg_motion = float(sum(motion_scores) / len(motion_scores))
        
        return {
            'average_motion': avg_motion,
            'motion_category': 'static' if avg_motion < 10 else 'moderate' if avg_motion < 30 else 'high',
            'motion_peaks': [i for i, score in enumerate(motion_scores) if score > avg_motion * 1.5]
        }
    
    def _analyze_colors(self, frames: List[tuple]) -> Dict[str, Any]:
        """Analyze color composition"""
        
        if not frames:
            return {}
        
        # Sample middle frame for color analysis
        mid_frame = frames[len(frames) // 2][1]
        
        # Calculate color histograms
        colors = {'blue': 0, 'green': 0, 'red': 0}
        for i, color in enumerate(['blue', 'green', 'red']):
            hist = cv2.calcHist([mid_frame], [i], None, [256], [0, 256])
            colors[color] = float(hist.mean())  # Convert numpy float to Python float
        
        # Determine dominant color
        dominant_color = max(colors, key=colors.get)
        
        return {
            'dominant_color': dominant_color,
            'color_balance': colors,
            'saturation_level': 'normal'  # Simplified
        }
    
    def _detect_scene_changes(self, frames: List[tuple]) -> List[float]:
        """Detect potential scene changes for auto-cutting"""
        
        if len(frames) < 2:
            return []
        
        scene_changes = []
        threshold = 30  # Motion threshold for scene change
        
        for i in range(1, len(frames)):
            prev_frame = cv2.cvtColor(frames[i-1][1], cv2.COLOR_BGR2GRAY)
            curr_frame = cv2.cvtColor(frames[i][1], cv2.COLOR_BGR2GRAY)
            
            # Calculate histogram difference
            hist1 = cv2.calcHist([prev_frame], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([curr_frame], [0], None, [256], [0, 256])
            
            correlation = float(cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL))  # Convert to native float
            
            # Low correlation indicates scene change
            if correlation < 0.7:
                scene_changes.append(float(frames[i][0]))  # timestamp as native float
        
        return scene_changes
    
    def _analyze_content_patterns(self, video_path: str, basic_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze content patterns to suggest editing approaches
        """
        
        duration = basic_info.get('duration', 0)
        aspect_ratio = basic_info.get('aspect_ratio', '16:9')
        
        # Content type suggestions based on video characteristics
        content_suggestions = []
        
        # Duration-based suggestions
        if duration < 30:
            content_suggestions.append("Short format - ideal for social media")
        elif duration > 300:
            content_suggestions.append("Long format - consider creating multiple clips")
        
        # Format-based suggestions
        if aspect_ratio == '9:16':
            content_suggestions.append("Vertical format - optimize for mobile viewing")
        elif aspect_ratio == '16:9':
            content_suggestions.append("Horizontal format - good for desktop/TV viewing")
        
        # Quality suggestions
        if basic_info.get('width', 0) < 1280:
            content_suggestions.append("Lower resolution - consider upscaling for better quality")
        
        return {
            'content_suggestions': content_suggestions,
            'estimated_complexity': self._estimate_editing_complexity(basic_info),
            'recommended_cuts': int(min(5, max(1, int(duration / 30))))  # Ensure native int
        }
    
    def _estimate_editing_complexity(self, video_info: Dict[str, Any]) -> str:
        """
        Estimate how complex the editing should be based on video characteristics
        """
        
        duration = video_info.get('duration', 0)
        motion_level = video_info.get('motion_category', 'moderate')
        
        complexity_score = 0
        
        # Duration factor
        if duration > 180:
            complexity_score += 2
        elif duration > 60:
            complexity_score += 1
        
        # Motion factor
        if motion_level == 'high':
            complexity_score += 2
        elif motion_level == 'moderate':
            complexity_score += 1
        
        # Quality factor
        if video_info.get('width', 0) >= 1920:
            complexity_score += 1
        
        if complexity_score <= 2:
            return 'simple'
        elif complexity_score <= 4:
            return 'moderate'
        else:
            return 'complex'
    
    def extract_thumbnail(self, video_path: str, timestamp: float = None) -> Optional[str]:
        """
        Extract a thumbnail from the video at specified timestamp
        """
        
        if timestamp is None:
            # Extract from middle of video
            info = self._get_video_info_ffprobe(video_path)
            timestamp = info['duration'] / 2
        
        output_path = f"output/thumbnails/{Path(video_path).stem}_thumb.jpg"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        cmd = [
            self.ffmpeg_path,
            '-i', video_path,
            '-ss', str(timestamp),
            '-vframes', '1',
            '-y',  # Overwrite output file
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_path
        except subprocess.CalledProcessError:
            return None
    
    def get_video_segments_info(self, video_path: str, segment_duration: int = 10) -> List[Dict[str, Any]]:
        """
        Analyze video in segments for detailed editing planning
        """
        
        info = self._get_video_info_ffprobe(video_path)
        duration = info['duration']
        
        segments = []
        current_time = 0
        
        while current_time < duration:
            segment_end = min(current_time + segment_duration, duration)
            
            segment_info = {
                'start': float(current_time),
                'end': float(segment_end),
                'duration': float(segment_end - current_time)
            }
            
            # Analyze this segment if OpenCV is available
            if CV2_AVAILABLE:
                segment_analysis = self._analyze_segment(video_path, current_time, segment_end)
                segment_info.update(segment_analysis)
            
            segments.append(segment_info)
            current_time = segment_end
        
        return convert_numpy_types(segments)
    
    def _analyze_segment(self, video_path: str, start_time: float, end_time: float) -> Dict[str, Any]:
        """
        Analyze a specific segment of the video
        """
        
        try:
            cap = cv2.VideoCapture(video_path)
            fps = float(cap.get(cv2.CAP_PROP_FPS))
            
            start_frame = int(start_time * fps)
            end_frame = int(end_time * fps)
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            frames = []
            current_frame = start_frame
            
            while current_frame < end_frame:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
                current_frame += 1
            
            cap.release()
            
            if not frames:
                return {}
            
            # Analyze this segment - convert all numpy types
            avg_brightness = float(sum(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).mean() for f in frames) / len(frames))
            
            # Motion analysis for this segment
            motion_scores = []
            for i in range(1, len(frames)):
                prev = cv2.cvtColor(frames[i-1], cv2.COLOR_BGR2GRAY)
                curr = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
                diff = cv2.absdiff(prev, curr)
                motion_scores.append(float(diff.mean()))
            
            avg_motion = float(sum(motion_scores) / len(motion_scores)) if motion_scores else 0.0
            
            return {
                'segment_brightness': avg_brightness,
                'segment_motion': avg_motion,
                'segment_quality': 'good' if avg_brightness > 50 and avg_motion > 5 else 'poor',
                'frame_count': int(len(frames))
            }
            
        except Exception as e:
            print(f"⚠️ Segment analysis failed: {e}")
            return {}
    
    def detect_optimal_cuts(self, video_path: str, target_segments: int = 3) -> List[Dict[str, float]]:
        """
        Detect optimal cut points in the video using scene change detection
        """
        
        info = self.analyze_video(video_path)
        scene_changes = info.get('scene_changes', [])
        duration = float(info['duration'])  # Ensure native float
        
        if not scene_changes:
            # Fallback: evenly spaced cuts
            segment_duration = duration / target_segments
            cuts = [
                {
                    'start': float(i * segment_duration),
                    'end': float(min((i + 1) * segment_duration, duration))
                }
                for i in range(target_segments)
            ]
            return cuts
        
        # Use detected scene changes for cuts
        cuts = []
        scene_changes.sort()
        
        # Add start of video
        current_start = 0.0
        
        for scene_time in scene_changes:
            scene_time = float(scene_time)  # Ensure native float
            if scene_time - current_start > 5:  # Minimum 5 seconds per segment
                cuts.append({
                    'start': float(current_start),
                    'end': float(scene_time)
                })
                current_start = scene_time
                
                if len(cuts) >= target_segments:
                    break
        
        # Add remaining video if needed
        if current_start < duration - 5:
            cuts.append({
                'start': float(current_start),
                'end': float(duration)
            })
        
        return cuts[:target_segments]