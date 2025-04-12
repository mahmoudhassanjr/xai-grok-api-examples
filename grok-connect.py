from openai import OpenAI
from dotenv import dotenv_values
import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
import constants

if __name__ == "__main__": 
    config = dotenv_values(".env")

    client = OpenAI(api_key=config["XAI_API_KEY"], base_url=constants.BASE_URL_V1)

    completion = client.chat.completions.create(model=models.GROK,
                                                messages = [{
                                                    "role": "system",
                                                    "content": "You are Grok, a chatbot inspired by the Hitchhiker's Guide to the Galaxy. You answer every question in 1 sentence."
                                                },
                                                {
                                                    "role": "user",
                                                    "content": "What is the meeaning of life, the universe, and everything?"
                                                },])

    print(completion.choices[0].message.content)