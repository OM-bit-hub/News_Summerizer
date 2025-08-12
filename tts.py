from gtts import gTTS
from io import BytesIO

LANG_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr"
}

def text_to_speech(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        return audio_data
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

