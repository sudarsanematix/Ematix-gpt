import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-20b"

def run_agent(role: str, task: str) -> str:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": role},
            {"role": "user", "content": task}
        ]
    )
    return response.output_text

def research_agent(topic: str) -> str:
    role = """You are a Research agent. Your responsibility is to research a topic given by the user.
Explain:
- what it is
- how it will work
- important concepts
- pros and cons"""
    task = f"Research this topic: {topic}"
    return run_agent(role, task)

def analysis_agent(topic: str, research: str) -> str:
    role = """You are an analysis agent. You need to analyze a research provided by the research agent.
Identify:
- important findings
- technical insights
- pros and cons"""
    task = f"topic: {topic}\n\nResearch Agent output:\n{research}\n\nAnalyze the above research."
    return run_agent(role, task)

def run_multi_agent(topic: str):
    research = research_agent(topic)
    analysis = analysis_agent(topic, research)
    return {"research": research, "analysis": analysis}
