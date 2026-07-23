import time
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.repositories.status_store_repository import set_status
from app.repositories.lancedb_repository import insert_embeddings

# Import processors for step 2
from app.features.fileProcessors.pdfProcessor import extract_pdf
from app.features.fileProcessors.imageProcessor import extract_image
from app.features.fileProcessors.pptxProcessor import extract_pptx
from app.features.fileProcessors.txtProcessor import extract_txt
from app.features.fileProcessors.xlsProcessor import extract_xls

# import chunker for step 3
from app.features.chunking.chunker import chunk_documents

# import sentence transformer model for step 4
from app.features.embedding.embedder import embed_chunks

# import vector db for step 5
from app.repositories.faiss_store_repository import ( store_embeddings, save_metadata, batchFills_save_to_disk )

WATCHER_READY = False

def is_file_stable(file_path, wait_time=1.5, retries=3):
    """Check if file size is stable"""
    last_size = -1

    for _ in range(retries):
        try:
            current_size = os.path.getsize(file_path)
        except FileNotFoundError:
            return False

        if current_size == last_size:
            return True

        last_size = current_size
        time.sleep(wait_time)

    return False


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        print(f"New file detected: {file_path}")

        # 🔥 Run each file in separate thread (independent processing)
        threading.Thread(target=self.handle_file, args=(file_path,)).start()

    def handle_file(self, file_path):
        # ✅ Wait until file is fully written
        if not is_file_stable(file_path):
            print(f"File not stable, skipping: {file_path}")
            return

        try:
            process_file(file_path)
        except Exception as e:
            print(f"Processing error: {e}")


def process_file(file_path: str):
    filename = os.path.basename(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        print(f"{filename} → processing started")

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
        print(f"processed data {documents}")
        
        # step 3 - chunking starts
        set_status(filename, "chunking")
        chunks = chunk_documents(documents)
        print(f"{filename} → chunking completed ✅")
        print(f"Total chunks created: {len(chunks)}")
        
        # step 4 - embedding starts
        set_status(filename, "embedding")
        embedded_data = embed_chunks(chunks)
        print(f"{filename} → embedding completed ✅")
        print(f"Total embeddings created: {len(embedded_data)}")
        if embedded_data:
            print("🔍 FINAL OUTPUT SAMPLE:")
            print(embedded_data[0])
        
        # step 5 - store in vector db
        store_embeddings(embedded_data)
        save_metadata(embedded_data)
        batchFills_save_to_disk() # persist it into memory 
        print(f"{filename} → stored in FAISS ✅")
        # step 5 - store in vector db
        insert_embeddings(embedded_data)
        print(f"{filename} → stored in LanceDB ✅")
        
        set_status(filename, "success")

    except Exception as e:
        set_status(filename, "failed", str(e))
        print(f"{filename} → failed ❌ ({e})")


def start_watching():
    global WATCHER_READY
    
    # clear_vector_db()
    
    path = "docs"
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    WATCHER_READY = True
    print("👀 Watching for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_watching()