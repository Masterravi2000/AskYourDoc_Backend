# app/chunking/chunker.py

from typing import List, Dict

def chunk_documents(
    documents: List[Dict],
    chunk_size: int = 500,
    overlap: int = 100
) -> List[Dict]:
    """
    الوثuments: [{ "text": str, "metadata": {...} }]
    returns: [{ "text": chunk, "metadata": {..., chunk_id, chunk_index} }]
    """

    chunks = []
    chunk_id = 0

    for doc in documents:
        text = doc.get("text", "").strip()
        metadata = doc.get("metadata", {})

        if not text:
            continue  # skip empty

        start = 0
        text_length = len(text)
        chunk_index = 0

        while start < text_length:
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():  # avoid empty/noise chunks
                chunk_metadata = {
                    **metadata,
                    "chunk_id": chunk_id,
                    "chunk_index": chunk_index
                }

                chunks.append({
                    "text": chunk_text,
                    "metadata": chunk_metadata
                })

                chunk_id += 1
                chunk_index += 1

            start += chunk_size - overlap  # move with overlap

    return chunks