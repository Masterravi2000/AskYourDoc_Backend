import faiss
import numpy as np
import pickle
import os

# ✅ dimension for MiniLM-L12-v2
dimension = 384

# ✅ FAISS index
index = faiss.IndexFlatL2(dimension)

# ✅ metadata storage
metadata_store = []

FAISS_PATH = "faiss_index.bin"
META_PATH = "metadata.pkl"

def store_embeddings(embedded_data):
    vectors = [item["embedding"] for item in embedded_data]
    vectors = np.array(vectors).astype("float32")

    index.add(vectors)  # add vectors

def save_metadata(embedded_data):
    for item in embedded_data:
        metadata_store.append(item["metadata"])
        
# save to disk (synced)
def save_to_disk():
    faiss.write_index(index, FAISS_PATH) # save vectors
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata_store, f) # save metadata
    print("FAISS + metadata saved")
    
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