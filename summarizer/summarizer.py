# summarizer/summarizer.py
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Summarizer:
    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7,model = "gpt-4o-mini")

    def summarize(self, text):
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Summarize the following text in a concise manner:\n\n{text}"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(text=text).strip()

    def summarize_with_metadata(self, text, metadata):
        title = metadata.get("title", "")
        description = metadata.get("description", "")
        tags = ", ".join(metadata.get("tags", []))

        prompt_text = f"""
        The following is the transcript of a YouTube video:
        Title: {title}
        Description: {description}
        Tags: {tags}

        Summarize the transcript below, using the above context for better accuracy:

        {text}
        """
        prompt = PromptTemplate(
            input_variables=["text"],
            template="{text}"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(text=prompt_text).strip()
