from fastapi import UploadFile
from app.repositories.status_store_repository import set_status
from app.features.workers.worker_pool import task_queue
import os
from uuid import uuid4


# Ensure folder exists
os.makedirs("docs/pdf", exist_ok=True)

async def upload_pdfs(files: list[UploadFile], last_modified: list[int]):
    uploaded_files = []
    failed_files = []

    for index, file in enumerate(files):
        fileId = str(uuid4())
        file_path = f"docs/pdf/{file.filename}"

        try:
            # File type check
            if not file.filename.lower().endswith(".pdf"):
                raise Exception("Under PDF section only PDF files are allowed")

            # Duplicate check
            if os.path.exists(file_path):
                raise FileExistsError("Given PDF file already exists")

            with open(file_path, "wb") as f:
                f.write(await file.read())

            uploaded_files.append({
                "fileId": fileId,
                "filename": file.filename,
            })
            
            # set done status
            set_status(fileId, file.filename, "queued")
                        
            # push both id and file path into task_queue
            task_queue.put({
                "fileId": fileId,
                "filePath": file_path,
                "last_modified": last_modified[index]
            })
            
        except FileExistsError as e:
            failed_files.append({
                "filename": file.filename,
                "error": str(e)
            })

            set_status(fileId, file.filename, "failed", str(e))
            print(f"{file.filename} → failed ❌ ({e})")

        except Exception as e:
            if os.path.exists(file_path):
                 os.remove(file_path)
                 
            failed_files.append({
                "filename": file.filename,
                "error": str(e)
            })
            
            # set failed status
            set_status(fileId, file.filename, "failed", str(e))
            # print done status
            print(f"{file.filename} → failed ❌ ({e})")

    return {
        "uploaded_files": uploaded_files,
        "failed_files": failed_files,
    }