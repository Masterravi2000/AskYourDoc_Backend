from fastapi import APIRouter
from app.services.status.status_service import fetch_status

router = APIRouter()

@router.get("/status/{fileId}")
def get_status_route(fileId: str):
    return fetch_status(fileId)