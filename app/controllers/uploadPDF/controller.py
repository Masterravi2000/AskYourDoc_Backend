from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

os.makedirs("docs/pdf", exist_ok=True)

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files allowed"}

    file_path = f"docs/pdf/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "type": "PDF", "status": "uploaded"}