from app.features.embedding.embedder import model
import app.repositories as faiss_store
import numpy as np


def search_query(query: str, k: int = 5):
    # 🔹 Step 1: Embed query
    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype("float32")

    # 🔹 Step 2: Search FAISS
    D, I = faiss_store.index.search(query_vector, k)

    results = []

    # 🔹 Step 3: Map results
    for i, idx in enumerate(I[0]):
        if idx == -1:
            continue

        chunk = faiss_store.metadata_store[idx]

        results.append({
            "content": chunk["text"],
            "score": float(D[0][i]),

            "file_name": chunk["metadata"]["file_name"],
            "file_type": chunk["metadata"]["file_type"],

            "page_number": chunk["metadata"]["page_number"],
            "slide_number": chunk["metadata"]["slide_number"],

            "line_start": chunk["metadata"]["line_start"],
            "line_end": chunk["metadata"]["line_end"]
        })

    return results