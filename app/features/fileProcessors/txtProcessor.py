import os
from app.repositories.status_store_repository import set_status

def extract_txt(file_path: str) -> str:
    filename = os.path.basename(file_path)
    documents = []

    try:
        set_status(filename, "processing")
        
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            
            if text:
                documents.append({
                    "text": text,
                    "metadata": {
                        "file_name": filename,
                        "file_type": "txt",
                        "page": 1
                    }
                })
            
        set_status(filename, "processed")

        return documents
    
    except Exception as e:
        set_status(filename, "failed", str(e))
        print(f"{filename} → failed ❌ ({e})")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        raise Exception(f"TXT processing failed: {str(e)}")