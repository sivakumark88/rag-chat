# UI
<img width="1424" height="907" alt="Screenshot 2025-11-28 at 5 26 06 PM" src="https://github.com/user-attachments/assets/f0859fac-1420-47bd-a6f4-a78d8f1f2b74" />

# RAG Chat System

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based on your documentation using FAISS vector search and OpenAI's GPT models.

## 📁 Project Structure

```
rag-chat/
├── backend/           # FastAPI backend
│   ├── app.py        # Main API server
│   ├── ingest.py     # Document ingestion script
│   ├── requirements.txt
│   └── db/           # Vector database (auto-generated)
│       ├── index.faiss
│       └── meta.pkl
├── frontend/         # HTML/CSS/JS frontend
│   └── index.html
├── docs/            # Your documentation files (.txt, .md)
└── README.md
```

## 🚀 Quick Start

### 1. Environment Setup

**Prerequisites:**
- Python 3.11 (conda environment recommended)
- OpenAI API Key

**Create Conda Environment:**
```bash
conda create -n rag python=3.11
conda activate rag
```

**Install Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Set Up OpenAI API Key:**
Create a `.env` file in the `backend/` directory:
```bash
cd backend
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### 2. Ingest Your Documents

Add your documentation files (`.txt` or `.md`) to the `docs/` directory, then run:

```bash
cd backend
python ingest.py
```

This will:
- Automatically detect all `.txt` and `.md` files in `../docs/`
- Split them into chunks (300 words with 50 word overlap)
- Generate embeddings using `sentence-transformers`
- Store vectors in `db/index.faiss` and metadata in `db/meta.pkl`

**Manual file selection (optional):**
```bash
python ingest.py ../docs/file1.txt ../docs/file2.md
```

**Re-ingesting:** If you add/modify documents, simply run `python ingest.py` again to rebuild the vector database.

### 3. Start the Backend Server

```bash
cd backend
uvicorn app:app --reload --port 8000
```

Or if using conda environment:
```bash
/opt/homebrew/Caskroom/miniconda/base/envs/rag/bin/python -m uvicorn app:app --reload --port 8000
```

Backend will be available at: `http://127.0.0.1:8000`

**API Endpoint:**
- `POST /api/ask` - Send questions and get answers
  ```json
  {
    "q": "Your question here"
  }
  ```

### 4. Start the Frontend

Open a new terminal:

```bash
cd frontend
python3 -m http.server 3001
```

Access the chat interface at: `http://localhost:3001`

## 🎯 How It Works

1. **Document Ingestion:**
   - Documents are split into overlapping chunks
   - Each chunk is converted to a 384-dimensional vector using `all-MiniLM-L6-v2`
   - Vectors are stored in FAISS index for fast similarity search

2. **Query Processing:**
   - User question is converted to a vector
   - FAISS finds top 3-5 most similar document chunks
   - Retrieved chunks are sent to OpenAI GPT-4o-mini as context
   - LLM generates a comprehensive answer

3. **Response Rendering:**
   - Frontend displays answers with markdown formatting
   - Source documents are shown for transparency

## 🛠️ Configuration

### Backend (`backend/app.py`)

**Adjust retrieval count:**
```python
ctxs = search(body.q, k=5)  # Retrieve top 5 chunks (default: 3)
```

**Change LLM model:**
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Options: gpt-4, gpt-4o, gpt-3.5-turbo
    max_tokens=300,       # Increase for longer responses
)
```

### Ingestion (`backend/ingest.py`)

**Adjust chunk size:**
```python
def chunk(text, size=300, overlap=50):  # 300 words per chunk, 50 word overlap
```

## 📝 Adding New Documents

1. Add `.txt` or `.md` files to `docs/` directory
2. Run ingestion: `cd backend && python ingest.py`
3. Restart backend server (if not using `--reload`)

## 🐛 Troubleshooting

**"ModuleNotFoundError":**
- Ensure you're in the conda environment: `conda activate rag`
- Install dependencies: `pip install -r requirements.txt`

**"No such file or directory: db/index.faiss":**
- Run `python ingest.py` first to create the vector database

**"Internal Server Error" from API:**
- Check OpenAI API key is set in `.env` file
- Verify backend server logs for detailed error messages

**Frontend shows "messy" text:**
- Clear browser cache and refresh
- Ensure `marked.js` library is loaded in `index.html`

**CORS errors:**
- Backend has CORS enabled for all origins (already configured)
- Make sure frontend is served via HTTP server (not `file://`)

## 📊 System Requirements

- **Embedding Model:** sentence-transformers/all-MiniLM-L6-v2 (~100MB)
- **Vector DB:** FAISS (CPU version)
- **LLM:** OpenAI API (requires API key)
- **Memory:** ~500MB for typical document collections

## 🔧 Tech Stack

- **Backend:** FastAPI, FAISS, sentence-transformers, OpenAI API
- **Frontend:** Vanilla HTML/CSS/JavaScript with marked.js
- **Vector DB:** FAISS (IndexFlatIP with cosine similarity)
- **Embeddings:** all-MiniLM-L6-v2 (384 dimensions)
- **LLM:** OpenAI GPT-4o-mini

## 📚 Example Usage

1. Start backend: `cd backend && uvicorn app:app --reload --port 8000`
2. Start frontend: `cd frontend && python3 -m http.server 3001`
3. Open browser: `http://localhost:3001`
4. Ask questions about your documentation!

---

**Note:** This system uses OpenAI's API which requires an active API key and may incur costs based on usage.
