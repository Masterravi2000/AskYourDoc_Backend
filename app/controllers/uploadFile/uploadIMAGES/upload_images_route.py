from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadIMAGES.upload_images_service import upload_images
from app.schemas.upload.UploadResponse import UploadResponse
from fastapi import Form

router = APIRouter()

@router.post("/upload/images", response_model=UploadResponse)
async def upload_images_route(
    files: list[UploadFile] = File(...),
    last_modified: list[int] = Form(...)
    ) -> UploadResponse :
    return await upload_images(files, last_modified)