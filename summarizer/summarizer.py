import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class Summarizer:
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

    def summarize(self, text):
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": f"Summarize the following text in a concise and informative paragraph:\n\n{text}"}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[ERROR] Summarization failed: {e}")
            return "❌ Could not generate summary."

    def summarize_with_metadata(self, text, metadata):
        title = metadata.get("title", "")
        description = metadata.get("description", "")
        tags = ", ".join(metadata.get("tags", []))

        prompt = f"""
        You are given a YouTube video's transcript and metadata.
        Title: {title}
        Description: {description}
        Tags: {tags}

        Transcript:
        {text}

        Provide a concise and informative summary considering the above metadata.
        """

        return self.summarize(prompt)
