from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadTXT.upload_txt_service import upload_txt
from app.schemas.upload.UploadResponse import UploadResponse

router = APIRouter()

@router.post("/upload/txt", response_model=UploadResponse)
async def upload_txt_route(files: list[UploadFile] = File(...)) -> UploadResponse :
    return await upload_txt(files)