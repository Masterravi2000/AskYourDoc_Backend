from fastapi import APIRouter
from app.features.search.search import search_query
from app.schemas.search.SearchResponse import SearchResponse
from app.schemas.search.SearchRequest import SearchRequest
from app.schemas.nexai.AIResponse import AIResponse

router = APIRouter()

@router.post("/search")
def search_api(request: SearchRequest):
    results = search_query(request.query, request.mode)
    
    if request.mode == "offline":
        return SearchResponse(results=results)
    
    elif request.mode == "ai":
        return AIResponse(**results)
    
    else :
        raise ValueError("Invalid search mode")