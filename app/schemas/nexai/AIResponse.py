from pydantic import BaseModel

class AISource (BaseModel) :
    file_name: str
    file_type: str
    file_size: str
    page_number: int | None
    slide_number: int | None
    last_modified: str
    
class AIResponse(BaseModel) :
    answer: str
    sources: list[AISource]