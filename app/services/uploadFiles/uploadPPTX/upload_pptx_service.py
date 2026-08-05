from fastapi import UploadFile
import os
from app.repositories.status_store_repository import set_status
from app.features.workers.worker_pool import task_queue
from uuid import uuid4

os.makedirs("docs/pptx", exist_ok=True)


async def upload_pptx(files: list[UploadFile], last_modified: list[int]):
    uploaded_files = []
    failed_files = []

    for index, file in enumerate(files):
        fileId = str(uuid4())
        file_path = f"docs/pptx/{file.filename}"

        try:
            # file type check
            if not file.filename.lower().endswith(".pptx"):
                raise Exception("Invalid file type")

            # Duplicate check
            if os.path.exists(file_path):
                raise FileExistsError("Given pptx already exists")

            with open(file_path, "wb") as f:
                f.write(await file.read())

            uploaded_files.append({"fileId": fileId, "filename": file.filename})

            # set status to queued
            set_status(fileId, file.filename, "queued")

            # push both id and file path into task_queue
            task_queue.put({
                "fileId": fileId, 
                "filePath": file_path,
                "last_modified": last_modified[index]
                })
            
        except FileExistsError as e:
            failed_files.append({"filename": file.filename, "error": str(e)})

            set_status(fileId, file.filename, "failed", str(e))
            print(f"{file.filename} → failed ❌ ({e})")
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            failed_files.append({"filename": file.filename, "error": str(e)})

            set_status(fileId, file.filename, "failed", str(e))
            print(f"{file.filename} → failed ❌ ({e})")

    return {
        "uploaded_files": uploaded_files,
        "failed_files": failed_files,
    }
