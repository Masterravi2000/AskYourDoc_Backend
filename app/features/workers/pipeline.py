from app.repositories.status_store_repository import set_status

# Import processors
from app.features.fileProcessors.pdfProcessor import extract_pdf
from app.features.fileProcessors.imageProcessor import extract_image
from app.features.fileProcessors.pptxProcessor import extract_pptx
from app.features.fileProcessors.txtProcessor import extract_txt
from app.features.fileProcessors.xlsProcessor import extract_xls

# Import chunker
from app.features.chunking.chunker import chunk_documents

# Import embedder
from app.features.embedding.embedder import embed_chunks

# Import LanceDB repository
from app.repositories.lancedb_repository import insert_embeddings

import os


# ==========================================================
# PROCESS FILE PIPELINE
# Handles the complete processing flow of a single file:
#
# Processing
#      ↓
# Chunking
#      ↓
# Embedding
#      ↓
# LanceDB Storage
# ==========================================================
def process_file(file_path: str):

    filename = os.path.basename(file_path)
    ext = os.path.splitext(file_path)[1].lower()

    try:

        print(f"{filename} → processing started")

        # --------------------------------------------------
        # STEP 1 : Extract file contents
        # --------------------------------------------------

        if ext == ".pdf":
            documents = extract_pdf(file_path)

        elif ext in [".png", ".jpg", ".jpeg"]:
            documents = extract_image(file_path)

        elif ext == ".pptx":
            documents = extract_pptx(file_path)

        elif ext == ".txt":
            documents = extract_txt(file_path)

        elif ext in [".xls", ".xlsx"]:
            documents = extract_xls(file_path)

        else:
            print(f"Unsupported file type: {file_path}")
            set_status(filename, "failed", "Unsupported file type")
            return

        print(f"{filename} → processing completed ✅")


        # --------------------------------------------------
        # STEP 2 : Chunking
        # --------------------------------------------------

        set_status(filename, "chunking")

        chunks = chunk_documents(documents)

        print(f"{filename} → chunking completed ✅")


        # --------------------------------------------------
        # STEP 3 : Embedding
        # --------------------------------------------------

        set_status(filename, "embedding")

        embedded_data = embed_chunks(chunks)

        print(f"{filename} → embedding completed ✅")


        # --------------------------------------------------
        # STEP 4 : Store in LanceDB
        # --------------------------------------------------

        insert_embeddings(embedded_data)

        print(f"{filename} → stored in LanceDB ✅")


        # --------------------------------------------------
        # STEP 5 : Mark Completed
        # --------------------------------------------------

        set_status(filename, "completed")

    except Exception as e:

        set_status(filename, "failed", str(e))

        print(f"{filename} → failed ❌ ({e})")