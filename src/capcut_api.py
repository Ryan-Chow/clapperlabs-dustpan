"""
CapCut API Wrapper - Integrates with the original capcut-mcp repository
"""

import requests
import json
import subprocess
import time
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

class CapCutAPI:
    def __init__(self, config):
        self.config = config
        self.base_url = config.get('capcut_mcp_url', 'http://localhost:9000')
        self.capcut_mcp_path = Path("capcut-mcp")
        self.server_process = None
        
        # Ensure the original capcut-mcp server is running
        self._ensure_server_running()
    
    def _ensure_server_running(self):
        """Start the original capcut-mcp server if not running"""
        
        from start_capcut_mcp import CapCutMCPManager
        
        self.mcp_manager = CapCutMCPManager()
        
        if not self.mcp_manager.is_server_running():
            print("🚀 Starting CapCut MCP server...")
            
            if not self.mcp_manager.start_server():
                raise Exception(
                    "Failed to start CapCut MCP server. Please ensure:\n"
                    "1. capcut-mcp directory exists\n"
                    "2. Dependencies are installed: cd capcut-mcp && pip install -r requirements.txt\n"
                    "3. FFmpeg is installed and in PATH"
                )
        
        # Test API endpoints
        endpoint_status = self.mcp_manager.test_api_endpoints()
        failed_endpoints = [ep for ep, status in endpoint_status.items() if not status and ep != "server_running"]
        
        if failed_endpoints:
            print(f"⚠️ Some API endpoints not responding: {failed_endpoints}")
            print("The server may still be starting up...")
            
            # Wait a bit more for full initialization
            time.sleep(3)
        
        print("✅ CapCut MCP server ready")
    
    def create_draft_from_plan(self, input_video: str, editing_plan: Dict[str, Any], 
                              output_name: str) -> Dict[str, Any]:
        """
        Create a CapCut draft from an AI editing plan using the exact capcut-mcp API
        """
        
        try:
            # Step 1: Create new draft (capcut-mcp creates drafts automatically)
            # Note: The original capcut-mcp doesn't have explicit draft creation,
            # it creates drafts when you start adding materials
            
            
            # Step 2: Add main video using exact capcut-mcp format
            video_cuts = editing_plan.get('cuts', [])
            
            if video_cuts:
                # Add video segments based on AI cuts
                for i, cut in enumerate(video_cuts):
                    self._api_call('/add_video', {
                        'video_url': input_video,  # Note: original expects 'video_url' not 'video_path'
                        'start': cut.get('start', 0),
                        'end': cut.get('end', 10),
                        'width': self._get_resolution_from_plan(editing_plan)[0],
                        'height': self._get_resolution_from_plan(editing_plan)[1]
                    })
            else:
                # Add full video if no cuts specified
                video_info = editing_plan.get('video_info', {})
                self._api_call('/add_video', {
                    'video_url': input_video,
                    'start': 0,
                    'end': video_info.get('duration', 30),
                    'width': video_info.get('width', 1920),
                    'height': video_info.get('height', 1080)
                })
            
            # Step 3: Add text elements using exact capcut-mcp format
            text_elements = editing_plan.get('text_elements', [])
            for text_elem in text_elements:
                self._api_call('/add_text', {
                    'text': text_elem.get('text', ''),
                    'start': text_elem.get('start', 0),
                    'end': text_elem.get('end', 3),
                    'font': text_elem.get('font', 'Source Han Sans'),  # capcut-mcp default
                    'font_color': text_elem.get('color', '#FF0000'),    # capcut-mcp format
                    'font_size': float(text_elem.get('size', 30.0))     # Must be float
                })
            
            # Step 4: Add audio if requested using capcut-mcp format
            audio_suggestions = editing_plan.get('audio', {})
            if audio_suggestions.get('add_music'):
                music_file = self._get_background_music(editing_plan.get('style'))
                if music_file:
                    self._api_call('/add_audio', {
                        'audio_url': music_file,  # Note: expects 'audio_url'
                        'start': 0,
                        'end': editing_plan.get('target_duration', 30),
                        'volume': audio_suggestions.get('music_volume', 0.3)
                    })
            
            # Step 5: Add subtitles if requested using capcut-mcp format
            if editing_plan.get('auto_subtitles'):
                subtitles = self._generate_subtitles(input_video, editing_plan)
                for subtitle in subtitles:
                    self._api_call('/add_subtitle', {
                        'text': subtitle['text'],
                        'start': subtitle['start'],
                        'end': subtitle['end']
                    })
            
            # Step 6: Add effects (note: capcut-mcp has /add_effect endpoint)
            effects = editing_plan.get('effects', [])
            for effect in effects:
                self._api_call('/add_effect', {
                    'effect_type': effect.get('type', 'transition'),
                    'effect_name': effect.get('name', 'fade'),
                    'start': effect.get('start', 0),
                    'end': effect.get('end', 1)
                })
            
            # Step 7: Add stickers if any
            stickers = editing_plan.get('stickers', [])
            for sticker in stickers:
                self._api_call('/add_sticker', {
                    'sticker_type': sticker.get('type', 'emoji'),
                    'sticker_content': sticker.get('content', '😀'),
                    'start': sticker.get('start', 0),
                    'end': sticker.get('end', 3),
                    'x': sticker.get('x', 100),
                    'y': sticker.get('y', 100)
                })
            
            # Step 8: Save the draft using exact capcut-mcp format
            capcut_drafts_folder = self.config.get_capcut_drafts_folder()
            
            save_response = self._api_call('/save_draft', {
                'draft_id': output_name,  # capcut-mcp uses this as identifier
                'draft_folder': capcut_drafts_folder
            })
            
            # The capcut-mcp generates a folder starting with "dfd_" 
            draft_path = save_response.get('draft_path', f"./dfd_{output_name}")
            
            return {
                'success': True,
                'draft_path': draft_path,
                'editing_plan': editing_plan,
                'instructions': f"Copy {draft_path} to your CapCut drafts directory to import"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _api_call(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make API call to the original capcut-mcp server with full error handling
        """
        
        # Ensure server is running
        if not hasattr(self, 'mcp_manager') or not self.mcp_manager.is_server_running():
            self._ensure_server_running()
        
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                json=data,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            # Handle different response types from capcut-mcp
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    # Some endpoints might return plain text
                    return {"success": True, "response": response.text}
            
            elif response.status_code == 400:
                # Bad request - likely parameter error
                error_msg = f"Bad request to {endpoint}: {response.text}"
                raise Exception(error_msg)
            
            elif response.status_code == 404:
                # Endpoint not found
                raise Exception(f"API endpoint not found: {endpoint}")
            
            elif response.status_code == 500:
                # Server error
                error_msg = f"Server error at {endpoint}: {response.text}"
                raise Exception(error_msg)
            
            else:
                raise Exception(f"Unexpected response code {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception(f"API call to {endpoint} timed out after 30 seconds")
        
        except requests.exceptions.ConnectionError:
            # Try to restart server once
            print("🔄 Connection failed, attempting to restart CapCut MCP server...")
            if hasattr(self, 'mcp_manager'):
                if self.mcp_manager.restart_server():
                    # Retry the API call once
                    try:
                        response = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=30)
                        return response.json() if response.status_code == 200 else {"error": response.text}
                    except Exception:
                        pass
            
            raise Exception(f"Could not connect to CapCut MCP server at {self.base_url}")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"CapCut MCP API call failed: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check of the CapCut MCP integration"""
        
        health_status = {
            "overall_status": "unknown",
            "server_running": False,
            "api_endpoints": {},
            "dependencies": {},
            "errors": []
        }
        
        try:
            # Check server status
            health_status["server_running"] = self.mcp_manager.is_server_running() if hasattr(self, 'mcp_manager') else False
            
            if health_status["server_running"]:
                # Test API endpoints
                health_status["api_endpoints"] = self.mcp_manager.test_api_endpoints()
                
                # Check if all critical endpoints are working
                critical_endpoints = ["/add_video", "/add_text", "/save_draft"]
                all_critical_working = all(
                    health_status["api_endpoints"].get(ep, False) 
                    for ep in critical_endpoints
                )
                
                if all_critical_working:
                    health_status["overall_status"] = "healthy"
                else:
                    health_status["overall_status"] = "degraded"
                    health_status["errors"].append("Some critical API endpoints not responding")
            else:
                health_status["overall_status"] = "down"
                health_status["errors"].append("CapCut MCP server not running")
            
            # Check dependencies
            health_status["dependencies"] = {
                "capcut_mcp_exists": self.capcut_mcp_path.exists(),
                "ffmpeg_available": self._check_ffmpeg(),
                "python_version_ok": sys.version_info >= (3, 8)
            }
            
        except Exception as e:
            health_status["overall_status"] = "error"
            health_status["errors"].append(str(e))
        
        return health_status
    
    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _get_resolution_from_plan(self, editing_plan: Dict[str, Any]) -> tuple:
        """Get width/height from editing plan"""
        quality = editing_plan.get('quality', '1080p')
        aspect_ratio = editing_plan.get('aspect_ratio', '16:9')
        
        # Base resolutions
        if quality == '720p':
            base_height = 720
        elif quality == '4k':
            base_height = 2160
        else:  # 1080p default
            base_height = 1080
        
        # Calculate width based on aspect ratio
        if aspect_ratio == '9:16':
            width = int(base_height * 9 / 16)
            height = base_height
        elif aspect_ratio == '1:1':
            width = height = base_height
        elif aspect_ratio == '4:3':
            width = int(base_height * 4 / 3)
            height = base_height
        else:  # 16:9 default
            width = int(base_height * 16 / 9)
            height = base_height
            
        return (width, height)
    
    def _get_background_music(self, style: str) -> Optional[str]:
        """
        Get background music file path based on style
        You'd implement this to return appropriate music files
        """
        
        music_dir = Path("assets/music")
        if not music_dir.exists():
            return None
        
        style_music = {
            'social_media': 'upbeat_short.mp3',
            'highlight_reel': 'energetic_sports.mp3',
            'tutorial': 'calm_background.mp3',
            'vlog': 'casual_ambient.mp3'
        }
        
        music_file = music_dir / style_music.get(style, 'default.mp3')
        return str(music_file) if music_file.exists() else None
    
    def _generate_subtitles(self, video_path: str, editing_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate subtitles for the video (placeholder for AI transcription)
        """
        
        # This would integrate with speech-to-text APIs
        # For now, return a simple placeholder
        duration = editing_plan.get('target_duration', 30)
        
        return [
            {
                'text': 'AI-generated subtitle',
                'start': 0,
                'end': min(3, duration)
            }
        ]
    
    def __del__(self):
        """Clean up server process when CLI exits"""
        if self.server_process:
            self.server_process.terminate()