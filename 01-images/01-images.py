import os
from openai import OpenAI
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
import constants

load_dotenv()
XAI_API_KEY = os.getenv("XAI_API_KEY")
image_url = "https://science.nasa.gov/wp-content/uploads/2023/09/web-first-images-release.png"

client = OpenAI(api_key = XAI_API_KEY, base_url = constants.BASE_URL_V1)

messages = [{
    "role": "user",
    "content": [
        {
            "type": "image_url",
            "image_url": {
                "url": image_url,
                "detail": "high",
            },
        },
        {
            "type": "text",
            "text": "What's in this image?"
        }
    ]
}]

completion = client.chat.completions.create(
    model=models.GROK_VISION,
    messages = messages,
    temperature=0.01
)

print(completion.choices[0].message.content)