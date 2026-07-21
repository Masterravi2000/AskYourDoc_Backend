from fastapi import UploadFile
from app.repositories.status_store_repository import set_status
import os


# Ensure folder exists
os.makedirs("docs/pdf", exist_ok=True)

async def upload_pdfs(files: list[UploadFile]):
    uploaded_files = []
    failed_files = []

    for file in files:
        file_path = f"docs/pdf/{file.filename}"

        try:
            # File type check
            if not file.filename.lower().endswith(".pdf"):
                raise Exception("Under PDF section only PDF files are allowed")

            # Duplicate check
            if os.path.exists(file_path):
                raise Exception("Given PDF file already exists")

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
            # print done status
            print(f"{file.filename} → failed ❌ ({e})")

    return {
        "uploaded_files": uploaded_files,
        "failed_files": failed_files,
        "status": "completed"
    }