from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import faiss, pickle, numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load vector DB
index = faiss.read_index("db/index.faiss")
metas = pickle.load(open("db/meta.pkl", "rb"))

# Embedding model
embed = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI()

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    q: str

def search(q, k=3):
    q_emb = embed.encode(q).astype("float32")
    faiss.normalize_L2(q_emb.reshape(1, -1))
    D, I = index.search(q_emb.reshape(1, -1), k)
    return [metas[i] for i in I[0]]

def build_prompt(q, ctxs):
    txt = "\n\n".join([c["text"] for c in ctxs])
    return f"""You are a helpful AI assistant with expertise in HIP (Hosted Infrastructure Platform) and Kubernetes.

Answer the question using the provided context below. If the context contains relevant information, use it as your primary source. You can supplement with your general knowledge to provide a clearer, more complete answer.

If the context doesn't contain any relevant information about the question, you can provide a general answer based on your knowledge, but mention that the specific documentation wasn't found.

Context from documentation:
{txt}

Question: {q}

Answer:"""

@app.post("/api/ask")
def ask(body: Query):
    ctxs = search(body.q, k=3)  # Retrieve top 5 chunks instead of 3
    prompt = build_prompt(body.q, ctxs)

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )

    answer = response.choices[0].message.content
    return {"answer": answer, "context": ctxs}
