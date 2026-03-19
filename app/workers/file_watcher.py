import time
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.status_store import set_status

# Import processors
from app.fileProcessors.pdfProcessor import extract_pdf
from app.fileProcessors.imageProcessor import extract_image
from app.fileProcessors.pptxProcessor import extract_pptx
from app.fileProcessors.txtProcessor import extract_txt
from app.fileProcessors.xlsProcessor import extract_xls


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
            text = extract_pdf(file_path)

        elif ext in [".png", ".jpg", ".jpeg"]:
            text = extract_image(file_path)

        elif ext == ".pptx":
            text = extract_pptx(file_path)

        elif ext == ".txt":
            text = extract_txt(file_path)

        elif ext in [".xls", ".xlsx"]:
            text = extract_xls(file_path)

        else:
            print(f"Unsupported file type: {file_path}")
            set_status(filename, "failed", "Unsupported file type")
            return

        print(f"{filename} → processing completed ✅")
        print(f"\nProcessed Text (Preview):\n{text[:500]}\n")

    except Exception as e:
        set_status(filename, "failed", str(e))
        print(f"{filename} → failed ❌ ({e})")


def start_watching():
    path = "docs"
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    print("👀 Watching for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_watching()