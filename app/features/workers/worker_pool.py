from queue import Queue
import threading
import os

# Import complete processing pipeline
from app.features.workers.pipeline import process_file

# ==========================================================
# GLOBAL TASK QUEUE
# Stores all files waiting to be processed.
# File Watcher puts tasks into this queue.
# Workers consume tasks from this queue.
# ==========================================================

task_queue: Queue[dict] = Queue()   # optional type hint (Python 3.9+)

# ==========================================================
# WORKER
# Each worker continuously waits for a file.
#
# Queue
#   ↓
# Get File
#   ↓
# Process File
#   ↓
# Mark Task Completed
# ==========================================================

def worker():
     
     while True:
         
         # Wait untill a task is available 
         task = task_queue.get()
         
         fileId = task["fileId"]
         filePath = task["filePath"]
         
         try:
             
             print(f"[Worker] Processing : {filePath}")
             
             process_file(fileId, filePath)
        
         except Exception as e:
             
             print(f"[Worker Error] {e}")
             
         finally:
             
             # Tell queue this task is completed
             task_queue.task_done()
             
             
# ==========================================================
# START WORKER POOL
# Creates multiple worker threads.
#
# Example (4 Workers)
# based on device resources cpu count
#
# Worker-1
# Worker-2
# Worker-3
# Worker-4 etc...
#
# All remain alive and wait for files.
# ==========================================================


def start_worker_pool() :
    
    NUM_WORKERS = os.cpu_count() or 4
    
    print(f"Starting {NUM_WORKERS} worker(s)...")
    
    for i in range(NUM_WORKERS):
        
        thread = threading.Thread(
            target=worker,
            daemon=True,
            name=f"Worker-{i+1}"
        )
        
        thread.start()
        
        print(f"{thread.name} started.")