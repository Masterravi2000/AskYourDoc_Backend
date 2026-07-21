import fitz  # PyMuPDF
import os
from app.repositories.status_store_repository import set_status
from app.utils.text_cleaner import clean_and_normalize

def extract_pdf(file_path: str) -> str:
    documents = []
    filename = os.path.basename(file_path)

    try:
        set_status(filename, "processing")

        with fitz.open(file_path) as doc:
            for page_num, page in enumerate(doc):
                # 🔹 REFACTORED: separated raw extraction
                raw_text = page.get_text("text")
                
                # 🔹 REFACTORED: applied cleaning + normalization
                page_text = clean_and_normalize(raw_text)
                
                if page_text:
                    documents.append({
                        "text": page_text,
                        "metadata": {
                            "file_name": filename,
                            "file_type": "pdf",
                            "page": page_num + 1
                        }
                    })
        
        set_status(filename, "processed")

    except Exception as e:
        set_status(filename, "failed", str(e))
        print(f"{filename} → failed ❌ ({e})") 
        
        if os.path.exists(file_path):
             os.remove(file_path)
             
        raise Exception(f"PDF processing failed: {str(e)}")

    return documents