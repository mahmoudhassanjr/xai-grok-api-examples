from dotenv import load_dotenv
from openai import OpenAI
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
import constants

def setup_env():
    load_dotenv()
    XAI_API_KEY = os.getenv("XAI_API_KEY")
    base_url = constants.BASE_URL_V1
    client = OpenAI(api_key = XAI_API_KEY, base_url = base_url)
    return client
    
if __name__ == "__main__":
    client = setup_env()
    model = models.GROK
    messages = [
        {"role": "system", "content": "You are a PhD-level mathematician."},
        {"role": "user", "content": "What is 2 + 2?"}
    ]

    completion = client.chat.completions.create(model = model, messages = messages)

    print(completion.choices[0].message.content)