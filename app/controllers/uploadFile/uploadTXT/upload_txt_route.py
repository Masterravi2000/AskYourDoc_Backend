from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadTXT.upload_txt_service import upload_txt

router = APIRouter()

router.post("/upload/txt")
async def upload_txt_route(files: list[UploadFile] = File(...)) :
    return await upload_txt(files)