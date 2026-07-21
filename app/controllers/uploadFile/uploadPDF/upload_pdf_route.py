from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadPDF.upload_pdf_service import upload_pdfs

router = APIRouter()

@router.post("/upload/pdf")
async def upload_pdf_route(files: list[UploadFile] = File(...)) :
    return await upload_pdfs(files)