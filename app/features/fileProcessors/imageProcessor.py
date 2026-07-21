from PIL import Image
import pytesseract
import os
import sys
from app.repositories import set_status 

def get_tesseract_path():
    if getattr(sys, 'frozen', False):  
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()

    return os.path.join(base_path, "tesseract", "tesseract.exe")

# pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_image(file_path: str) -> str:
    filename = os.path.basename(file_path)
    documents = []
    
    try:
        # set current status
        set_status(filename, "processing")
        
        with Image.open(file_path) as img:
            text = pytesseract.image_to_string(img).strip()
            
            if text:
                documents.append({ 
                    "text": text,
                    "metadata": {
                        "file_name": filename,
                        "file_type": "image",
                        "page": 1
                    }
                })
            
            # set done status
            set_status(filename, "processed")
            
        return documents
    
    except Exception as e:
        # set failed status
        set_status(filename, "failed", str(e))
        # print failed status
        print(f"{filename} → failed ❌ ({e})")
        
        # remove the file if failed
        if os.path.exists(file_path):
             os.remove(file_path)
             
        raise Exception(f"Image processing failed: {str(e)}")