#!/usr/bin/env python3
import json
import os
import shutil
import requests
from pathlib import Path
from typing import Dict, List, Any
import zipfile

class CapCutDraftExtractor:
    def __init__(self, draft_folder: str):
        self.draft_folder = Path(draft_folder)
        self.assets_folder = self.draft_folder / "assets"
        self.draft_content = None
        
    def load_draft(self) -> Dict[str, Any]:
        """Load and parse the CapCut draft file"""
        draft_files = list(self.draft_folder.glob("draft_*.json"))
        if not draft_files:
            draft_files = list(self.draft_folder.glob("*.json"))
        
        if not draft_files:
            raise FileNotFoundError("No draft JSON file found")
            
        with open(draft_files[0], 'r', encoding='utf-8') as f:
            self.draft_content = json.load(f)
            
        print(f"✅ Loaded draft: {draft_files[0].name}")
        return self.draft_content
    
    def extract_media_info(self) -> List[Dict]:
        """Extract all media file information from the draft"""
        if not self.draft_content:
            self.load_draft()
            
        media_files = []
        
        # Look for video tracks
        if 'tracks' in self.draft_content:
            for track in self.draft_content['tracks']:
                if 'segments' in track:
                    for segment in track['segments']:
                        if 'material' in segment:
                            material = segment['material']
                            if 'video_file' in material:
                                media_files.append({
                                    'type': 'video',
                                    'file': material['video_file'],
                                    'segment': segment
                                })
                            if 'audio_file' in material:
                                media_files.append({
                                    'type': 'audio', 
                                    'file': material['audio_file'],
                                    'segment': segment
                                })
        
        # Look for materials array (alternative structure)
        if 'materials' in self.draft_content:
            for material in self.draft_content['materials']:
                if 'file' in material:
                    media_files.append({
                        'type': material.get('type', 'unknown'),
                        'file': material['file'],
                        'material': material
                    })
        
        return media_files
    
    def download_missing_media(self, output_dir: str = None) -> List[str]:
        """Download any media files that are URLs"""
        if not output_dir:
            output_dir = str(self.draft_folder / "downloaded_media")
            
        os.makedirs(output_dir, exist_ok=True)
        downloaded_files = []
        
        media_info = self.extract_media_info()
        
        for media in media_info:
            file_ref = media['file']
            
            if isinstance(file_ref, str) and file_ref.startswith('http'):
                # It's a URL, download it
                filename = os.path.basename(file_ref.split('?')[0])
                if not filename or '.' not in filename:
                    filename = f"media_{len(downloaded_files)}.mp4"
                    
                output_path = os.path.join(output_dir, filename)
                
                try:
                    print(f"📥 Downloading: {file_ref}")
                    response = requests.get(file_ref, stream=True)
                    response.raise_for_status()
                    
                    with open(output_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                            
                    downloaded_files.append(output_path)
                    print(f"✅ Downloaded: {output_path}")
                    
                except Exception as e:
                    print(f"❌ Failed to download {file_ref}: {e}")
                    
        return downloaded_files
    
    def copy_local_media(self, output_dir: str = None) -> List[str]:
        """Copy all local media files to output directory"""
        if not output_dir:
            output_dir = str(self.draft_folder / "exported_media")
            
        os.makedirs(output_dir, exist_ok=True)
        copied_files = []
        
        # Copy everything from assets folder
        if self.assets_folder.exists():
            for asset_file in self.assets_folder.iterdir():
                if asset_file.is_file():
                    dest_path = os.path.join(output_dir, asset_file.name)
                    shutil.copy2(asset_file, dest_path)
                    copied_files.append(dest_path)
                    print(f"📁 Copied: {asset_file.name}")
        
        return copied_files
    
    def create_portable_draft(self, output_dir: str) -> str:
        """Create a portable version of the draft with all media"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Copy draft folder structure
        portable_draft = os.path.join(output_dir, self.draft_folder.name + "_portable")
        if os.path.exists(portable_draft):
            shutil.rmtree(portable_draft)
            
        shutil.copytree(self.draft_folder, portable_draft)
        
        # Download any remote media
        downloaded = self.download_missing_media(os.path.join(portable_draft, "assets"))
        
        # Update draft JSON to point to local files
        self._update_draft_paths(portable_draft, downloaded)
        
        print(f"✅ Created portable draft: {portable_draft}")
        return portable_draft
    
    def _update_draft_paths(self, draft_dir: str, downloaded_files: List[str]):
        """Update the draft JSON to use local file paths"""
        draft_files = list(Path(draft_dir).glob("*.json"))
        
        for draft_file in draft_files:
            with open(draft_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            # Update file references (this is simplified - you'd need to map URLs to local files)
            content_str = json.dumps(content)
            
            # Replace HTTP URLs with local paths
            for downloaded in downloaded_files:
                filename = os.path.basename(downloaded)
                content_str = content_str.replace(
                    f'"http', 
                    f'"./assets/{filename}'  # Simplified replacement
                )
            
            # Write back updated content
            with open(draft_file, 'w', encoding='utf-8') as f:
                json.dump(json.loads(content_str), f, indent=2, ensure_ascii=False)
    
    def export_media_only(self, output_dir: str) -> Dict[str, List[str]]:
        """Export just the media files without CapCut structure"""
        os.makedirs(output_dir, exist_ok=True)
        
        results = {
            'local_files': self.copy_local_media(output_dir),
            'downloaded_files': self.download_missing_media(output_dir)
        }
        
        print(f"📁 Exported {len(results['local_files'])} local files")
        print(f"📥 Downloaded {len(results['downloaded_files'])} remote files") 
        
        return results
    
    def create_zip_export(self, output_path: str = None) -> str:
        """Create a ZIP file with all draft content"""
        if not output_path:
            output_path = f"{self.draft_folder.name}_export.zip"
            
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from draft folder
            for file_path in self.draft_folder.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.draft_folder.parent)
                    zipf.write(file_path, arcname)
            
            # Download and add remote media
            temp_media = self.download_missing_media()
            for media_file in temp_media:
                arcname = f"{self.draft_folder.name}/downloaded/{os.path.basename(media_file)}"
                zipf.write(media_file, arcname)
                os.remove(media_file)  # Clean up temp file
        
        print(f"📦 Created ZIP export: {output_path}")
        return output_path


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="CapCut Draft Extractor")
    parser.add_argument("draft_folder", help="Path to CapCut draft folder")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--mode", choices=['portable', 'media-only', 'zip'], 
                       default='media-only', help="Extraction mode")
    
    args = parser.parse_args()
    
    extractor = CapCutDraftExtractor(args.draft_folder)
    
    try:
        if args.mode == 'portable':
            result = extractor.create_portable_draft(args.output or ".")
            
        elif args.mode == 'media-only':
            result = extractor.export_media_only(args.output or "./exported_media")
            
        elif args.mode == 'zip':
            result = extractor.create_zip_export(args.output)
            
        print(f"✅ Export completed: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()