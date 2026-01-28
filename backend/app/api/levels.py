"""
Levels API endpoint
"""
from typing import List
from fastapi import APIRouter, HTTPException

from app.models.schemas import Level
from levels.definitions import get_all_levels, get_level_by_id

router = APIRouter()


@router.get("/levels")
async def list_levels():
    """Get all available levels"""
    levels = get_all_levels()
    return {"levels": levels, "total": len(levels)}


@router.get("/levels/{level_id}")
async def get_level(level_id: int):
    """Get a specific level by ID"""
    level = get_level_by_id(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level
