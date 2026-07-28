from pydantic import BaseModel

class UploadFile(BaseModel) :
    fileId: str
    filename: str
    
class FailedFile(BaseModel):
    filename: str
    error: str
    
class UploadResponse(BaseModel):
    uploaded_files: list[UploadFile]
    failed_files: list[FailedFile]