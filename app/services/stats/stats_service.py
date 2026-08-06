from app.repositories.stats_repository import (
    get_stats,
    reset_today_counts,
    increment_file_stats,
    increment_search_count,
    increment_download_count,
)
from datetime import date


def reset_today_if_needed():
    stats = get_stats()
    
    today = date.today().isoformat()
    
    if stats["stats_date"] != today:
        reset_today_counts(today)
        
        
def increment_file(file_type: str):
    reset_today_if_needed()
    increment_file_stats(file_type)
    

def increment_search():
    reset_today_if_needed()
    increment_search_count()


def increment_download():
    reset_today_if_needed()
    increment_download_count()


def get_dashboard_stats():
    reset_today_if_needed()
    return get_stats()

