from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadIMAGES.upload_images_service import upload_images

router = APIRouter()

@router.post("/upload/images")
async def upload_images_route(files: list[UploadFile] = File(...)) :
    print("✅ Route reached")
    return await upload_images(files)