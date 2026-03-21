# app/embedding/embedder.py

from sentence_transformers import SentenceTransformer

# ✅ Load model once (global - avoids reloading every time)
model = SentenceTransformer("all-MiniLM-L12-v2")


def embed_chunks(chunks):
    """
    chunks: [{ "text": str, "metadata": {...} }]
    returns: [{ "embedding": vector, "metadata": {...} }]
    """

    texts = [chunk["text"] for chunk in chunks]

    # 🔥 Convert text → vectors
    embeddings = model.encode(texts, show_progress_bar=False)

    embedded_data = []

    for i, chunk in enumerate(chunks):
        embedded_data.append({
            "id": chunk["id"],
            "text": chunk["text"], 
            "embedding": embeddings[i].tolist(),
            "metadata": chunk["metadata"]
        })

    return embedded_data