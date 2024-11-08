from restack_ai.function import function
from restack_ai import log
from openai import OpenAI
from dataclasses import dataclass
from pydantic import BaseModel
import os

@dataclass
class ResponseFormat:
    name: str
    description: str
    schema: dict

@dataclass
class FunctionInputParams:
    user_content: str
    system_content: str | None = None
    model: str | None = None

@function.defn(name="OpenaiGreet")
async def openai_greet(input: FunctionInputParams) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    messages = []
    if input.system_content:
        messages.append({"role": "system", "content": input.system_content})
    messages.append({"role": "user", "content": input.user_content})

    response = client.chat.completions.create(
        model=input.model or "gpt-4o-mini",
        messages=messages,
        response_format={
            "json_schema": {
                "name": "greet",
                "description": "Greet a person",
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"}
                    },
                    "required": ["message"]
                }
            },
            "type": "json_schema",
        },
    )
    log.info("Response", response=response)
    return response.choices[0].message.content
