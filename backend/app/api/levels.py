"""
Levels API endpoint — reads from Supabase DB
"""
from fastapi import APIRouter, HTTPException

from app.core.security import get_supabase_client

router = APIRouter()


@router.get("/levels")
async def list_levels():
    """Get all published levels, ordered by order_index"""
    supabase = get_supabase_client()
    result = (
        supabase.table("lessons")
        .select("*")
        .eq("is_published", True)
        .order("order_index")
        .execute()
    )
    return {"levels": result.data, "total": len(result.data)}


@router.get("/levels/{level_id}")
async def get_level(level_id: int):
    """Get a specific published level by ID"""
    supabase = get_supabase_client()
    result = (
        supabase.table("lessons")
        .select("*")
        .eq("id", level_id)
        .eq("is_published", True)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Level not found")

    return result.data[0]
