"""
Judge API endpoint — validates user answers for all game types
"""
import re
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.core.security import verify_token, get_supabase_client

router = APIRouter()


class JudgeRequest(BaseModel):
    level_id: int
    user_prompt: str = ""  # For exact_match, fill_blank
    selected: Optional[List[int]] = None  # For multiple_choice
    user_order: Optional[List[int]] = None  # For reorder
    answers: Optional[List[str]] = None  # For fill_blank


class JudgeResponse(BaseModel):
    success: bool
    feedback: str
    score: int
    ai_output: Optional[str] = None


def judge_exact_match(user_input: str, config: dict) -> tuple:
    """Judge exact match, contains, or regex"""
    expected = config.get("expected", "")
    case_sensitive = config.get("case_sensitive", True)
    match_type = config.get("match_type", "exact")

    compare_input = user_input if case_sensitive else user_input.lower()
    compare_expected = expected if case_sensitive else expected.lower()

    if match_type == "exact":
        if compare_input.strip() == compare_expected.strip():
            return True, "Perfect! Exact match achieved! 🎉", 100
        return False, f"Not quite. Expected exactly: '{expected}'", 0

    elif match_type == "contains":
        if compare_expected in compare_input:
            return True, "Great job! Your output contains the required content! ✨", 100
        return False, f"Your output should contain: '{expected}'", 0

    elif match_type == "regex":
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            if re.search(expected, user_input, flags):
                return True, "Excellent! Pattern matched successfully! 🚀", 100
            return False, "The pattern doesn't match. Try a different approach.", 0
        except re.error:
            return False, "Internal error: Invalid validation pattern.", 0

    return False, "Unknown match type.", 0


def judge_fill_blank(answers: list, config: dict) -> tuple:
    """Judge fill-in-the-blank answers"""
    expected = config.get("answers", [])
    case_sensitive = config.get("case_sensitive", False)

    if not answers or len(answers) != len(expected):
        return False, f"Expected {len(expected)} answers, got {len(answers or [])}", 0

    correct = 0
    for i, (user_ans, exp_ans) in enumerate(zip(answers, expected)):
        u = user_ans.strip() if case_sensitive else user_ans.strip().lower()
        e = exp_ans.strip() if case_sensitive else exp_ans.strip().lower()
        if u == e:
            correct += 1

    if correct == len(expected):
        return True, "All blanks filled correctly! 🎉", 100

    return False, f"You got {correct}/{len(expected)} correct. Keep trying!", int(correct / len(expected) * 100)


def judge_multiple_choice(selected: list, config: dict) -> tuple:
    """Judge multiple choice selection"""
    correct = config.get("correct", [])

    if not selected:
        return False, "Please select an answer.", 0

    if sorted(selected) == sorted(correct):
        return True, "Correct answer! 🎉", 100

    return False, "That's not quite right. Try again!", 0


def judge_reorder(user_order: list, config: dict) -> tuple:
    """Judge drag-and-drop reordering"""
    correct_order = config.get("correct_order", [])

    if not user_order:
        return False, "Please arrange the items.", 0

    if user_order == correct_order:
        return True, "Perfect order! 🎉", 100

    # Partial credit
    correct_positions = sum(1 for u, c in zip(user_order, correct_order) if u == c)
    total = len(correct_order)
    score = int(correct_positions / total * 100)

    return False, f"Almost! {correct_positions}/{total} items in the right position.", score


@router.post("/judge", response_model=JudgeResponse)
async def judge_prompt(
    request: JudgeRequest,
    user: dict = Depends(verify_token)
):
    """Judge a user's submission based on the lesson's game type"""
    supabase = get_supabase_client()

    # Fetch lesson from DB
    result = supabase.table("lessons").select("*").eq("id", request.level_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Level not found")

    lesson = result.data[0]
    game_type = lesson["game_type"]
    config = lesson.get("config", {})

    # Route to correct judge
    if game_type == "exact_match":
        success, feedback, score = judge_exact_match(request.user_prompt, config)
    elif game_type == "fill_blank":
        success, feedback, score = judge_fill_blank(request.answers or [], config)
    elif game_type == "multiple_choice":
        success, feedback, score = judge_multiple_choice(request.selected or [], config)
    elif game_type == "reorder":
        success, feedback, score = judge_reorder(request.user_order or [], config)
    else:
        success, feedback, score = False, f"Game type '{game_type}' not yet supported.", 0

    return JudgeResponse(
        success=success,
        feedback=feedback,
        score=score,
        ai_output=request.user_prompt if game_type == "exact_match" else None
    )
