from fastapi import APIRouter
from app.schemas.recent_searches.RecentSearchRequest import RecentSearchRequest
from app.schemas.recent_searches.RecentSearchResponse import RecentSearchResponse
from app.services.recent_searches.recent_searches import (
    save_search, 
    fetch_recent_searches, 
    delete_search, 
    clear_all_searches
)

router = APIRouter()

@router.post("/recentSearches/add")
def add_recent_searches_route(request: RecentSearchRequest) :
    save_search(request.query)
    return {"message - " : "Recent search saved successfully"}

@router.get("/recentSearches/get", response_model=list[RecentSearchResponse])
def get_recent_searches_route():
    return fetch_recent_searches()

@router.delete("/recentSearches/remove/{id}")
def remove_recent_search_route(id: int):
    delete_search(id)
    return {"message": "Recent search removed successfully"}

@router.delete("/recentSearches/clearall")
def clear_recent_search_route():
    clear_all_searches()
    return {"message - " : "Recent search cleared successfully"}