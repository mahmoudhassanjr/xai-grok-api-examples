import os
from openai import OpenAI
import base64
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
import constants

def setup_env():
    load_dotenv()
    XAI_API_KEY = os.getenv("XAI_API_KEY")
    client = OpenAI(api_key=XAI_API_KEY, base_url=constants.BASE_URL_V1)
    return client

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def process_image(image_path):
    base64_image = encode_image(image_path)

    messages = [
        {
            "role": "user",
            "content": [
                { "type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"} },
                { "type": "text", "text": "What's in this image?"}
            ]
        }
    ]
    
    return messages

def send_request(messages):
    client = setup_env()
    completion = client.chat.completions.create(model = models.GROK_VISION, messages = messages, temperature = 0.01)
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    image_path = os.getcwd() + "/01-images/man-image.png"
    print("Path: " + image_path)
    messages = process_image(image_path)
    send_request(messages)
