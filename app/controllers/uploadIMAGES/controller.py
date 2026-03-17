from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

os.makedirs("docs/images", exist_ok=True)

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return {"error": "Only PNG/JPG/JPEG allowed"}

    file_path = f"docs/images/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "type": "IMAGE", "status": "uploaded"}