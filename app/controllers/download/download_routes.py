from fastapi import APIRouter
from app.services.download.download_service import download_file

router = APIRouter()

@router.get("/download")
async def download(file_name: str, file_type: str) :
    print(file_name, file_type)
    return download_file(file_name, file_type)