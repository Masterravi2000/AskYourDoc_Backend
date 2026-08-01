from pydantic import BaseModel

class StatusResponse(BaseModel):
    filename: str
    status : str
    error : str | None