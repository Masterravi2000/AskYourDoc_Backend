# app/embedding/embedder.py
import os
import sys
from sentence_transformers import SentenceTransformer
from app.repositories.status_store_repository import set_status

if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.abspath(".")

MODEL_PATH = os.path.join(BASE_DIR, "models", "all-MiniLM-L12-v2")

model = SentenceTransformer(MODEL_PATH)


def embed_chunks(fileId: str, chunks):
    """
    chunks: [{ "id": str, "text": str, "metadata": {...} }]
    returns: [{ "id": str, "text": str, "vector": vector, "metadata": {...} }]
    """
    # start = time.perf_counter()
    
    # set status
    filename = chunks[0]["metadata"]["file_name"]
    set_status(fileId, filename, "embedding")

    texts = [chunk["text"] for chunk in chunks]

    # 🔥 Convert text → vectors
    vectors = model.encode(texts, show_progress_bar=False)
    
    # elapsed = time.perf_counter() - start

    embedded_data = []

    for i, chunk in enumerate(chunks):
        embedded_data.append({
            "id": chunk["id"],
            "text": chunk["text"], 
            "vector": vectors[i].tolist(),
            "metadata": chunk["metadata"]
        })
    
    # print(f"Total embeddings: {len(embedded_data)}")
    # print(f"[Embedding] Completed in {elapsed:.3f} sec")
    # print(f"Time per chunk: {elapsed / len(embedded_data):.3f} sec")

    return embedded_data