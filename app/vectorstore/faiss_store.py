import faiss
import numpy as np
import pickle
import os
import threading

# 🔒 NEW: lock to avoid race conditions (parallel threads)
lock = threading.Lock()

# ✅ dimension for MiniLM-L12-v2
dimension = 384

# ✅ FAISS index
index = faiss.IndexFlatL2(dimension)

# ✅ metadata storage
metadata_store = []

FAISS_PATH = "faiss_index.bin"
META_PATH = "metadata.pkl"

# 📦 NEW: batch control variables
BATCH_SIZE = 10
current_batch_count = 0

def store_embeddings(embedded_data):
    global current_batch_count
    vectors = [item["embedding"] for item in embedded_data]
    vectors = np.array(vectors).astype("float32")
    
    with lock:
        index.add(vectors)  # add vectors
        current_batch_count +=1 # count files for batching

def save_metadata(embedded_data):
    with lock:
        for item in embedded_data:
            metadata_store.append(item["metadata"])
        
# save to disk (synced)
def save_to_disk():
    faiss.write_index(index, FAISS_PATH) # save vectors
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata_store, f) # save metadata
    print("FAISS + metadata saved")

# batch trigger function
def batchFills_save_to_disk():
    global current_batch_count
    
    with lock:
        if current_batch_count >= BATCH_SIZE:
            save_to_disk()
            current_batch_count = 0
            print(f"💾 Batch saved! Total vectors: {index.ntotal}")
    
# load from disk (synced)
def load_from_disk():
    global index, metadata_store
    
    if os.path.exists(FAISS_PATH) and os.path.exists(META_PATH):
        index = faiss.read_index(FAISS_PATH)
        with open(META_PATH, "rb") as f:
            metadata_store = pickle.load(f)
            
        print(f"FAISS loaded Total vectors: {index.ntotal}")
    else:
        print("No existing FAISS index found, starting fresh")