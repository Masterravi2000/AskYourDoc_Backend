from fastapi import UploadFile
import os
from uuid import uuid4
from app.repositories.status_store_repository import set_status
from app.features.workers.worker_pool import task_queue

os.makedirs("docs/images", exist_ok=True)


async def upload_images(files: list[UploadFile], last_modified: list[int]):

    uploaded_files = []
    failed_files = []

    for index, file in enumerate(files):
        fileId = str(uuid4())
        file_path = f"docs/images/{file.filename}"

        try:
            # File type check
            if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                raise Exception("Given image has invalid file type")

            # Duplicate check (before writing)
            if os.path.exists(file_path):
                raise FileExistsError("Given image already exists")

            with open(file_path, "wb") as f:
                f.write(await file.read())

            uploaded_files.append(
                {
                    "fileId": fileId,
                    "filename": file.filename,
                }
            )

            # set done status
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

            # set failed status
            set_status(fileId, file.filename, "failed", str(e))
            # print failed status
            print(f"{file.filename} → failed ❌ ({e})")

    return {
        "uploaded_files": uploaded_files,
        "failed_files": failed_files,
    }
