from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()

os.makedirs("docs/pptx", exist_ok=True)

@router.post("/upload/pptx")
async def upload_pptx(files: list[UploadFile] = File(...)):
    uploaded_files = []
    failed_files = []

    for file in files:
        file_path = f"docs/pptx/{file.filename}"

        try:
            # file type check
            if not file.filename.lower().endswith(".pptx"):
                raise Exception("Invalid file type")

            # Duplicate check
            if os.path.exists(file_path):
                raise Exception("File already exists")

            with open(file_path, "wb") as f:
                f.write(await file.read())

            uploaded_files.append(file.filename)

        except Exception as e:
            failed_files.append({
                "filename": file.filename,
                "error": str(e)
            })

    return {
        "uploaded_files": uploaded_files,
        "failed_files": failed_files,
        "status": "completed"
    }