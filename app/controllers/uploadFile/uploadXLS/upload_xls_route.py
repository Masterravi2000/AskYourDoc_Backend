from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadXLS.upload_xls_service import upload_xls
from app.schemas.upload.UploadResponse import UploadResponse
from fastapi import Form

router = APIRouter()

@router.post("/upload/xls", response_model=UploadResponse)
async def upload_xls_route(
    files: list[UploadFile] = File(...),
    last_modified: list[int] = Form(...)
    ) -> UploadResponse :
    return await upload_xls(files, last_modified)