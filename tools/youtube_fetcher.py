from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import re

def extract_video_id(url_or_id):
    if len(url_or_id) == 11 and "http" not in url_or_id:
        return url_or_id

    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url_or_id)
    if match:
        return match.group(1)

    raise ValueError("Invalid YouTube URL or ID")

def fetch_transcript(url_or_id):
    try:
        video_id = extract_video_id(url_or_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text
    except Exception as e:
        print(f"[Transcript] Not available: {e}")
        return None

def get_audio_stream_url(url):
    from yt_dlp import YoutubeDL
    try:
        ydl_opts = {
            'format': 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio/best',
            'quiet': True,
            'skip_download': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']
    except Exception as e:
        print(f"[yt_dlp] Failed to fetch audio stream: {e}")
        return None
