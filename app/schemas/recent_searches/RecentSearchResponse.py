from pydantic import BaseModel

class RecentSearchResponse(BaseModel):
    id: int
    query: str
    searched_at: str