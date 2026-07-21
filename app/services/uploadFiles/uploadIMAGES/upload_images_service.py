from fastapi import UploadFile
import os
from app.repositories.status_store_repository import set_status

os.makedirs("docs/images", exist_ok=True)

async def upload_images(files: list[UploadFile]):
    uploaded_files = []
    failed_files = []

    for file in files:
        file_path = f"docs/images/{file.filename}"

        try:
            # File type check
            if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                raise Exception("Given image has invalid file type")
            
            # Duplicate check (before writing)
            if os.path.exists(file_path):
                raise Exception("Given image already exists")

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