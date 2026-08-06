from fastapi import APIRouter
from app.schemas.stats.DashboardStatsResponse import DashboardStatsResponse
from app.services.stats.stats_service import get_dashboard_stats

router = APIRouter()

@router.get("/stats", response_model=DashboardStatsResponse)
def get_stats() :
    return get_dashboard_stats()