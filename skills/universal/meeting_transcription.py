class MeetingTranscription:
    def __init__(self): pass
    def transcribe(self, audio_file: str) -> Dict: return {"status": "ready"}

SKILL_NAME = "meeting_transcription"
SKILL_DESCRIPTION = "Transcribe and summarize meeting recordings"
