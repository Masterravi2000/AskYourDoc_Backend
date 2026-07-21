from fastapi import APIRouter
from app.repositories import search_query

router = APIRouter()

@router.get("/search")
def search_api(query: str):
    results = search_query(query)
    return {"results": results}