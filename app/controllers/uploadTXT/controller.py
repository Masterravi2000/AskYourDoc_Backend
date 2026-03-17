from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

os.makedirs("docs/txt", exist_ok=True)

@router.post("/upload/txt")
async def upload_txt(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".txt"):
        return {"error": "Only TXT files allowed"}

    file_path = f"docs/txt/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "type": "TXT", "status": "uploaded"}