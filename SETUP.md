# Complete Integration Guide: CapCut CLI + Original capcut-mcp

## Key Integration Points with capcut-mcp:

### 1. **Dependency Management**
The original capcut-mcp sits in its own directory and runs as a separate HTTP server:
```
capcut-cli/
├── capcut-mcp/           # Original repo as git submodule
│   ├── main.py           # Their HTTP server
│   ├── config.json       # Their config
│   └── requirements.txt  # Their dependencies
├── src/                  # Your CLI code
│   ├── capcut_api.py     # Wrapper that calls their API
│   └── ai_director.py    # Your AI logic
```

### 2. **API Compatibility**
Your `capcut_api.py` makes HTTP calls to the exact endpoints from the original:
- `/add_video` - Add video segments
- `/add_text` - Add text overlays  
- `/add_audio` - Add audio tracks
- `/add_subtitle` - Add subtitles
- `/add_effect` - Add effects/transitions
- `/add_sticker` - Add stickers/emojis
- `/save_draft` - Generate CapCut draft folder

### 3. **Data Format Compatibility**
Uses the exact parameter formats expected by capcut-mcp:
```python
# Your CLI generates this format for capcut-mcp:
{
    "video_url": "path/to/video.mp4",  # Note: 'video_url' not 'video_path'
    "start": 0,
    "end": 10,
    "width": 1920,
    "height": 1080
}
```

### 4. **Server Lifecycle Management**
Your CLI automatically:
- Starts the capcut-mcp server if not running
- Monitors server health
- Restarts if connection fails
- Cleans up on exit

## Complete Setup Workflow:

### Step 1: Initial Setup
```bash

# 1. Add original capcut-mcp
git submodule add https://github.com/fancyboi999/capcut-mcp.git capcut-mcp
#(This is already done)

### Step 2: Install Dependencies
```bash
# Install CLI dependencies
pip install -r requirements.txt

# Install capcut-mcp dependencies
cd capcut-mcp
pip install -r requirements.txt
cd ..
```

### Step 3: Configuration
```bash
# Set up environment
cp .env.example .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env

# Configure CLI
cp config/config.json.example config/config.json

# Configure capcut-mcp
cp capcut-mcp/config.json.example capcut-mcp/config.json
```

### Step 4: Test Integration
```bash
# Run health check
python example_usage.py health

# Test basic editing
python cli.py edit sample_video.mp4 --style social_media
```

## How the AI + capcut-mcp Flow Works:

```
1. User runs: python cli.py edit video.mp4 --style social_media

2. CLI starts capcut-mcp server (localhost:9000)

3. AI Director analyzes video with Anthropic API:
   - Video duration, resolution, content type
   - Optimal cut points and timing
   - Text overlay suggestions
   - Effect recommendations

4. AI creates editing plan:
   {
     "cuts": [{"start": 0, "end": 15}, {"start": 30, "end": 45}],
     "text_elements": [{"text": "Amazing!", "start": 2, "end": 5}],
     "effects": [{"type": "transition", "name": "fade"}]
   }

5. CapCut API wrapper translates plan to capcut-mcp calls:
   POST /add_video {"video_url": "video.mp4", "start": 0, "end": 15}
   POST /add_text {"text": "Amazing!", "start": 2, "end": 5}
   POST /save_draft {"draft_id": "video_edited"}

6. capcut-mcp generates CapCut draft folder (dfd_video_edited/)

7. User copies folder to CapCut drafts directory

8. Opens CapCut to see AI-edited project ready for final touches
```

## Key Benefits of This Architecture:

✅ **Leverages Proven Code**: Uses the working capcut-mcp for actual CapCut integration
✅ **Adds AI Intelligence**: Your CLI adds the "brain" that makes smart editing decisions  
✅ **Maintains Compatibility**: Works with both CapCut versions (China/International)
✅ **Easy Updates**: Can update capcut-mcp independently of your CLI
✅ **Clean Separation**: AI logic separate from CapCut technical implementation

## Testing Your Integration:

```bash
# 1. Health check
python cli.py setup

# 2. Test server integration  
python start_capcut_mcp.py

# 3. Test AI analysis
python cli.py analyze sample_video.mp4

# 4. Full workflow test
python cli.py edit sample_video.mp4 --style social_media --verbose

# 5. Interactive test
python cli.py interactive sample_video.mp4
```

## Troubleshooting Integration Issues:

**Server won't start**: Check capcut-mcp requirements.txt is installed
**API calls fail**: Verify endpoints match capcut-mcp exactly
**Drafts don't appear**: Check CapCut drafts folder path in config
**FFmpeg errors**: Ensure FFmpeg is installed and in PATH

Your CLI now acts as an intelligent wrapper around the proven capcut-mcp functionality, adding AI decision-making and a user-friendly interface while preserving full compatibility with the original CapCut integration!