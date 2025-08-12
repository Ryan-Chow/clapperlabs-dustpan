"""
CapCut CLI - Main application logic
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from capcut_api import CapCutAPI
from ai_director import AIDirector
from video_analyzer import VideoAnalyzer
from config import Config
from utils.file_utils import ensure_output_dir, generate_unique_name
from utils.video_utils import get_video_info

class CapCutCLI:
    def __init__(self, config_path: str = "config/config.json", verbose: bool = False, 
             start_server: bool = False, server_port: int = 9000): 
        self.config = Config(config_path)
        self.verbose = verbose
        self.capcut_api = CapCutAPI(self.config, start_server=start_server, server_port=server_port)
        self.ai_director = AIDirector(self.config)
        self.video_analyzer = VideoAnalyzer(self.config)
        
        # Ensure output directory exists
        ensure_output_dir(self.config.get('output_dir', 'output/drafts'))
        
        if self.verbose:
            print("✅ CapCut CLI initialized successfully")
    
    def edit_video(self, input_path: str, style: str = "auto", duration: Optional[int] = None,
                   output_name: Optional[str] = None, add_music: bool = False,
                   auto_subtitles: bool = False, quality: str = "1080p", 
                   aspect_ratio: str = "16:9") -> Dict[str, Any]:
        """
        Main video editing function that coordinates AI analysis and CapCut editing
        """
        
        try:
            # Step 1: Analyze the video
            if self.verbose:
                print("🔍 Analyzing video content...")
            
            video_info = self.video_analyzer.analyze_video(input_path)
            
            # Step 2: Get AI editing decisions
            if self.verbose:
                print("🤖 Getting AI editing recommendations...")
            
            editing_plan = self.ai_director.create_editing_plan(
                video_info=video_info,
                style=style,
                target_duration=duration,
                quality=quality,
                aspect_ratio=aspect_ratio,
                add_music=add_music,
                auto_subtitles=auto_subtitles
            )
            
            # Step 3: Create CapCut draft
            if self.verbose:
                print("✂️ Creating CapCut draft...")
            
            if not output_name:
                output_name = generate_unique_name(Path(input_path).stem)
            
            draft_result = self.capcut_api.create_draft_from_plan(
                input_video=input_path,
                editing_plan=editing_plan,
                output_name=output_name
            )
            
            if self.verbose:
                print(f"💾 Draft saved to: {draft_result['draft_path']}")
            
            return {
                'success': True,
                'draft_path': draft_result['draft_path'],
                'editing_plan': editing_plan,
                'video_info': video_info
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def batch_edit_videos(self, video_files: List[Path], style: str = "auto", 
                         output_dir: str = "output/batch/", 
                         parallel_jobs: int = 1) -> List[Dict[str, Any]]:
        """
        Batch process multiple videos
        """
        
        ensure_output_dir(output_dir)
        results = []
        
        if parallel_jobs == 1:
            # Sequential processing
            for i, video_file in enumerate(video_files, 1):
                if self.verbose:
                    print(f"📹 Processing {i}/{len(video_files)}: {video_file.name}")
                
                result = self.edit_video(
                    input_path=str(video_file),
                    style=style,
                    output_name=f"{video_file.stem}_batch"
                )
                result['input_file'] = str(video_file)
                results.append(result)
        else:
            # Parallel processing
            with ThreadPoolExecutor(max_workers=parallel_jobs) as executor:
                future_to_file = {
                    executor.submit(
                        self.edit_video,
                        str(video_file),
                        style,
                        None,
                        f"{video_file.stem}_batch"
                    ): video_file for video_file in video_files
                }
                
                for future in as_completed(future_to_file):
                    video_file = future_to_file[future]
                    try:
                        result = future.result()
                        result['input_file'] = str(video_file)
                        results.append(result)
                        
                        if self.verbose:
                            status = "✅" if result['success'] else "❌"
                            print(f"{status} Completed: {video_file.name}")
                            
                    except Exception as e:
                        results.append({
                            'success': False,
                            'error': str(e),
                            'input_file': str(video_file)
                        })
                        
                        if self.verbose:
                            print(f"❌ Failed: {video_file.name} - {e}")
        
        return results
    
    def interactive_edit(self, input_video: str):
        """
        Interactive editing mode with user prompts
        """
        
        print(f"\n🎬 Interactive Editing Mode")
        print(f"📁 Video: {input_video}")
        
        # Analyze video first
        print("\n🔍 Analyzing video...")
        video_info = self.video_analyzer.analyze_video(input_video)
        
        print(f"\n📊 Video Information:")
        print(f"  Duration: {video_info['duration']:.1f}s")
        print(f"  Resolution: {video_info['width']}x{video_info['height']}")
        print(f"  FPS: {video_info['fps']}")
        
        # Get user preferences
        print(f"\n🎨 Editing Preferences:")
        
        style = input("Style (social_media/highlight_reel/tutorial/vlog) [auto]: ").strip() or "auto"
        
        duration_input = input(f"Target duration in seconds [{video_info['duration']:.0f}]: ").strip()
        duration = int(duration_input) if duration_input else None
        
        add_music = input("Add background music? (y/n) [n]: ").strip().lower() == 'y'
        auto_subtitles = input("Add automatic subtitles? (y/n) [n]: ").strip().lower() == 'y'
        
        aspect_ratio = input("Aspect ratio (16:9/9:16/1:1) [16:9]: ").strip() or "16:9"
        quality = input("Quality (720p/1080p/4k) [1080p]: ").strip() or "1080p"
        
        output_name = input("Output name [auto]: ").strip()
        
        # Custom AI instructions
        custom_instructions = input("\n💭 Any specific editing instructions for the AI? [none]: ").strip()
        
        print(f"\n🚀 Starting editing process...")
        
        # Execute editing
        result = self.edit_video(
            input_path=input_video,
            style=style,
            duration=duration,
            output_name=output_name,
            add_music=add_music,
            auto_subtitles=auto_subtitles,
            quality=quality,
            aspect_ratio=aspect_ratio
        )
        
        if result['success']:
            print(f"\n✅ Interactive editing completed!")
            print(f"📂 Draft location: {result['draft_path']}")
            
            # Show editing summary
            plan = result['editing_plan']
            print(f"\n📋 Editing Summary:")
            print(f"  Cuts made: {len(plan.get('cuts', []))}")
            print(f"  Effects added: {len(plan.get('effects', []))}")
            print(f"  Text elements: {len(plan.get('texts', []))}")
            
        else:
            print(f"\n❌ Editing failed: {result['error']}")
    
    def analyze_video(self, input_video: str) -> Dict[str, Any]:
        """
        Analyze video and return detailed information with AI suggestions
        """
        
        # Basic video info
        video_info = self.video_analyzer.analyze_video(input_video)
        
        # Get AI analysis and suggestions
        ai_analysis = self.ai_director.analyze_for_editing(video_info)
        
        return {
            **video_info,
            'ai_suggestions': ai_analysis.get('suggestions', []),
            'recommended_style': ai_analysis.get('recommended_style', 'auto'),
            'estimated_edit_time': ai_analysis.get('estimated_time', 'Unknown')
        }

def main():
    """Entry point for direct script execution"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <video_file>")
        sys.exit(1)
    
    app = CapCutCLI(verbose=True)
    result = app.edit_video(sys.argv[1])
    
    if result['success']:
        print(f"✅ Success! Draft saved to: {result['draft_path']}")
    else:
        print(f"❌ Failed: {result['error']}")

if __name__ == "__main__":
    main()