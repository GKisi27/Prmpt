"""
Admin API endpoints for managing lessons
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.security import verify_token, get_supabase_client

router = APIRouter()


# --- Models ---
class LessonCreate(BaseModel):
    title: str
    description: Optional[str] = None
    goal: str
    game_type: str = "exact_match"
    difficulty: str = "beginner"
    order_index: int = 0
    config: dict = {}
    time_limit: Optional[int] = None
    is_published: bool = False


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    goal: Optional[str] = None
    game_type: Optional[str] = None
    difficulty: Optional[str] = None
    order_index: Optional[int] = None
    config: Optional[dict] = None
    time_limit: Optional[int] = None
    is_published: Optional[bool] = None


# --- Helpers ---
async def verify_admin(user: dict = Depends(verify_token)) -> dict:
    """Verify the user has admin role"""
    supabase = get_supabase_client()
    user_response = supabase.auth.admin.get_user_by_id(user["user_id"])

    if not user_response or not user_response.user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    role = (user_response.user.user_metadata or {}).get("role", "")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user


# --- Routes ---
@router.get("/admin/lessons")
async def list_all_lessons(user: dict = Depends(verify_admin)):
    """List ALL lessons (including unpublished) for admin"""
    supabase = get_supabase_client()
    result = supabase.table("lessons").select("*").order("order_index").execute()
    return {"lessons": result.data, "total": len(result.data)}


@router.post("/admin/lessons", status_code=status.HTTP_201_CREATED)
async def create_lesson(lesson: LessonCreate, user: dict = Depends(verify_admin)):
    """Create a new lesson"""
    supabase = get_supabase_client()
    result = supabase.table("lessons").insert(lesson.model_dump()).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create lesson")

    return {"lesson": result.data[0], "message": "Lesson created successfully"}


@router.get("/admin/lessons/{lesson_id}")
async def get_lesson(lesson_id: int, user: dict = Depends(verify_admin)):
    """Get a single lesson by ID (admin view)"""
    supabase = get_supabase_client()
    result = supabase.table("lessons").select("*").eq("id", lesson_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return result.data[0]


@router.put("/admin/lessons/{lesson_id}")
async def update_lesson(
    lesson_id: int,
    lesson: LessonUpdate,
    user: dict = Depends(verify_admin)
):
    """Update an existing lesson"""
    supabase = get_supabase_client()
    update_data = {k: v for k, v in lesson.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = supabase.table("lessons").update(update_data).eq("id", lesson_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return {"lesson": result.data[0], "message": "Lesson updated successfully"}


@router.delete("/admin/lessons/{lesson_id}")
async def delete_lesson(lesson_id: int, user: dict = Depends(verify_admin)):
    """Delete a lesson"""
    supabase = get_supabase_client()
    result = supabase.table("lessons").delete().eq("id", lesson_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return {"message": "Lesson deleted successfully"}


@router.get("/admin/game-types")
async def list_game_types(user: dict = Depends(verify_admin)):
    """Return available game types and their config schemas"""
    return {
        "game_types": [
            {
                "id": "exact_match",
                "name": "Exact Match",
                "description": "User types the exact expected output",
                "config_schema": {
                    "expected": {"type": "string", "required": True, "label": "Expected Answer"},
                    "case_sensitive": {"type": "boolean", "default": True, "label": "Case Sensitive"},
                    "match_type": {"type": "select", "options": ["exact", "contains", "regex"], "default": "exact", "label": "Match Type"},
                }
            },
            {
                "id": "fill_blank",
                "name": "Fill in the Blank",
                "description": "User fills in missing words in a template",
                "config_schema": {
                    "template": {"type": "string", "required": True, "label": "Template (use {{blank}} for blanks)"},
                    "answers": {"type": "string_array", "required": True, "label": "Answers (in order)"},
                    "case_sensitive": {"type": "boolean", "default": False, "label": "Case Sensitive"},
                }
            },
            {
                "id": "multiple_choice",
                "name": "Multiple Choice",
                "description": "User selects the correct option(s)",
                "config_schema": {
                    "question": {"type": "string", "required": True, "label": "Question"},
                    "options": {"type": "string_array", "required": True, "label": "Options"},
                    "correct": {"type": "number_array", "required": True, "label": "Correct Option Indices (0-based)"},
                    "multi": {"type": "boolean", "default": False, "label": "Allow Multiple Selections"},
                }
            },
            {
                "id": "reorder",
                "name": "Reorder / Drag & Drop",
                "description": "User arranges items in the correct order by dragging",
                "config_schema": {
                    "items": {"type": "string_array", "required": True, "label": "Items (in correct order)"},
                    "correct_order": {"type": "number_array", "required": True, "label": "Correct Order Indices"},
                }
            },
        ]
    }


# ============================================
# User Management
# ============================================

class UserRoleUpdate(BaseModel):
    role: str = ""  # "admin" or "" for regular user


@router.get("/admin/users")
async def list_users(user: dict = Depends(verify_admin)):
    """List all users"""
    supabase = get_supabase_client()
    result = supabase.auth.admin.list_users()

    users = []
    for u in result:
        users.append({
            "id": str(u.id),
            "email": u.email,
            "role": (u.user_metadata or {}).get("role", "user"),
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "last_sign_in_at": u.last_sign_in_at.isoformat() if u.last_sign_in_at else None,
            "email_confirmed": u.email_confirmed_at is not None,
        })

    return {"users": users, "total": len(users)}


@router.put("/admin/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    role_update: UserRoleUpdate,
    user: dict = Depends(verify_admin)
):
    """Update a user's role"""
    supabase = get_supabase_client()
    result = supabase.auth.admin.update_user_by_id(
        user_id,
        {"user_metadata": {"role": role_update.role}}
    )

    if not result or not result.user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message": f"User role updated to '{role_update.role or 'user'}'",
        "user_id": user_id,
    }


@router.delete("/admin/users/{user_id}")
async def delete_user(user_id: str, user: dict = Depends(verify_admin)):
    """Delete a user"""
    # Prevent self-deletion
    if user_id == user["user_id"]:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    supabase = get_supabase_client()
    supabase.auth.admin.delete_user(user_id)

    return {"message": "User deleted successfully"}

