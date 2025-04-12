import asyncio
import os
from asyncio import Semaphore
from typing import List
from openai import AsyncOpenAI
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
import constants

load_dotenv()
client = AsyncOpenAI(api_key = os.getenv("XAI_API_KEY"), base_url = constants.BASE_URL_V1)

async def send_request(sem: Semaphore, request: str) -> dict:
    async with sem:
        return await client.chat.completions.create(
            model = models.GROK_MINI,
            messages = [{"role": "user", "content": request}]
        )

async def process_requests(requests: List[str], max_concurrent: int = 2) -> List[dict]:
    sem = Semaphore(max_concurrent)
    tasks = [send_request(sem, request) for request in requests]
    return await asyncio.gather(*tasks)

async def main() -> None:
    requests = [
        "Tell me a joke",
        "Write a funny haiku",
        "Generate a funny X post",
        "Say something unhinged"
    ]

    responses = await process_requests(requests)

    for i, response in enumerate(responses):
        print(f"# response {i}")
        print(response.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())