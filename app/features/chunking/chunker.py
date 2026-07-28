# app/chunking/chunker.py

from typing import List, Dict
from app.repositories.status_store_repository import set_status
import re


def chunk_documents(
    fileId: str,
    documents: List[Dict],
    chunk_size: int = 500,
    overlap: int = 100
) -> List[Dict]:

    # start = time.perf_counter()
    
    #set status
    filename = documents[0]["metadata"]["file_name"]
    set_status(fileId, filename, "chunking")

    chunks = []
    chunk_id = 0

    for doc in documents:
        text = doc.get("text", "").strip()
        metadata = doc.get("metadata", {})

        if not text:
            continue

        # ✅ SENTENCE SPLITTING (clean input assumed)
        sentences = re.split(r'(?<=[.!?])\s+', text)

        current_chunk = ""

        for sentence in sentences:

            # If sentence itself is too large → hard split
            if len(sentence) > chunk_size:
                words = sentence.split()
                temp = ""

                for word in words:
                    if len(temp) + len(word) + 1 <= chunk_size:
                        temp += " " + word
                    else:
                        if temp.strip():
                            chunks.append(_create_chunk(temp, metadata, chunk_id))
                            chunk_id += 1
                        temp = word

                if temp.strip():
                    chunks.append(_create_chunk(temp, metadata, chunk_id))
                    chunk_id += 1

                continue

            # Normal chunk building
            if len(current_chunk) + len(sentence) + 1 <= chunk_size:
                current_chunk += " " + sentence
            else:
                if current_chunk.strip():
                    chunks.append(_create_chunk(current_chunk, metadata, chunk_id))
                    chunk_id += 1

                # ✅ WORD-BASED OVERLAP
                words = current_chunk.split()
                overlap_words = words[-(overlap // 5):] if words else []

                current_chunk = " ".join(overlap_words) + " " + sentence

        # ✅ FINAL CHUNK
        if current_chunk.strip():
            chunks.append(_create_chunk(current_chunk, metadata, chunk_id))
            chunk_id += 1
    
    # print(f"Total chunks created: {len(chunks)}")
    # print(f"[Chunking] Completed in {time.perf_counter() - start:.3f} sec")

    return chunks


# 🔹 Helper function (clean + reusable)
def _create_chunk(text: str, metadata: Dict, chunk_id: int) -> Dict:
    file_type = metadata.get("file_type")

    chunk_metadata = {
        "file_name": metadata.get("file_name"),
        "file_type": file_type,
        "page_number": metadata.get("page") if file_type == "pdf" else None,
        "slide_number": metadata.get("page") if file_type == "pptx" else None,
        "sheet_name": metadata.get("page") if file_type == "xls" else None,
        "line_start": None,
        "line_end": None
    }

    # print(f"\n🔹 Chunk ID: {chunk_id}")
    # print(f"Text Preview: {text[:150]}...")
    # print(f"Metadata: {chunk_metadata}")
    # print("-" * 50)

    return {
        "id": f"chunk_{chunk_id}",
        "text": text.strip(),
        "metadata": chunk_metadata
    }
    