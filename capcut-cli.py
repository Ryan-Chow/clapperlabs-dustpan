#!/usr/bin/env python3
import requests
import argparse
import json
import sys
from typing import Dict, Any, Optional

class CapCutCLI:
    def __init__(self, base_url: str = "http://localhost:9000"):
        self.base_url = base_url
        self.current_draft_id = None
        
    def create_draft(self) -> Dict[str, Any]:
        """Create a new CapCut draft"""
        try:
            response = requests.post(f"{self.base_url}/create_draft")
            response.raise_for_status()
            result = response.json()
            if 'draft_id' in result:
                self.current_draft_id = result['draft_id']
                print(f"✅ Draft created successfully! ID: {self.current_draft_id}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating draft: {e}")
            return {}

    def add_video(self, video_path: str, start: float = 0, end: Optional[float] = None, 
                  width: int = 1080, height: int = 1920) -> Dict[str, Any]:
        """Add video to the current draft"""
        if not self.current_draft_id:
            print("❌ No draft created. Please create a draft first.")
            return {}
            
        data = {
            "draft_id": self.current_draft_id,
            "video_url": video_path,
            "start": start,
            "width": width,
            "height": height
        }
        if end is not None:
            data["end"] = end
            
        try:
            response = requests.post(f"{self.base_url}/add_video", json=data)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Video added successfully: {video_path}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding video: {e}")
            return {}

    def add_text(self, text: str, start: float = 0, end: float = 3, 
                 font: str = "Source Han Sans", font_color: str = "#FFFFFF", 
                 font_size: float = 30.0) -> Dict[str, Any]:
        """Add text overlay to the current draft"""
        if not self.current_draft_id:
            print("❌ No draft created. Please create a draft first.")
            return {}
            
        data = {
            "draft_id": self.current_draft_id,
            "text": text,
            "start": start,
            "end": end,
            "font": font,
            "font_color": font_color,
            "font_size": font_size
        }
        
        try:
            response = requests.post(f"{self.base_url}/add_text", json=data)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Text added successfully: '{text}'")
            return result
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding text: {e}")
            return {}

    def add_audio(self, audio_path: str, start: float = 0, 
                  end: Optional[float] = None, volume: float = 1.0) -> Dict[str, Any]:
        """Add audio to the current draft"""
        if not self.current_draft_id:
            print("❌ No draft created. Please create a draft first.")
            return {}
            
        data = {
            "draft_id": self.current_draft_id,
            "audio_url": audio_path,
            "start": start,
            "volume": volume
        }
        if end is not None:
            data["end"] = end
            
        try:
            response = requests.post(f"{self.base_url}/add_audio", json=data)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Audio added successfully: {audio_path}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding audio: {e}")
            return {}

    def add_effect(self, effect_type: str, target_material: Optional[str] = None,
                   parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add effect to materials"""
        if not self.current_draft_id:
            print("❌ No draft created. Please create a draft first.")
            return {}
            
        data = {
            "draft_id": self.current_draft_id,
            "effect_type": effect_type
        }
        if target_material:
            data["target_material"] = target_material
        if parameters:
            data["parameters"] = parameters
            
        try:
            response = requests.post(f"{self.base_url}/add_effect", json=data)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Effect added successfully: {effect_type}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding effect: {e}")
            return {}

    def save_draft(self, draft_folder: Optional[str] = None) -> Dict[str, Any]:
        """Save the current draft"""
        if not self.current_draft_id:
            print("❌ No draft created. Please create a draft first.")
            return {}
            
        data = {"draft_id": self.current_draft_id}
        if draft_folder:
            data["draft_folder"] = draft_folder
            
        try:
            response = requests.post(f"{self.base_url}/save_draft", json=data)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Draft saved successfully! ID: {self.current_draft_id}")
            print("📁 Copy the generated 'dfd_*' folder to your CapCut draft directory")
            return result
        except requests.exceptions.RequestException as e:
            print(f"❌ Error saving draft: {e}")
            return {}

    def vibe_edit(self, command: str) -> None:
        """Process a vibe editing command"""
        command_lower = command.lower()
        
        # Simple command parsing for vibe editing
        if "vintage" in command_lower or "retro" in command_lower:
            print("🎨 Applying vintage vibe...")
            self.add_effect("vintage_filter")
            self.add_effect("film_grain", parameters={"intensity": 0.3})
            
        elif "dramatic" in command_lower or "cinematic" in command_lower:
            print("🎬 Applying cinematic vibe...")
            self.add_effect("color_grading", parameters={"style": "cinematic"})
            self.add_effect("letterbox")
            
        elif "bright" in command_lower or "vibrant" in command_lower:
            print("☀️ Applying bright vibe...")
            self.add_effect("brightness", parameters={"value": 0.2})
            self.add_effect("saturation", parameters={"value": 0.3})
            
        elif "dark" in command_lower or "moody" in command_lower:
            print("🌙 Applying moody vibe...")
            self.add_effect("brightness", parameters={"value": -0.2})
            self.add_effect("contrast", parameters={"value": 0.3})
            
        else:
            print(f"🤔 Unknown vibe: '{command}'. Adding as custom effect...")
            self.add_effect("custom", parameters={"description": command})


def main():
    parser = argparse.ArgumentParser(description="CapCut MCP Command Line Interface")
    parser.add_argument("--url", default="http://localhost:9000", 
                       help="CapCut MCP server URL")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create draft
    subparsers.add_parser("create", help="Create a new draft")
    
    # Add video
    video_parser = subparsers.add_parser("add-video", help="Add video to draft")
    video_parser.add_argument("path", help="Path to video file")
    video_parser.add_argument("--start", type=float, default=0, help="Start time")
    video_parser.add_argument("--end", type=float, help="End time")
    video_parser.add_argument("--width", type=int, default=1080, help="Video width")
    video_parser.add_argument("--height", type=int, default=1920, help="Video height")
    
    # Add text
    text_parser = subparsers.add_parser("add-text", help="Add text overlay")
    text_parser.add_argument("text", help="Text content")
    text_parser.add_argument("--start", type=float, default=0, help="Start time")
    text_parser.add_argument("--end", type=float, default=3, help="End time")
    text_parser.add_argument("--font", default="Source Han Sans", help="Font name")
    text_parser.add_argument("--color", default="#FFFFFF", help="Font color")
    text_parser.add_argument("--size", type=float, default=30.0, help="Font size")
    
    # Add audio
    audio_parser = subparsers.add_parser("add-audio", help="Add audio to draft")
    audio_parser.add_argument("path", help="Path to audio file")
    audio_parser.add_argument("--start", type=float, default=0, help="Start time")
    audio_parser.add_argument("--end", type=float, help="End time")
    audio_parser.add_argument("--volume", type=float, default=1.0, help="Volume level")
    
    # Add effect
    effect_parser = subparsers.add_parser("add-effect", help="Add effect")
    effect_parser.add_argument("effect_type", help="Type of effect")
    effect_parser.add_argument("--params", help="Effect parameters as JSON string")
    
    # Vibe editing
    vibe_parser = subparsers.add_parser("vibe", help="Apply vibe-based editing")
    vibe_parser.add_argument("command", help="Vibe command (e.g., 'make it vintage')")
    
    # Save draft
    save_parser = subparsers.add_parser("save", help="Save the current draft")
    save_parser.add_argument("--folder", help="CapCut draft folder path")
    
    # Interactive mode
    subparsers.add_parser("interactive", help="Start interactive mode")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = CapCutCLI(args.url)
    
    try:
        if args.command == "create":
            cli.create_draft()
            
        elif args.command == "add-video":
            cli.add_video(args.path, args.start, args.end, args.width, args.height)
            
        elif args.command == "add-text":
            cli.add_text(args.text, args.start, args.end, args.font, args.color, args.size)
            
        elif args.command == "add-audio":
            cli.add_audio(args.path, args.start, args.end, args.volume)
            
        elif args.command == "add-effect":
            params = json.loads(args.params) if args.params else None
            cli.add_effect(args.effect_type, parameters=params)
            
        elif args.command == "vibe":
            cli.vibe_edit(args.command)
            
        elif args.command == "save":
            cli.save_draft(args.folder)
            
        elif args.command == "interactive":
            interactive_mode(cli)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def interactive_mode(cli: CapCutCLI):
    """Interactive command mode"""
    print("🎬 CapCut Interactive Mode")
    print("Commands: create, add-video <path>, add-text '<text>', vibe '<command>', save, quit")
    print("-" * 60)
    
    while True:
        try:
            command = input("capcut> ").strip()
            
            if not command:
                continue
                
            if command == "quit" or command == "exit":
                break
                
            parts = command.split(None, 1)
            cmd = parts[0].lower()
            
            if cmd == "create":
                cli.create_draft()
                
            elif cmd == "add-video" and len(parts) > 1:
                cli.add_video(parts[1])
                
            elif cmd == "add-text" and len(parts) > 1:
                text = parts[1].strip("'\"")
                cli.add_text(text)
                
            elif cmd == "vibe" and len(parts) > 1:
                vibe_cmd = parts[1].strip("'\"")
                cli.vibe_edit(vibe_cmd)
                
            elif cmd == "save":
                cli.save_draft()
                
            else:
                print("❓ Unknown command. Try: create, add-video, add-text, vibe, save, quit")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()