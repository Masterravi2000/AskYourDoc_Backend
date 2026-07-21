from fastapi import UploadFile
import os
from app.repositories.status_store_repository import set_status


os.makedirs("docs/txt", exist_ok=True)

async def upload_txt(files: list[UploadFile]):
    uploaded_files = []
    failed_files = []

    for file in files:
        file_path = f"docs/txt/{file.filename}"

        try:
            # file type check
            if not file.filename.lower().endswith(".txt"):
                raise Exception("Invalid file type")

            # Duplicate check
            if os.path.exists(file_path):
                raise Exception("File already exists")

            with open(file_path, "wb") as f:
                f.write(await file.read())

            uploaded_files.append(file.filename)
            
            set_status(file.filename, "uploaded")
            
        except Exception as e:
            if os.path.exists(file_path):
                 os.remove(file_path)
                 
            failed_files.append({
                "filename": file.filename,
                "error": str(e)
            })
            
            set_status(file.filename, "failed", str(e))
            print(f"{file.filename} → failed ❌ ({e})")

    return {
        "uploaded_files": uploaded_files,
        "failed_files": failed_files,
        "status": "completed"
    }