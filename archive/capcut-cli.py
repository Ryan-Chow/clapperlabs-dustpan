#!/usr/bin/env python3
import requests
import json
import os
import shutil
import zipfile
from pathlib import Path
import subprocess
from typing import Dict, Any, Optional, List

class EnhancedCapCutCLI:
    def __init__(self, base_url: str = "http://localhost:9000"):
        self.base_url = base_url
        self.current_draft_id = None
        
    def create_draft(self) -> Dict[str, Any]:
        """Create a new CapCut draft"""
        try:
            response = requests.post(f"{self.base_url}/create_draft", json={})
            response.raise_for_status()
            result = response.json()
            
            if 'draft_id' in result:
                self.current_draft_id = result['draft_id']
            elif 'output' in result and 'draft_id' in result['output']:
                self.current_draft_id = result['output']['draft_id']
                
            print(f"✅ Draft created: {self.current_draft_id}")
            return result
        except Exception as e:
            print(f"❌ Error creating draft: {e}")
            return {}
    
    def save_draft(self) -> Dict[str, Any]:
        """Save the current draft"""
        if not self.current_draft_id:
            print("❌ No draft created")
            return {}
            
        try:
            response = requests.post(f"{self.base_url}/save_draft", json={
                "draft_id": self.current_draft_id
            })
            response.raise_for_status()
            result = response.json()
            print(f"✅ Draft saved: {self.current_draft_id}")
            return result
        except Exception as e:
            print(f"❌ Error saving draft: {e}")
            return {}
    
    def custom_download(self, output_dir: str = "./downloads") -> Dict[str, Any]:
        """Custom download implementation"""
        if not self.current_draft_id:
            print("❌ No draft to download")
            return {}
            
        print(f"🔄 Starting custom download for {self.current_draft_id}")
        
        # Method 1: Check for local draft folder
        local_result = self._download_local_folder(output_dir)
        if local_result:
            return local_result
            
        # Method 2: Try server-side file access
        server_result = self._download_from_server(output_dir)
        if server_result:
            return server_result
            
        # Method 3: Try web scraping the download page
        web_result = self._download_via_web_scraping(output_dir)
        if web_result:
            return web_result
            
        print("❌ All download methods failed")
        return {}
    
    def _download_local_folder(self, output_dir: str) -> Optional[Dict[str, Any]]:
        """Try to find and copy local draft folder"""
        print("🔍 Looking for local draft folder...")
        
        # Look in current directory
        if os.path.exists(self.current_draft_id):
            return self._process_local_draft(self.current_draft_id, output_dir)
            
        # Look in common server locations
        search_paths = [
            f"./{self.current_draft_id}",
            f"./drafts/{self.current_draft_id}",
            f"./output/{self.current_draft_id}",
            f"../capcut-mcp/{self.current_draft_id}"
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                print(f"📁 Found draft folder: {path}")
                return self._process_local_draft(path, output_dir)
        
        print("📁 No local draft folder found")
        return None
    
    def _process_local_draft(self, draft_path: str, output_dir: str) -> Dict[str, Any]:
        """Process a local draft folder"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Copy the entire draft folder
        draft_name = os.path.basename(draft_path)
        output_path = os.path.join(output_dir, draft_name)
        
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        shutil.copytree(draft_path, output_path)
        
        # Extract media files
        media_files = self._extract_media_from_draft(output_path)
        
        # Create a clean media folder
        media_dir = os.path.join(output_dir, f"{draft_name}_media")
        os.makedirs(media_dir, exist_ok=True)
        
        copied_media = []
        for media_file in media_files:
            if os.path.exists(media_file):
                dest = os.path.join(media_dir, os.path.basename(media_file))
                shutil.copy2(media_file, dest)
                copied_media.append(dest)
        
        print(f"✅ Local draft processed!")
        print(f"📁 Draft folder: {output_path}")
        print(f"🎬 Media files: {media_dir}")
        print(f"📊 Found {len(copied_media)} media files")
        
        return {
            "method": "local_folder",
            "draft_folder": output_path,
            "media_folder": media_dir,
            "media_files": copied_media
        }
    
    def _extract_media_from_draft(self, draft_folder: str) -> List[str]:
        """Extract media file paths from draft"""
        media_files = []
        
        # Look in assets folder
        assets_folder = os.path.join(draft_folder, "assets")
        if os.path.exists(assets_folder):
            for file in os.listdir(assets_folder):
                file_path = os.path.join(assets_folder, file)
                if os.path.isfile(file_path):
                    media_files.append(file_path)
        
        # Parse draft JSON for additional references
        for json_file in Path(draft_folder).glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # This is a simplified parser - you'd need to adapt based on actual structure
                    self._find_media_in_json(data, media_files, draft_folder)
            except Exception as e:
                print(f"⚠️ Could not parse {json_file}: {e}")
        
        return media_files
    
    def _find_media_in_json(self, data: Any, media_files: List[str], base_path: str):
        """Recursively find media references in JSON"""
        if isinstance(data, dict):
            for key, value in data.items():
                if key in ['video_file', 'audio_file', 'image_file', 'file', 'path', 'url']:
                    if isinstance(value, str) and not value.startswith('http'):
                        # It's a local file reference
                        full_path = os.path.join(base_path, value)
                        if os.path.exists(full_path):
                            media_files.append(full_path)
                else:
                    self._find_media_in_json(value, media_files, base_path)
        elif isinstance(data, list):
            for item in data:
                self._find_media_in_json(item, media_files, base_path)
    
    def _download_from_server(self, output_dir: str) -> Optional[Dict[str, Any]]:
        """Try to download directly from MCP server"""
        print("🔍 Trying server-side download...")
        
        # Try different potential endpoints
        endpoints = [
            f"/download/{self.current_draft_id}",
            f"/export/{self.current_draft_id}",
            f"/draft/{self.current_draft_id}/download",
            f"/get_draft_files/{self.current_draft_id}"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=30)
                if response.status_code == 200:
                    # Check if it's a ZIP file or JSON
                    content_type = response.headers.get('content-type', '')
                    
                    if 'application/zip' in content_type or 'application/octet-stream' in content_type:
                        # It's a file download
                        output_file = os.path.join(output_dir, f"{self.current_draft_id}.zip")
                        os.makedirs(output_dir, exist_ok=True)
                        
                        with open(output_file, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"✅ Downloaded via server endpoint: {endpoint}")
                        return self._process_zip_download(output_file)
                        
            except Exception as e:
                continue
        
        print("📡 No working server endpoints found")
        return None
    
    def _process_zip_download(self, zip_file: str) -> Dict[str, Any]:
        """Process a downloaded ZIP file"""
        extract_dir = zip_file.replace('.zip', '_extracted')
        
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find media files in extracted content
        media_files = []
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.lower().endswith(('.mp4', '.mov', '.avi', '.mp3', '.wav', '.jpg', '.png')):
                    media_files.append(os.path.join(root, file))
        
        print(f"📦 Extracted ZIP file")
        print(f"📁 Content: {extract_dir}")
        print(f"🎬 Media files found: {len(media_files)}")
        
        return {
            "method": "zip_download",
            "extracted_folder": extract_dir,
            "media_files": media_files,
            "zip_file": zip_file
        }
    
    def _download_via_web_scraping(self, output_dir: str) -> Optional[Dict[str, Any]]:
        """Try to download by scraping the web interface"""
        print("🌐 Trying web interface download...")
        
        web_url = f"https://www.install-ai-guider.top/draft/downloader?draft_id={self.current_draft_id}"
        
        try:
            # First, get the page
            response = requests.get(web_url, timeout=30)
            response.raise_for_status()
            
            # Look for download links or buttons in the HTML
            import re
            download_links = re.findall(r'href="([^"]*download[^"]*)"', response.text)
            download_links.extend(re.findall(r'action="([^"]*download[^"]*)"', response.text))
            
            for link in download_links:
                try:
                    if not link.startswith('http'):
                        link = f"https://www.install-ai-guider.top{link}"
                    
                    download_response = requests.get(link, timeout=60)
                    if download_response.status_code == 200:
                        content_type = download_response.headers.get('content-type', '')
                        
                        if 'application' in content_type or len(download_response.content) > 1000:
                            # Looks like a file
                            filename = f"{self.current_draft_id}_web_download.zip"
                            output_file = os.path.join(output_dir, filename)
                            os.makedirs(output_dir, exist_ok=True)
                            
                            with open(output_file, 'wb') as f:
                                f.write(download_response.content)
                            
                            print(f"✅ Downloaded via web scraping")
                            return self._process_zip_download(output_file)
                            
                except Exception:
                    continue
            
        except Exception as e:
            print(f"🌐 Web scraping failed: {e}")
        
        return None
    
    def create_video_export(self, output_path: str = None) -> Dict[str, Any]:
        """Create a video export using ffmpeg if available"""
        if not output_path:
            output_path = f"./{self.current_draft_id}_export.mp4"
        
        # First download the draft
        download_result = self.custom_download()
        if not download_result:
            return {}
        
        media_files = download_result.get('media_files', [])
        video_files = [f for f in media_files if f.lower().endswith(('.mp4', '.mov', '.avi'))]
        
        if not video_files:
            print("❌ No video files found to export")
            return download_result
        
        # Try to use ffmpeg to concatenate videos
        if len(video_files) == 1:
            # Single video - just copy
            shutil.copy2(video_files[0], output_path)
            print(f"✅ Single video exported: {output_path}")
        else:
            # Multiple videos - try to concatenate with ffmpeg
            success = self._concatenate_videos_ffmpeg(video_files, output_path)
            if not success:
                print("⚠️ ffmpeg concatenation failed, copying first video only")
                shutil.copy2(video_files[0], output_path)
        
        download_result['exported_video'] = output_path
        return download_result
    
    def _concatenate_videos_ffmpeg(self, video_files: List[str], output_path: str) -> bool:
        """Use ffmpeg to concatenate multiple videos"""
        try:
            # Create a temporary file list for ffmpeg
            list_file = "temp_video_list.txt"
            with open(list_file, 'w') as f:
                for video in video_files:
                    f.write(f"file '{video}'\n")
            
            # Run ffmpeg
            cmd = [
                'ffmpeg', '-f', 'concat', '-safe', '0', 
                '-i', list_file, '-c', 'copy', output_path, '-y'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.remove(list_file)
            
            if result.returncode == 0:
                print(f"✅ Videos concatenated with ffmpeg: {output_path}")
                return True
            else:
                print(f"❌ ffmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ ffmpeg concatenation failed: {e}")
            return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced CapCut CLI")
    parser.add_argument("--url", default="http://localhost:9000")
    subparsers = parser.add_subparsers(dest="command")
    
    # Custom download command
    download_parser = subparsers.add_parser("custom-download", help="Custom download with multiple methods")
    download_parser.add_argument("--output", default="./downloads", help="Output directory")
    
    # Video export command  
    export_parser = subparsers.add_parser("video-export", help="Export as video file")
    export_parser.add_argument("--output", help="Output video file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = EnhancedCapCutCLI(args.url)
    
    # You'd need to set the draft ID somehow - either from previous command or as argument
    cli.current_draft_id = "dfd_cat_1754795836_a4df36da"  # Your current draft
    
    if args.command == "custom-download":
        result = cli.custom_download(args.output)
        print(f"📊 Download result: {json.dumps(result, indent=2)}")
        
    elif args.command == "video-export":
        result = cli.create_video_export(args.output)
        print(f"🎬 Export result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()