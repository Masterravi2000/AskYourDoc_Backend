from app.repositories.status_store_repository import get_status
from app.schemas.status.StatusResponse import StatusResponse

def fetch_status(filename: str) -> StatusResponse:
    status=get_status(filename)
    
    return StatusResponse(
        status=status["status"],
        error=status["error"]
    )