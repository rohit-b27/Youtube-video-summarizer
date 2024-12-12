# app.py
from flask import Flask, request, render_template
from dotenv import load_dotenv
import os

from tools.youtube_fetcher import fetch_transcript, get_audio_stream_url
from tools.youtube_metadata import fetch_video_metadata
from transcriber.transcriber import transcribe_audio
from summarizer.summarizer import Summarizer

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", summary="No URL provided", transcript="")

        # Extract video_id
        # A basic method: split by "v=" and take last part
        video_id = url.split("v=")[-1]

        # Fetch transcript
        transcript = fetch_transcript(video_id)

        if not transcript:
            # No transcript available, fallback to transcription
            audio_url = get_audio_stream_url(url)
            transcript = transcribe_audio(audio_url)

        # Fetch metadata (optional step)
        metadata = fetch_video_metadata(video_id)
        
        summarizer = Summarizer()
        if metadata:
            summary = summarizer.summarize_with_metadata(transcript, metadata)
        else:
            summary = summarizer.summarize(transcript)

        return render_template("index.html", summary=summary, transcript=transcript)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
