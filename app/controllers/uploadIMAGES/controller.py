from fastapi import APIRouter, UploadFile, File
import os
from app.status_store import set_status

router = APIRouter()

os.makedirs("docs/images", exist_ok=True)

@router.post("/upload/images")
async def upload_images(files: list[UploadFile] = File(...)):
    uploaded_files = []
    failed_files = []

    for file in files:
        file_path = f"docs/images/{file.filename}"

        try:
            # File type check
            if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                raise Exception("Invalid file type")
            
            # Duplicate check (before writing)
            if os.path.exists(file_path):
                raise Exception("File already exists")

            with open(file_path, "wb") as f:
                f.write(await file.read())

            uploaded_files.append(file.filename)
            
            # set done status
            set_status(file.filename, "uploaded")

        except Exception as e:
            if os.path.exists(file_path):
                 os.remove(file_path)
                 
            failed_files.append({
                "filename": file.filename,
                "error": str(e)
            })
            
            # set failed status
            set_status(file.filename, "failed", str(e))
            # print failed status
            print(f"{file.filename} → failed ❌ ({e})")

    return {
        "uploaded_files": uploaded_files,
        "failed_files": failed_files,
        "status": "completed"
    }