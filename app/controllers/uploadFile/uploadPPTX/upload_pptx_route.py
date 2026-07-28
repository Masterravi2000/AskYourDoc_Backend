from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadPPTX.upload_pptx_service import upload_pptx
from app.schemas.upload.UploadResponse import UploadResponse

router = APIRouter()

@router.post("/upload/pptx", response_model=UploadResponse)
async def upload_pptx_route(files: list[UploadFile] = File(...)) -> UploadResponse :
    return await upload_pptx(files)