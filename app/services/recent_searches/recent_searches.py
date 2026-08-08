from app.repositories.recent_search_repository import (
    save_recent_search,
    get_recent_searches,
    delete_recent_search,
    clear_recent_searches,
)

def save_search(query: str):
    save_recent_search(query)

def fetch_recent_searches():
    return get_recent_searches()

def delete_search(id: int):
    delete_recent_search(id)
    
def clear_all_searches():
    clear_recent_searches()