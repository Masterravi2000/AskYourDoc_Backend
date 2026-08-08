from pydantic import BaseModel

class RecentSearchRequest (BaseModel):
    query : str