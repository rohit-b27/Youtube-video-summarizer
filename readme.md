# 🎥 YouTube Video Summarizer App

A Flask-based web application that summarizes YouTube videos using transcript extraction or local audio transcription. Built with LangChain, LLMs (OpenAI/Groq), and Whisper-based models.

---

## 🚀 Features

- 🔗 Accepts YouTube video URL input
- 📄 Automatically fetches transcript (if available)
- 🔊 Falls back to audio extraction + transcription using `faster-whisper`
- 🧠 Summarizes content using LLMs (Groq, OpenAI, etc.)
- ⚡ Fast, reliable, and cost-efficient (can run fully offline!)

---

## 🛠️ Tech Stack

- **Backend**: Flask, Python
- **Transcription**: [`faster-whisper`](https://github.com/guillaumekln/faster-whisper), `yt-dlp`, `ffmpeg`
- **Summarization**: LangChain + Chat LLMs ( LLaMA 3 via Groq)
- **Optional**: Use [Deepgram](https://www.deepgram.com) API for fast cloud transcription
- **Frontend**: HTML/CSS (templated)

---

## 📦 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/youtube-video-summarizer.git
   cd youtube-video-summarizer


## Set up Python environment

conda create -n youtube_env python=3.10
conda activate youtube_env
pip install -r requirements.txt


## Create a .env file

OPENAI_API_KEY=your_openai_key         # optional
GROQ_API_KEY=your_groq_key             # for summarization
DEEPGRAM_API_KEY=your_deepgram_key     # optional alternative to whisper



## Ensure ffmpeg is installed

Download: https://ffmpeg.org/download.html

Add the ffmpeg/bin path to your system PATH