# CapCut CLI 🎬

AI-powered command-line interface for automated video editing using CapCut and Anthropic's Claude.

## Overview

CapCut CLI combines the power of AI with CapCut's video editing capabilities to automatically edit your raw footage. Simply provide your video files and editing preferences, and let AI create professional CapCut projects for you.

## Features

- 🤖 **AI-Powered Editing**: Uses Anthropic's Claude to analyze video content and create intelligent editing plans
- ✂️ **Automatic Cutting**: Smart scene detection and optimal cut point identification
- 🎨 **Style Presets**: Pre-configured editing styles (social media, highlight reel, tutorial, vlog)
- 📱 **Multi-Format Support**: Works with various video formats and aspect ratios
- 🎵 **Audio Integration**: Automatic background music and subtitle generation
- 📊 **Batch Processing**: Process multiple videos simultaneously
- 🔧 **CapCut Integration**: Generates native CapCut draft files for further editing

## Prerequisites

- **Python 3.8+**
- **FFmpeg** installed and in PATH
- **Anthropic API key**
- **CapCut** installed on your system
- **capcut-mcp** repository (automatically managed)

## Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url> capcut-cli
cd capcut-cli
```

### 2. Set Up capcut-mcp Dependency
```bash
# Add as git submodule (recommended)
git submodule add https://github.com/fancyboi999/capcut-mcp.git capcut-mcp
git submodule update --init --recursive

# OR clone directly
git clone https://github.com/fancyboi999/capcut-mcp.git capcut-mcp
```

### 3. Install Dependencies
```bash
# Install CLI dependencies
pip install -r requirements.txt

# Install capcut-mcp dependencies
cd capcut-mcp
pip install -r requirements.txt
cd ..
```

### 4. Configuration
```bash
# Set up CLI configuration
cp config/config.json.example config/config.json
cp .env.example .env

# Set up capcut-mcp configuration
cp capcut-mcp/config.json.example capcut-mcp/config.json

# Add your Anthropic API key to .env
echo "ANTHROPIC_API_KEY=your_api_key_here" >> .env
```

### 5. Initial Setup
```bash
python cli.py setup
```

## Quick Start

### Basic Video Editing
```bash
# Edit a video with AI choosing the best style
python cli.py edit my_video.mp4

# Specify editing style and duration
python cli.py edit my_video.mp4 --style social_media --duration 60

# Add music and subtitles
python cli.py edit my_video.mp4 --add-music --auto-subtitles --style highlight_reel
```

### Batch Processing
```bash
# Process all videos in a folder
python cli.py batch videos/ --style tutorial

