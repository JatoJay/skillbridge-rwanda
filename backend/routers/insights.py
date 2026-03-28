from fastapi import APIRouter
from services.database import db

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("")
async def get_dashboard_insights():
    insights = await db.get_insights()
    return insights


@router.get("/skills")
async def get_top_skills(limit: int = 10):
    insights = await db.get_insights()
    return {"skills": insights["top_skills"][:limit]}


@router.get("/sectors")
async def get_sectors_hiring():
    insights = await db.get_insights()
    return {"sectors": insights["sectors_hiring"]}


@router.get("/gaps")
async def get_skill_gaps_by_region():
    insights = await db.get_insights()
    return {"regions": insights["skill_gaps_by_region"]}


@router.get("/stats")
async def get_platform_stats():
    insights = await db.get_insights()
    return {
        "total_candidates": insights["total_candidates"],
        "total_jobs": insights["total_jobs"],
        "matches_made": insights["matches_made"]
    }
