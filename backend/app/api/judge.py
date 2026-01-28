"""
Judge API endpoint
"""
from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import JudgeRequest, JudgeResponse
from app.core.security import verify_token
from app.services.static_judge import judge_static
from levels.definitions import get_level_by_id

router = APIRouter()


@router.post("/judge", response_model=JudgeResponse)
async def judge_prompt(
    request: JudgeRequest,
    user: dict = Depends(verify_token)
):
    """
    Judge a user's prompt submission.
    
    - Levels 1-10: Static validation (regex/exact match)
    - Levels 11+: LLM-based validation (requires credits)
    """
    # Get level configuration
    level = get_level_by_id(request.level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    
    # Static mode (levels 1-10)
    if level["mode"] == "static":
        validation = level.get("validation", {})
        success, feedback, score = judge_static(request.user_prompt, validation)
        
        return JudgeResponse(
            success=success,
            feedback=feedback,
            score=score,
            ai_output=request.user_prompt  # For static, input = output
        )
    
    # LLM mode (levels 11+) - Placeholder for now
    else:
        # TODO: Implement LLM-based judging
        return JudgeResponse(
            success=False,
            feedback="LLM-based judging coming soon!",
            score=0,
            ai_output=None
        )
