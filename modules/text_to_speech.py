from gtts import gTTS
import tempfile

def text_to_audio(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        raise RuntimeError(f"Text-to-speech conversion failed: {e}")
