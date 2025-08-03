import os
import tempfile
from faster_whisper import WhisperModel
import yt_dlp


def download_audio_with_ytdlp(video_url, temp_dir):
    print("[INFO] Downloading audio using yt_dlp...")

    ffmpeg_path = "C:/ffmpeg-master-latest-win64-gpl-shared/bin"  # Use forward slashes or raw string

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_dir, 'audio.%(ext)s'),
        'quiet': True,
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            return os.path.join(temp_dir, 'audio.mp3')
    except Exception as e:
        print(f"[ERROR] yt_dlp failed: {e}")
        return None


def transcribe_audio(video_url, model_name="tiny"):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = download_audio_with_ytdlp(video_url, tmpdir)
            if not audio_path or not os.path.exists(audio_path):
                raise Exception("Audio download failed or file missing.")

            print(f"[INFO] Audio saved to: {audio_path}")
            print(f"[INFO] Loading faster-whisper model: {model_name}")

            model = WhisperModel(model_name, device="cpu", compute_type="int8")
            segments, info = model.transcribe(audio_path)

            transcript = " ".join([seg.text.strip() for seg in segments])
            print("[INFO] Transcription completed successfully.")
            return transcript

    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return None
