from fastapi import APIRouter
from app.features.search.search import search_query
from app.schemas.SearchResponse import SearchResponse

router = APIRouter()

@router.get("/search")
def search_api(query: str):
    results = search_query(query)
    return SearchResponse(results=results)