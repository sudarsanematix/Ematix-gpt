import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import faiss
import numpy as np
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-20b"
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

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

    # Embeddings
    embeddings = embed_model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    # Vector DB
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Retrieve
    query_embedding = embed_model.encode([question])
    distance, ids = index.search(np.array(query_embedding).astype("float32"), min(3, len(chunks)))

    context = ""
    for i in ids[0]:
        if i < len(chunks):
            context += chunks[i] + "\n\n"

    # LLM
    prompt = f"Answer the question using the context below\n\nContext:\n{context}\n\nQuestion:\n{question}"
    response = client.responses.create(
        model=MODEL,
        input=prompt
    )
    return response.output_text
