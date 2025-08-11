"""
AI Director - Uses Anthropic API to make intelligent video editing decisions
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    import anthropic
except ImportError:
    raise ImportError("Please install anthropic: pip install anthropic")

class AIDirector:
    def __init__(self, config):
        self.config = config
        
        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY') or config.get('anthropic_api_key')
        if not api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable or add to config.")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = config.get('anthropic_model', 'claude-3-sonnet-20240229')
        
        # Load editing prompts
        self.load_prompts()
    
    def load_prompts(self):
        """Load AI prompts for different editing tasks"""
        
        prompts_path = Path("config/prompts/editing_prompts.json")
        if prompts_path.exists():
            with open(prompts_path, 'r') as f:
                self.prompts = json.load(f)
        else:
            # Default prompts
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
        
        prompt = self.prompts["analyze_video"].format(
            video_info=json.dumps(video_info, indent=2)
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
                    analysis['suggestions'] = self._generate_default_suggestions(video_info)
                
                return analysis
                
            except json.JSONDecodeError:
                # Fallback to text parsing
                return self._parse_text_analysis(response_text, video_info)
                
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")
            return self._generate_default_suggestions(video_info)
    
    def create_editing_plan(self, video_info: Dict[str, Any], style: str = "auto",
                           target_duration: Optional[int] = None, quality: str = "1080p",
                           aspect_ratio: str = "16:9", add_music: bool = False,
                           auto_subtitles: bool = False) -> Dict[str, Any]:
        """
        Create a detailed editing plan using AI
        """
        
        # Auto-detect style if needed
        if style == "auto":
            analysis = self.analyze_for_editing(video_info)
            style = analysis.get('recommended_style', 'social_media')
        
        # Set target duration if not specified
        if not target_duration:
            if style == "social_media":
                target_duration = min(60, video_info['duration'] * 0.7)
            elif style == "highlight_reel":
                target_duration = min(90, video_info['duration'] * 0.5)
            else:
                target_duration = video_info['duration'] * 0.8
        
        prompt = self.prompts["create_editing_plan"].format(
            video_info=json.dumps(video_info, indent=2),
            style=style,
            duration=target_duration,
            add_music=add_music,
            auto_subtitles=auto_subtitles,
            quality=quality,
            aspect_ratio=aspect_ratio
        )
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system="You are an expert video editor creating editing plans for CapCut. Provide detailed, actionable editing instructions as JSON.",
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            response_text = message.content[0].text
            
            # Parse the editing plan
            try:
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                else:
                    json_text = response_text.strip()
                
                editing_plan = json.loads(json_text)
                
                # Validate and enhance the plan
                editing_plan = self._validate_editing_plan(editing_plan, video_info)
                
                return editing_plan
                
            except json.JSONDecodeError:
                return self._create_fallback_plan(video_info, style, target_duration)
                
        except Exception as e:
            print(f"⚠️ AI planning failed: {e}")
            return self._create_fallback_plan(video_info, style, target_duration)
    
    def _validate_editing_plan(self, plan: Dict[str, Any], video_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and enhance the AI-generated editing plan
        """
        
        video_duration = video_info.get('duration', 30)
        
        # Ensure cuts don't exceed video duration
        if 'cuts' in plan:
            valid_cuts = []
            for cut in plan['cuts']:
                start = max(0, cut.get('start', 0))
                end = min(video_duration, cut.get('end', video_duration))
                if start < end:
                    valid_cuts.append({'start': start, 'end': end})
            plan['cuts'] = valid_cuts
        
        # Validate text elements timing
        if 'text_elements' in plan:
            for text_elem in plan['text_elements']:
                text_elem['start'] = max(0, text_elem.get('start', 0))
                text_elem['end'] = min(video_duration, text_elem.get('end', 5))
        
        # Add video_info to plan for reference
        plan['video_info'] = video_info
        plan['target_duration'] = plan.get('target_duration', video_duration * 0.8)
        
        return plan
    
    def _create_fallback_plan(self, video_info: Dict[str, Any], style: str, 
                             target_duration: int) -> Dict[str, Any]:
        """
        Create a basic editing plan when AI fails
        """
        
        video_duration = video_info.get('duration', 30)
        
        # Basic cuts for highlight reel
        if style == "highlight_reel":
            cuts = [
                {'start': 0, 'end': min(10, video_duration)},
                {'start': max(0, video_duration * 0.3), 'end': min(video_duration * 0.3 + 15, video_duration)},
                {'start': max(0, video_duration * 0.7), 'end': min(video_duration * 0.7 + 10, video_duration)}
            ]
        elif style == "social_media":
            # Single cut for social media
            start_time = max(0, (video_duration - target_duration) / 2)
            cuts = [{'start': start_time, 'end': start_time + target_duration}]
        else:
            # Default: use most of the video
            cuts = [{'start': 0, 'end': min(target_duration, video_duration)}]
        
        return {
            'cuts': cuts,
            'text_elements': [
                {
                    'text': 'Edited with CapCut CLI',
                    'start': 1,
                    'end': 4,
                    'font': 'Arial',
                    'color': '#FFFFFF',
                    'size': 30.0
                }
            ],
            'effects': [
                {
                    'type': 'transition',
                    'name': 'fade',
                    'start': 0,
                    'end': 1
                }
            ],
            'audio': {
                'add_music': False,
                'music_volume': 0.3
            },
            'color_grading': {
                'brightness': 0,
                'contrast': 0,
                'saturation': 0
            },
            'video_info': video_info,
            'target_duration': target_duration,
            'style': style
        }
    
    def _generate_default_suggestions(self, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate basic suggestions when AI analysis fails
        """
        
        duration = video_info.get('duration', 0)
        
        suggestions = []
        
        if duration > 120:
            suggestions.append("Video is long - consider creating highlights or multiple shorter clips")
        if duration < 15:
            suggestions.append("Short video - perfect for social media with minimal editing")
        
        # Basic content type detection
        aspect_ratio = video_info.get('width', 16) / video_info.get('height', 9)
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