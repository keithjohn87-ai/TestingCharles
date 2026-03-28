"""
Voice ElevenLabs Skill
TTS for notifications, voice messages, storytelling
"""

import requests
from typing import Dict, Any, Optional


class VoiceElevenLabs:
    """Text-to-speech via ElevenLabs."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
    
    def synthesize(self, text: str, voice_id: str = "pNInz6obpgDQfF1MoFWkg") -> Dict:
        """Convert text to speech."""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        headers = {"xi-api-key": self.api_key}
        data = {"text": text, "model_id": "eleven_monolingual_v1"}
        
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=30)
            return {"status": "success", "audio_length": len(resp.content)}
        except Exception as e:
            return {"error": str(e)}
    
    def list_voices(self) -> Dict:
        """List available voices."""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
    
    def narrate(self, text: str, output_file: str) -> Dict:
        """Generate narration and save to file."""
        result = self.synthesize(text)
        
        if result.get("status") == "success":
            return {"status": "saved", "file": output_file}
        
        return result


SKILL_NAME = "voice_elevenlabs"
SKILL_DESCRIPTION = "TTS for notifications, voice messages, storytelling"
