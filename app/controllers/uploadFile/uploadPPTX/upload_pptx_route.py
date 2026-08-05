from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadPPTX.upload_pptx_service import upload_pptx
from app.schemas.upload.UploadResponse import UploadResponse
from fastapi import Form

router = APIRouter()

@router.post("/upload/pptx", response_model=UploadResponse)
async def upload_pptx_route(
    files: list[UploadFile] = File(...),
    last_modified: list[int] = Form(...)
    ) -> UploadResponse :
    return await upload_pptx(files, last_modified)