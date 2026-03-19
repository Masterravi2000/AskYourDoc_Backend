import fitz  # PyMuPDF
import os
from app.status_store import set_status

def extract_pdf(file_path: str) -> str:
    text_parts = []
    filename = os.path.basename(file_path)

    try:
        set_status(filename, "processing")

        with fitz.open(file_path) as doc:
            for page_num, page in enumerate(doc):
                page_text = page.get_text().strip()
                if page_text:
                    text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
        
        set_status(filename, "processed")

    except Exception as e:
        set_status(filename, "failed", str(e))
        print(f"{filename} → failed ❌ ({e})") 
        
        if os.path.exists(file_path):
             os.remove(file_path)
             
        raise Exception(f"PDF processing failed: {str(e)}")

    return "\n\n".join(text_parts)