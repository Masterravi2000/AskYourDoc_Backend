from fastapi import APIRouter
from app.features.search.search import search_query
from app.schemas.SearchResponse import SearchResponse
from app.schemas.SearchRequest import SearchRequest

router = APIRouter()

@router.post("/search")
def search_api(request: SearchRequest):
    results = search_query(request.query)
    return SearchResponse(results=results)