# Parallel processing for faster results
python cli.py batch videos/ --parallel 3 --style social_media
```

### Interactive Mode
```bash
# Interactive editing with custom prompts
python cli.py interactive my_video.mp4
```

### Video Analysis
```bash
# Analyze video and get AI suggestions
python cli.py analyze my_video.mp4
```

## Command Reference

### `edit` - Edit a single video
```bash
python cli.py edit INPUT_VIDEO [OPTIONS]
```

**Options:**
- `--style, -s`: Editing style (`auto`, `social_media`, `highlight_reel`, `tutorial`, `vlog`)
- `--duration, -d`: Target duration in seconds
- `--output, -o`: Output name for the CapCut draft
- `--add-music`: Add background music
- `--auto-subtitles`: Generate automatic subtitles
- `--quality`: Video quality (`720p`, `1080p`, `4k`)
- `--aspect-ratio`: Aspect ratio (`16:9`, `9:16`, `1:1`, `4:3`)

### `batch` - Process multiple videos
```bash
python cli.py batch INPUT_DIRECTORY [OPTIONS]
```

**Options:**
- `--style, -s`: Editing style for all videos
- `--output-dir, -o`: Output directory for drafts
- `--parallel, -p`: Number of parallel processes

### `interactive` - Interactive editing mode
```bash
python cli.py interactive INPUT_VIDEO
```

### `analyze` - Analyze video content
```bash
python cli.py analyze INPUT_VIDEO
```

## Editing Styles

### Social Media (`social_media`)
- Target: 60 seconds
- Aspect ratio: 9:16 (vertical)
- Fast-paced cuts with captions
- Optimized for TikTok, Instagram Reels

### Highlight Reel (`highlight_reel`)
- Target: 90 seconds
- Aspect ratio: 16:9
- Dynamic cuts focusing on best moments
- Perfect for sports or event highlights

### Tutorial (`tutorial`)
- Target: 5 minutes
- Aspect ratio: 16:9
- Clean, educational style with clear captions
- Slower cuts for better comprehension

### Vlog (`vlog`)
- Target: 3 minutes
- Aspect ratio: 16:9
- Casual style with personal touches
- Balanced pacing for storytelling

## AI Integration

The CLI uses Anthropic's Claude to:

1. **Analyze Video Content**: Understand what's in your video (motion, brightness, scene changes)
2. **Create Editing Plans**: Generate detailed editing instructions based on content and style
3. **Optimize Cuts**: Find the best moments to cut and transition
4. **Generate Text**: Create appropriate titles, captions, and subtitles
5. **Suggest Effects**: Recommend transitions and effects that match the content

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CapCut CLI    │───▶│   AI Director    │───▶│  Anthropic API  │
│   (User Input)  │    │  (Claude AI)     │    │     (Claude)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌──────────────────┐
│ CapCut API      │───▶│   capcut-mcp     │
│ (Translation)   │    │   (Original)     │
└─────────────────┘    └──────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌──────────────────┐
│ CapCut Drafts   │    │    CapCut App    │
│ (Generated)     │───▶│   (Final Edit)   │
└─────────────────┘    └──────────────────┘
```

## Compatibility with capcut-mcp

This CLI is fully compatible with the original [capcut-mcp](https://github.com/fancyboi999/capcut-mcp) repository:

- ✅ Uses exact API endpoints (`/add_video`, `/add_text`, `/add_audio`, etc.)
- ✅ Maintains original parameter formats and data structures
- ✅ Supports both CapCut China and International versions
- ✅ Generates standard CapCut draft folders (`dfd_*`)
- ✅ Preserves all original functionality while adding AI intelligence

## Troubleshooting

### Common Issues

**"CapCut MCP server not found"**
```bash
# Ensure capcut-mcp is cloned and configured
git clone https://github.com/fancyboi999/capcut-mcp.git capcut-mcp
cd capcut-mcp && pip install -r requirements.txt
```

**"FFmpeg not found"**
```bash
# Install FFmpeg (varies by OS)
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg
# Windows: Download from https://ffmpeg.org/
```

**"Anthropic API key invalid"**
```bash
# Verify your API key in .env file
echo "ANTHROPIC_API_KEY=your_actual_key" > .env
```

**"CapCut drafts folder not found"**
- The CLI auto-detects CapCut installation
- Manually set path in `config/config.json` if needed
- Ensure CapCut is installed and has been run at least once

### Debug Mode
```bash
python cli.py --verbose edit my_video.mp4
```

## Advanced Usage

### Custom AI Instructions
```bash
# Interactive mode allows custom AI prompts
python cli.py interactive my_video.mp4
# Then provide specific editing instructions to the AI
```

### Template Customization
Edit files in `templates/` directory to create custom editing styles:
```json
{
  "name": "my_custom_style",
  "target_duration": 45,
  "effects": ["custom_transition"],
  "text_style": {
    "font": "Custom Font",
    "color": "#custom_color"
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

- Built on top of [capcut-mcp](https://github.com/fancyboi999/capcut-mcp) by fancyboi999
- Powered by [Anthropic's Claude](https://www.anthropic.com/) for AI intelligence
- Uses [FFmpeg](https://ffmpeg.org/) for video processing