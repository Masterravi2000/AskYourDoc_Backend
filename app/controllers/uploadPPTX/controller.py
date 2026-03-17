from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

os.makedirs("docs/pptx", exist_ok=True)

@router.post("/upload/pptx")
async def upload_pptx(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pptx"):
        return {"error": "Only PPTX files allowed"}

    file_path = f"docs/pptx/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "type": "PPTX", "status": "uploaded"}