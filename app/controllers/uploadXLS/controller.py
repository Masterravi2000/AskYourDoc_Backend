from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

os.makedirs("docs/xls", exist_ok=True)

@router.post("/upload/xls")
async def upload_xls(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".xls", ".xlsx")):
        return {"error": "Only Excel files allowed"}

    file_path = f"docs/xls/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "type": "XLS", "status": "uploaded"}