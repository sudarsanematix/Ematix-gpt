import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import shutil

from agents.multi_agent import run_multi_agent
from agents.rag_agent import process_pdf_and_query
from agents.web_search_agent import run_web_search
from agents.image_agent import query_image
from agents.multi_agent import run_agent

app = FastAPI(title="Multi-Agent Research System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str

class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    message: str

@app.post("/api/research")
async def research_endpoint(request: TopicRequest):
    try:
        result = run_multi_agent(request.topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/web-search")
async def web_search_endpoint(request: QueryRequest):
    try:
        result = run_web_search(request.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rag")
async def rag_endpoint(file: UploadFile = File(...), question: str = Form(...)):
    try:
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = process_pdf_and_query(file_path, question)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/image")
async def image_endpoint(request: QueryRequest):
    try:
        image_bytes = query_image(request.query)
        return Response(content=image_bytes, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        role = "You are a helpful AI chatbot capable of answering general questions."
        result = run_agent(role, request.message)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
