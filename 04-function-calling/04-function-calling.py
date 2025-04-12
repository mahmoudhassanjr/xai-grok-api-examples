from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from pydantic import BaseModel , Field
from typing import Literal
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
import constants

class TemperatureRequest(BaseModel):
    location: str = Field(description = "The city and state, e.g. San Francisco, CA")
    unit: Literal["celsius", "fahrenheit"] = Field(
        "celsius", description = "Temperature unit"
    )

class CeilingRequest(BaseModel):
    location: str = Field(description = "The city and state, e.g. San Francisco, CA")

def get_current_temperature(**kwargs):
    request = TemperatureRequest(**kwargs)
    temperature: int

    if request.unit.lower() == "fahrenheit":
        temperature = 59
    elif request.unit.lower() == "celsius":
        temperature = 15
    else:
        raise ValueError("unit must be one of fahrenheit or celsius")
    
    return {
        "location": request.location,
        "temperature": temperature,
        "unit": "fahrenheit"
    }

def get_current_ceiling(**kwargs):
    request = CeilingRequest(**kwargs)
    return {
        "location": request.location,
        "ceiling": 15000,
        "ceiling_type": "broken",
        "unit": "ft"
    }

get_current_temperature_schema = TemperatureRequest.model_json_schema()
get_current_ceiling_schema = CeilingRequest.model_json_schema()

tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "get_current_temperature",
            "description": "Get the current temperature in a given location",
            "parameters": get_current_temperature_schema
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_ceiling",
            "description": "Get the current cloud ceiling in a given location",
            "parameters": get_current_ceiling_schema
        }
    }
]

tools_map = {
    "get_current_temperature": get_current_temperature,
    "get_current_ceiling": get_current_ceiling
}

def setup_env():
    load_dotenv()
    XAI_API_KEY = os.getenv("XAI_API_KEY")

    client = OpenAI(api_key = XAI_API_KEY, base_url=constants.BASE_URL_V1)

    return client

def send_request():
    client = setup_env()
    messages = [{"role": "user", "content": "What's the temperature like in Paris?"}]
    response = client.chat.completions.create(
        model = models.GROK_MINI,
        messages = messages,
        tools = tools_definition,
        tool_choice = "auto"
    )

    print(response.choices[0].message)

    messages.append(response.choices[0].message)
    
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            result = tools_map[function_name](**function_args)

            messages.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })

    response = client.chat.completions.create(model = models.GROK_MINI, messages = messages, tools = tools_definition, tool_choice = "auto")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    send_request()