#!/usr/bin/env python3
"""
CapCut CLI - AI-Powered Video Editing Command Line Tool
"""

import click
import os
import sys
from pathlib import Path
from typing import Optional, List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import CapCutCLI
from config import load_config
from src.utils.file_utils import validate_video_file, ensure_output_dir

@click.group()
@click.option('--config', '-c', default='config/config.json', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config: str, verbose: bool):
    """CapCut CLI - AI-powered video editing tool"""
    ctx.ensure_object(dict)
    ctx.obj['config_path'] = config
    ctx.obj['verbose'] = verbose
    
    # Initialize the CLI app
    try:
        ctx.obj['app'] = CapCutCLI(config_path=config, verbose=verbose)
    except Exception as e:
        click.echo(f"❌ Failed to initialize CapCut CLI: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('input_video', type=click.Path(exists=True))
@click.option('--style', '-s', default='auto', 
              type=click.Choice(['auto', 'social_media', 'highlight_reel', 'tutorial', 'vlog']),
              help='Video editing style preset')
@click.option('--duration', '-d', type=int, help='Target duration in seconds')
@click.option('--output', '-o', help='Output name for the CapCut draft')
@click.option('--add-music', is_flag=True, help='Add background music')
@click.option('--auto-subtitles', is_flag=True, help='Generate automatic subtitles')
@click.option('--quality', type=click.Choice(['720p', '1080p', '4k']), default='1080p')
@click.option('--aspect-ratio', type=click.Choice(['16:9', '9:16', '1:1', '4:3']), default='16:9')
@click.pass_context
def edit(ctx, input_video: str, style: str, duration: Optional[int], output: Optional[str], 
         add_music: bool, auto_subtitles: bool, quality: str, aspect_ratio: str):
    """Edit a video using AI-powered CapCut automation"""
    
    app = ctx.obj['app']
    verbose = ctx.obj['verbose']
    
    # Validate input
    if not validate_video_file(input_video):
        click.echo(f"❌ Invalid video file: {input_video}", err=True)
        return
    
    # Generate output name if not provided
    if not output:
        output = Path(input_video).stem + "_edited"
    
    click.echo(f"🎬 Starting AI video editing...")
    click.echo(f"📁 Input: {input_video}")
    click.echo(f"🎨 Style: {style}")
    click.echo(f"📐 Quality: {quality} ({aspect_ratio})")
    
    try:
        result = app.edit_video(
            input_path=input_video,
            style=style,
            duration=duration,
            output_name=output,
            add_music=add_music,
            auto_subtitles=auto_subtitles,
            quality=quality,
            aspect_ratio=aspect_ratio
        )
        
        if result['success']:
            click.echo(f"✅ Video editing completed!")
            click.echo(f"📂 CapCut draft saved to: {result['draft_path']}")
            click.echo(f"💡 Copy this folder to your CapCut drafts directory")
        else:
            click.echo(f"❌ Editing failed: {result['error']}", err=True)
            
    except KeyboardInterrupt:
        click.echo("\n⏹️  Editing cancelled by user")
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()

@cli.command()
@click.argument('input_directory', type=click.Path(exists=True, file_okay=False))
@click.option('--style', '-s', default='auto', help='Video editing style preset')
@click.option('--output-dir', '-o', default='output/batch/', help='Output directory for drafts')
@click.option('--parallel', '-p', type=int, default=1, help='Number of parallel processes')
@click.pass_context
def batch(ctx, input_directory: str, style: str, output_dir: str, parallel: int):
    """Batch process multiple videos in a directory"""
    
    app = ctx.obj['app']
    
    video_files = []
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.m4v']
    
    # Find all video files
    for ext in video_extensions:
        video_files.extend(Path(input_directory).glob(f'*{ext}'))
        video_files.extend(Path(input_directory).glob(f'*{ext.upper()}'))
    
    if not video_files:
        click.echo(f"❌ No video files found in {input_directory}")
        return
    
    click.echo(f"📁 Found {len(video_files)} video files")
    click.echo(f"🎨 Using style: {style}")
    click.echo(f"⚡ Parallel processes: {parallel}")
    
    ensure_output_dir(output_dir)
    
    try:
        results = app.batch_edit_videos(
            video_files=video_files,
            style=style,
            output_dir=output_dir,
            parallel_jobs=parallel
        )
        
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        
        click.echo(f"\n✅ Batch processing completed!")
        click.echo(f"📊 Results: {successful} successful, {failed} failed")
        
        if failed > 0:
            click.echo("\n❌ Failed files:")
            for result in results:
                if not result['success']:
                    click.echo(f"  - {result['input_file']}: {result['error']}")
                    
    except KeyboardInterrupt:
        click.echo("\n⏹️  Batch processing cancelled")

@cli.command()
@click.argument('input_video', type=click.Path(exists=True))
@click.pass_context
def interactive(ctx, input_video: str):
    """Interactive mode for custom video editing"""
    
    app = ctx.obj['app']
    
    click.echo("🎬 Welcome to CapCut CLI Interactive Mode!")
    click.echo(f"📁 Working with: {input_video}")
    
    try:
        app.interactive_edit(input_video)
    except KeyboardInterrupt:
        click.echo("\n👋 Goodbye!")

@cli.command()
@click.argument('input_video', type=click.Path(exists=True))
@click.pass_context
def analyze(ctx, input_video: str):
    """Analyze video content and suggest editing approaches"""
    
    app = ctx.obj['app']
    
    click.echo(f"🔍 Analyzing video: {input_video}")
    
    try:
        analysis = app.analyze_video(input_video)
        
        click.echo("\n📊 Video Analysis Results:")
        click.echo(f"Duration: {analysis['duration']:.2f}s")
        click.echo(f"Resolution: {analysis['width']}x{analysis['height']}")
        click.echo(f"FPS: {analysis['fps']}")
        click.echo(f"Audio channels: {analysis.get('audio_channels', 'Unknown')}")
        
        if 'ai_suggestions' in analysis:
            click.echo("\n🤖 AI Suggestions:")
            for suggestion in analysis['ai_suggestions']:
                click.echo(f"  • {suggestion}")
                
    except Exception as e:
        click.echo(f"❌ Analysis failed: {e}", err=True)

@cli.command()
def setup():
    """Setup CapCut CLI configuration"""
    
    click.echo("🛠️  CapCut CLI Setup")
    
    # Check for required dependencies
    try:
        import ffmpeg
        click.echo("✅ FFmpeg found")
    except ImportError:
        click.echo("❌ FFmpeg not found. Please install FFmpeg first.")
        return
    
    # Create directories
    dirs = ['config', 'output', 'output/drafts', 'templates']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        click.echo(f"📁 Created directory: {dir_name}")
    
    # Copy example config
    if not Path('config/config.json').exists():
        if Path('config/config.json.example').exists():
            import shutil
            shutil.copy('config/config.json.example', 'config/config.json')
            click.echo("📄 Created config/config.json from example")
        else:
            click.echo("⚠️  No example config found")
    
    # Check API key
    api_key = click.prompt("Enter your Anthropic API key", hide_input=True, default="")
    if api_key:
        with open('.env', 'w') as f:
            f.write(f"ANTHROPIC_API_KEY={api_key}\n")
        click.echo("✅ API key saved to .env")
    
    click.echo("\n🎉 Setup completed! Run 'python cli.py edit --help' to get started.")

if __name__ == '__main__':
    cli()