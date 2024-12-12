import whisper
import requests
import os

def transcribe_audio(audio_url):
    """
    Download audio from audio_url and transcribe it using Whisper.
    """
    model = whisper.load_model("base")
    temp_filename = "temp_audio.mp3"
    
    # Download the audio
    response = requests.get(audio_url)
    with open(temp_filename, "wb") as f:
        f.write(response.content)

    # Transcribe
    result = model.transcribe(temp_filename)
    transcript = result["text"]

    # Clean up
    os.remove(temp_filename)
    return transcript