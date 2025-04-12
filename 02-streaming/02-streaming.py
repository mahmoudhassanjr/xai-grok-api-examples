import os
from openai import OpenAI
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
import constants

def setup_env():
    load_dotenv()
    XAI_API_KEY = os.getenv("XAI_API_KEY")
    client = OpenAI(api_key=XAI_API_KEY, base_url = constants.BASE_URL_V1)
    return client

if __name__ == "__main__":
    client = setup_env()
    messages = [
        {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
        {"role": "user", "content": "What is the meaning of life, the universe, and everything?"}
    ]

    stream = client.chat.completions.create(
        model = models.GROK,
        messages = messages,
        stream = True
    )

    for chunk in stream: 
        print(chunk.choices[0].delta.content, end="", flush=True)