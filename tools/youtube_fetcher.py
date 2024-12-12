# tools/youtube_fetcher.py
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

def fetch_transcript(video_id):
    """
    Attempts to fetch the transcript for a given YouTube video_id.
    Returns:
        transcript_text (str) if found, else None.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text
    except Exception as e:
        print(f"No transcript found: {e}")
        return None

def get_audio_stream_url(video_url):
    """
    Given a YouTube video URL, return the audio-only stream URL.
    """
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    return audio_stream.url
