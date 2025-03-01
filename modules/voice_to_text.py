import os
import io
import tempfile
import openai
from pydub import AudioSegment
from utils import config

# Set ffmpeg and ffprobe paths dynamically based on the environment.
if os.path.exists("/opt/homebrew/bin/ffmpeg"):
    AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"
    AudioSegment.ffprobe = "/opt/homebrew/bin/ffprobe"
elif os.path.exists("/usr/bin/ffmpeg"):
    AudioSegment.converter = "/usr/bin/ffmpeg"
    AudioSegment.ffprobe = "/usr/bin/ffprobe"
else:
    # Optionally, print a warning or let pydub use its default search.
    print("Warning: ffmpeg not found in the expected paths.")

def transcribe_audio(audio_data, language="en-US"):
    try:
        openai.api_key = config.OPENAI_API_KEY
        # Convert audio bytes to an AudioSegment
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
        # Export audio to MP3 for Whisper API
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            audio_segment.export(temp_file.name, format="mp3")
            temp_file.seek(0)
            with open(temp_file.name, "rb") as f:
                transcript_response = openai.Audio.transcribe("whisper-1", f)
        return transcript_response.get("text", "")
    except Exception as e:
        raise RuntimeError(f"Voice-to-text transcription failed: {e}")
