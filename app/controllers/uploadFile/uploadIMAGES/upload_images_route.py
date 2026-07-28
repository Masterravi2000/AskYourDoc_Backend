from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadIMAGES.upload_images_service import upload_images
from app.schemas.upload.UploadResponse import UploadResponse

router = APIRouter()

@router.post("/upload/images", response_model=UploadResponse)
async def upload_images_route(files: list[UploadFile] = File(...)) -> UploadResponse :
    return await upload_images(files)