##python ingest.py ../docs/*.txt ../docs/*.md
import pickle, numpy as np, faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
import glob

EMBED = "all-MiniLM-L6-v2"
DIM = 384

def chunk(text, size=300, overlap=50):
    words = text.split()
    out, i = [], 0
    while i < len(words):
        out.append(" ".join(words[i:i+size]))
        i += size - overlap
    return out

def ingest(files):
    model = SentenceTransformer(EMBED)
    vectors, metas = [], []

    for f in files:
        content = Path(f).read_text()
        for i, c in enumerate(chunk(content)):
            emb = model.encode(c)
            vectors.append(emb)
            metas.append({"source": f, "chunk": i, "text": c})

    vectors = np.array(vectors).astype("float32")
    faiss.normalize_L2(vectors)

    index = faiss.IndexFlatIP(DIM)
    index.add(vectors)

    Path("db").mkdir(exist_ok=True)
    faiss.write_index(index, "db/index.faiss")
    pickle.dump(metas, open("db/meta.pkl", "wb"))

    print("Done. Vectors:", len(metas))

if __name__ == "__main__":
    import sys
    
    # If no files provided, automatically find all .txt and .md files
    if len(sys.argv) < 2:
        files = glob.glob("../docs/*.txt") + glob.glob("../docs/*.md")
        print(f"Auto-detecting documents: {len(files)} files found")
    else:
        files = sys.argv[1:]
    
    if not files:
        print("No documents found. Add .txt or .md files to ../docs/")
        sys.exit(1)
    
    print(f"Ingesting {len(files)} documents...")
    ingest(files)
