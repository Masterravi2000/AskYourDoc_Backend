import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.repositories.lancedb_repository import inspect_vector_db, clear_lancedb

WATCHER_READY = False


# ==========================================================
# CHECK WHETHER FILE IS FULLY WRITTEN
# Prevents reading half-written files.
# ==========================================================
def is_file_stable(file_path, wait_time=1.5, retries=3):

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


# ==========================================================
# WATCHDOG EVENT HANDLER
# Triggered whenever a new file appears.
# ==========================================================
class FileHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = event.src_path
        filename = os.path.basename(file_path)

        print(f"New file detected : {file_path}")

        # Wait until upload is complete
        if not is_file_stable(file_path):
            print(f"File not stable, skipping : {file_path}")
            return

        # # Mark file as queued
        # set_status(filename, "queued")

        # # Push into queue
        # task_queue.put(file_path)

        # print(f"{filename} added to processing queue")


# ==========================================================
# START WATCHDOG
# Starts monitoring the docs folder.
# ==========================================================
def start_watching():

    global WATCHER_READY
    
    # clear_lancedb()
    inspect_vector_db()

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