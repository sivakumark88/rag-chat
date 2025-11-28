# RAG Chat Frontend

A simple, beginner-friendly web interface for the RAG Chat application.

## Features

- 💬 Clean chat interface
- 📱 Responsive design
- 🎨 Modern UI with gradient background
- 📚 Shows document sources used for answers
- ⚡ Real-time responses
- 🔄 Loading indicators

## How to Use

### Option 1: Open Directly (Simplest)

1. Make sure your backend is running:
   ```bash
   cd ../backend
   uvicorn app:app --reload --port 8000
   ```

2. Open `index.html` in your browser:
   - Double-click the file, OR
   - Right-click → Open with → Your browser

### Option 2: Use a Simple HTTP Server

```bash
# Using Python
python -m http.server 3000

# Using Node.js
npx http-server -p 3000
```

Then visit: http://localhost:3000

## Configuration

The frontend connects to the backend at `http://127.0.0.1:8000/api/ask`

To change this, edit the `API_URL` in `index.html`:
```javascript
const API_URL = 'http://127.0.0.1:8000/api/ask';
```

## CORS Setup

Make sure your backend allows CORS. Add this to your `backend/app.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Browser Support

Works on all modern browsers:
- ✅ Chrome/Edge
- ✅ Firefox
- ✅ Safari
