from pydantic import BaseModel

class downloadRequest(BaseModel) :
    file_name: str
    file_type: str