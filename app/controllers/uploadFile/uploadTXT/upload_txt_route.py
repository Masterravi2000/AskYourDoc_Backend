from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadTXT.upload_txt_service import upload_txt
from app.schemas.upload.UploadResponse import UploadResponse
from fastapi import Form

router = APIRouter()

@router.post("/upload/txt", response_model=UploadResponse)
async def upload_txt_route(
    files: list[UploadFile] = File(...),
    last_modified: list[int] = Form(...)
    ) -> UploadResponse :
    return await upload_txt(files, last_modified)