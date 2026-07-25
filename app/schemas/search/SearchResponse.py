from pydantic import BaseModel

class SearchResult(BaseModel) :
    content: str
    score: float
    file_name: str
    file_type: str
    page_number: int | None
    slide_number: int | None
    line_start: int | None
    line_end: int | None
    
class SearchResponse(BaseModel):
    results: list[SearchResult]