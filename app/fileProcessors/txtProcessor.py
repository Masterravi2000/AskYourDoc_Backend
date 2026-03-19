import os
from app.status_store import set_status

def extract_txt(file_path: str) -> str:
    filename = os.path.basename(file_path)

    try:
        set_status(filename, "processing")
        
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            
        set_status(filename, "processed")

        return text
    
    except Exception as e:
        set_status(filename, "failed", str(e))
        print(f"{filename} → failed ❌ ({e})")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        raise Exception(f"TXT processing failed: {str(e)}")