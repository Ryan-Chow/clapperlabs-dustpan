"""
AI Director - Uses Anthropic API to make intelligent video editing decisions
Fixed version with proper JSON serialization for numpy types
"""

import json
import os
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    import anthropic
except ImportError:
    raise ImportError("Please install anthropic: pip install anthropic")


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


class AIDirector:
    def __init__(self, config):
        self.config = config
        
        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY') or config.get('anthropic_api_key')
        if not api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable or add to config.")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        # Updated to use the current model name
        self.model = config.get('anthropic_model', 'claude-sonnet-4-20250514')
        
        # Load editing prompts
        self.load_prompts()
    
    def load_prompts(self):
        """Load AI prompts for different editing tasks"""
        
        # Always use default prompts to avoid JSON loading issues
        self.prompts = {
            "analyze_video": """Analyze this video information and provide editing recommendations:

Video Details: {video_info}

Please provide:
1. Content analysis (what type of content is this?)
2. Recommended editing style
3. Suggested cuts and highlights
4. Text overlay suggestions
5. Music/audio recommendations
6. Estimated editing complexity

Return your response as structured JSON with these keys: content_type, recommended_style, cuts, text_overlays, audio_suggestions, complexity_score""",

            "create_editing_plan": """Create a detailed video editing plan for CapCut based on this information:

Video Info: {video_info}
Style: {style}
Target Duration: {duration}s
Add Music: {add_music}
Auto Subtitles: {auto_subtitles}
Quality: {quality}
Aspect Ratio: {aspect_ratio}

Create a comprehensive editing plan with:
1. Timeline cuts (start/end times)
2. Transitions between clips
3. Text overlays with timing
4. Effects to apply
5. Audio adjustments
6. Color grading suggestions

Return as JSON with keys: cuts, transitions, text_elements, effects, audio, color_grading"""
        }
    
    def analyze_for_editing(self, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze video content and provide AI-powered editing suggestions
        """
        
        # Convert numpy types before JSON serialization
        clean_video_info = convert_numpy_types(video_info)
        
        prompt = self.prompts["analyze_video"].format(
            video_info=json.dumps(clean_video_info, indent=2)
        )
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                system="You are an expert video editor who analyzes content and provides editing recommendations. Always respond with valid JSON.",
                messages=[{
                    "role": "user", 
                    "content": prompt
                }]
            )
            
            # Parse AI response
            response_text = message.content[0].text
            
            # Try to extract JSON from response
            try:
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                else:
                    json_text = response_text.strip()
                
                analysis = json.loads(json_text)
                
                # Add some default suggestions if AI didn't provide them
                if 'suggestions' not in analysis:
                    analysis['suggestions'] = self._generate_default_suggestions(clean_video_info)
                
                return convert_numpy_types(analysis)
                
            except json.JSONDecodeError:
                # Fallback to text parsing
                return self._parse_text_analysis(response_text, clean_video_info)
                
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")
            return self._generate_default_suggestions(clean_video_info)
    
    def create_editing_plan(self, video_info: Dict[str, Any], style: str = "auto",
                           target_duration: Optional[int] = None, quality: str = "1080p",
                           aspect_ratio: str = "16:9", add_music: bool = False,
                           auto_subtitles: bool = False) -> Dict[str, Any]:
        """
        Create a detailed editing plan using AI
        """
        
        # Convert numpy types before processing
        clean_video_info = convert_numpy_types(video_info)
        
        # Auto-detect style if needed
        if style == "auto":
            analysis = self.analyze_for_editing(clean_video_info)
            style = analysis.get('recommended_style', 'social_media')
        
        # Set target duration if not specified
        if not target_duration:
            duration = clean_video_info['duration']
            if style == "social_media":
                target_duration = min(60, duration * 0.7)
            elif style == "highlight_reel":
                target_duration = min(90, duration * 0.5)
            else:
                target_duration = duration * 0.8
            target_duration = int(target_duration)  # Ensure it's a native int
        
        prompt = self.prompts["create_editing_plan"].format(
            video_info=json.dumps(clean_video_info, indent=2),
            style=style,
            duration=target_duration,
            add_music=add_music,
            auto_subtitles=auto_subtitles,
            quality=quality,
            aspect_ratio=aspect_ratio
        )
        
        try:
            print(f"🤖 Sending request to Anthropic API...")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system="You are an expert video editor creating editing plans for CapCut. Provide detailed, actionable editing instructions as JSON.",
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            print(f"✅ Received response from Anthropic API")
            
            response_text = message.content[0].text
            
            # Debug: Print the AI response
            print(f"🤖 AI Response: {response_text[:500]}...")
            print(f"🤖 AI Response length: {len(response_text)}")
            
            # Parse the editing plan
            try:
                print(f"🔍 Parsing AI response...")
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                    print(f"📝 Found JSON code block")
                else:
                    json_text = response_text.strip()
                    print(f"📝 Using raw response text")
                
                print(f"🔍 Extracted JSON: {json_text[:300]}...")
                print(f"🔍 JSON text length: {len(json_text)}")
                
                editing_plan = json.loads(json_text)
                print(f"✅ JSON parsing successful")
                
                # Validate and enhance the plan
                editing_plan = self._validate_editing_plan(editing_plan, clean_video_info)
                
                return convert_numpy_types(editing_plan)
                
            except json.JSONDecodeError:
                return self._create_fallback_plan(clean_video_info, style, target_duration)
                
        except Exception as e:
            print(f"⚠️ AI planning failed: {e}")
            print(f"⚠️ Exception type: {type(e)}")
            print(f"⚠️ Exception details: {str(e)}")
            import traceback
            print(f"⚠️ Traceback: {traceback.format_exc()}")
            return self._create_fallback_plan(clean_video_info, style, target_duration)
    
    def _validate_editing_plan(self, plan: Dict[str, Any], video_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and enhance the AI-generated editing plan
        """
        
        print(f"🔍 Validating editing plan...")
        print(f"🔍 Plan keys: {list(plan.keys())}")
        
        video_duration = float(video_info.get('duration', 30))
        
        # Ensure cuts don't exceed video duration
        if 'cuts' in plan:
            print(f"🔍 Processing cuts: {plan['cuts']}")
            valid_cuts = []
            for cut in plan['cuts']:
                start = max(0.0, float(cut.get('start', 0)))
                end = min(video_duration, float(cut.get('end', video_duration)))
                if start < end:
                    valid_cuts.append({'start': start, 'end': end})
            plan['cuts'] = valid_cuts
            print(f"✅ Validated cuts: {valid_cuts}")
        
        # Validate text elements timing
        if 'text_elements' in plan:
            for text_elem in plan['text_elements']:
                text_elem['start'] = max(0.0, float(text_elem.get('start', 0)))
                text_elem['end'] = min(video_duration, float(text_elem.get('end', 5)))
        
        # Add video_info to plan for reference
        plan['video_info'] = video_info
        plan['target_duration'] = float(plan.get('target_duration', video_duration * 0.8))
        
        return plan
    
    def _create_fallback_plan(self, video_info: Dict[str, Any], style: str, 
                             target_duration: Optional[int]) -> Dict[str, Any]:
        """
        Create a basic editing plan when AI fails
        """
        
        video_duration = float(video_info.get('duration', 30))
        # Handle case where target_duration is None
        if target_duration is None:
            target_duration = min(60.0, video_duration)  # Default to 60 seconds or video duration
        else:
            target_duration = float(target_duration)
        
        # Basic cuts for highlight reel
        if style == "highlight_reel":
            cuts = [
                {'start': 0.0, 'end': min(10.0, video_duration)},
                {'start': max(0.0, video_duration * 0.3), 'end': min(video_duration * 0.3 + 15.0, video_duration)},
                {'start': max(0.0, video_duration * 0.7), 'end': min(video_duration * 0.7 + 10.0, video_duration)}
            ]
        elif style == "social_media":
            # Single cut for social media
            start_time = max(0.0, (video_duration - target_duration) / 2)
            cuts = [{'start': start_time, 'end': start_time + target_duration}]
        else:
            # Default: use most of the video
            cuts = [{'start': 0.0, 'end': min(target_duration, video_duration)}]
        
        return {
            'cuts': cuts,
            'text_elements': [
                {
                    'text': 'Edited with CapCut CLI',
                    'start': 1.0,
                    'end': 4.0,
                    'font': 'Source Han Sans CN Regular',  # Use supported font
                    'color': '#FFFFFF',
                    'size': 30.0
                }
            ],
            'effects': [
                {
                    'type': 'filter',  # Use supported effect type
                    'name': 'brightness',
                    'start': 0.0,
                    'end': 1.0
                }
            ],
            'audio': {
                'add_music': False,
                'music_volume': 0.3
            },
            'color_grading': {
                'brightness': 0.0,
                'contrast': 0.0,
                'saturation': 0.0
            },
            'video_info': video_info,
            'target_duration': target_duration,
            'style': style
        }
    
    def _generate_default_suggestions(self, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate basic suggestions when AI analysis fails
        """
        
        duration = float(video_info.get('duration', 0))
        
        suggestions = []
        
        if duration > 120:
            suggestions.append("Video is long - consider creating highlights or multiple shorter clips")
        if duration < 15:
            suggestions.append("Short video - perfect for social media with minimal editing")
        
        # Basic content type detection
        width = float(video_info.get('width', 16))
        height = float(video_info.get('height', 9))
        aspect_ratio = width / height
        
        if abs(aspect_ratio - (9/16)) < 0.1:
            suggestions.append("Vertical format detected - ideal for TikTok/Instagram Stories")
        elif abs(aspect_ratio - (16/9)) < 0.1:
            suggestions.append("Horizontal format - good for YouTube or general use")
        
        return {
            'suggestions': suggestions,
            'recommended_style': 'social_media' if duration < 60 else 'highlight_reel',
            'content_type': 'general',
            'complexity_score': 'medium'
        }
    
    def _parse_text_analysis(self, response_text: str, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse AI response when JSON parsing fails
        """
        
        # Basic text parsing fallback
        suggestions = []
        recommended_style = "auto"
        
        if "social media" in response_text.lower():
            recommended_style = "social_media"
        elif "highlight" in response_text.lower():
            recommended_style = "highlight_reel"
        elif "tutorial" in response_text.lower():
            recommended_style = "tutorial"
        
        # Extract suggestions from text
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                suggestions.append(line[1:].strip())
        
        return {
            'suggestions': suggestions[:5],  # Limit to 5 suggestions
            'recommended_style': recommended_style,
            'content_type': 'general',
            'raw_response': response_text
        }