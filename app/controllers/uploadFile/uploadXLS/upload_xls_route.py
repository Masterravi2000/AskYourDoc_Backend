from fastapi import APIRouter, UploadFile, File
from app.services.uploadFiles.uploadXLS.upload_xls_service import upload_xls

router = APIRouter()

@router.post("/upload/xls")
async def upload_xls_route(files: list[UploadFile] = File(...)) :
    return await upload_xls(files)