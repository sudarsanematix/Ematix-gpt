import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-20b"

def run_web_search(query: str) -> str:
    response = client.responses.create(
        input=query,
        tools=[{"type": "browser_search"}],
        tool_choice="required",
        model=MODEL,
    )
    return response.output_text
