from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadPDF.upload_pdf_service import upload_pdfs
from app.schemas.upload.UploadResponse import UploadResponse

router = APIRouter()

@router.post("/upload/pdf", response_model=UploadResponse)
async def upload_pdf_route(files: list[UploadFile] = File(...)) -> UploadResponse :
    return await upload_pdfs(files)