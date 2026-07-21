from pptx import Presentation
import os
from app.repositories import set_status 

def extract_pptx(file_path: str) -> str:
    documents = []
    filename = os.path.basename(file_path)

    try:
        set_status(filename, "processing")
        
        prs = Presentation(file_path)

        for slide_num, slide in enumerate(prs.slides):
            slide_text = []

            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    content = shape.text.strip()
                    if content:
                        slide_text.append(content)

            if slide_text:
                documents.append({
                    "text": "\n".join(slide_text),
                    "metadata": {
                        "file_name": filename,
                        "file_type": "pptx",
                        "page": slide_num + 1
                    }
                })
                
        set_status(filename, "processed")
        
    except Exception as e:
        set_status(filename, "failed", str(e))
        print(f"{filename} → failed ❌ ({e})")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        raise Exception(f"PPTX processing failed: {str(e)}")

    return documents