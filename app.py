from flask import Flask, request, render_template
from dotenv import load_dotenv
import os

from tools.youtube_fetcher import fetch_transcript, get_audio_stream_url
from tools.youtube_metadata import fetch_video_metadata
from transcriber.transcriber import transcribe_audio
from summarizer.summarizer import Summarizer

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url_or_id = request.form.get("url")
        if not url_or_id:
            return render_template("index.html", summary="❌ No YouTube URL provided.", transcript="")

        try:
            print("[STEP 1] Fetching transcript using YouTubeTranscriptApi...")
            transcript = fetch_transcript(url_or_id)

            if not transcript:
                print("[STEP 2] No transcript found. Trying audio extraction...")
                audio_url = get_audio_stream_url(url_or_id)
                if not audio_url:
                    print("[ERROR] Could not extract audio stream.")
                    return render_template("index.html", summary="❌ Could not extract audio stream from the video.", transcript="")

                print("[STEP 3] Starting transcription from audio...")
                transcript = transcribe_audio(audio_url)
                print("[STEP 4] Transcription complete.")

            if not transcript:
                return render_template("index.html", summary="❌ Transcript could not be generated.", transcript="")

            print("[STEP 5] Fetching metadata...")
            metadata = fetch_video_metadata(url_or_id)

            print("[STEP 6] Generating summary...")
            summarizer = Summarizer()
            if metadata:
                summary = summarizer.summarize_with_metadata(transcript, metadata)
            else:
                summary = summarizer.summarize(transcript)

            print("[DONE] Summary generated.")
            return render_template("index.html", summary=summary, transcript=transcript)

        except Exception as e:
            print(f"[FATAL ERROR] {e}")
            return render_template("index.html", summary=f"❌ Unexpected error: {e}", transcript="")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
