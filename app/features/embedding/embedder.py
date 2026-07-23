# app/embedding/embedder.py

from sentence_transformers import SentenceTransformer

# ✅ Load model once (global - avoids reloading every time)
model = SentenceTransformer("all-MiniLM-L12-v2")


def embed_chunks(chunks):
    """
    chunks: [{ "id": str, "text": str, "metadata": {...} }]
    returns: [{ "id": str, "text": str, "vector": vector, "metadata": {...} }]
    """

    texts = [chunk["text"] for chunk in chunks]

    # 🔥 Convert text → vectors
    vectors = model.encode(texts, show_progress_bar=False)

    embedded_data = []

    for i, chunk in enumerate(chunks):
        embedded_data.append({
            "id": chunk["id"],
            "text": chunk["text"], 
            "vector": vectors[i].tolist(),
            "metadata": chunk["metadata"]
        })

    return embedded_data