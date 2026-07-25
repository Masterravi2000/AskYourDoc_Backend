from fastapi import APIRouter
from app.services.status.status_service import fetch_status

router = APIRouter()

@router.get("/status/{filename}")
def get_status_route(filename: str):
    return fetch_status(filename)