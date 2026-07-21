from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadPPTX.upload_pptx_service import upload_pptx

router = APIRouter()

@router.post("/upload/pptx")
async def upload_pptx_route(files: list[UploadFile] = File(...)) :
    return await upload_pptx(files)