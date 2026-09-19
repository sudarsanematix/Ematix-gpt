import os
import numpy as np
from openai import OpenAI
from pypdf import PdfReader
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

hf_key = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
hf_client = InferenceClient(api_key=hf_key)

MODEL = "openai/gpt-oss-20b"

def get_embeddings(texts: list) -> np.ndarray:
    # Use Hugging Face Inference API for embeddings instead of local sentence-transformers
    # to save memory on Render.
    embeddings = []
    for text in texts:
        # Note: Depending on the text length, you might want to batch this.
        # But for basic RAG, we can process one by one.
        res = hf_client.feature_extraction(text, model="sentence-transformers/all-MiniLM-L6-v2")
        embeddings.append(res)
    return np.array(embeddings).astype("float32")

def cosine_similarity(a, b):
    # Basic cosine similarity replacing FAISS
    return np.dot(a, b.T) / (np.linalg.norm(a, axis=1)[:, None] * np.linalg.norm(b, axis=1))

def process_pdf_and_query(file_path: str, question: str) -> str:
    # Extract text
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
        
    # Chunks
    chunks = [chunk for chunk in text.split("\n\n") if chunk.strip()]
    if not chunks:
        return "No text could be extracted from the PDF."

    # Generate Embeddings via Cloud API
    doc_embeddings = get_embeddings(chunks)
    query_embedding = get_embeddings([question])

    # Calculate similarity without FAISS
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    
    # Get top 3 indices
    top_k = min(3, len(chunks))
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    context = ""
    for i in top_indices:
        context += chunks[i] + "\n\n"

    # LLM via Groq
    prompt = f"Answer the question using the context below\n\nContext:\n{context}\n\nQuestion:\n{question}"
    response = client.responses.create(
        model=MODEL,
        input=prompt
    )
    return response.output_text
