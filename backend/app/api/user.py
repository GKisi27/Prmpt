"""
User API endpoint
"""
from fastapi import APIRouter, Depends

from app.models.schemas import UserCredits, CreditDeductRequest
from app.core.security import verify_token

router = APIRouter()

# In-memory credits storage (replace with Supabase in production)
user_credits: dict = {}
DEFAULT_CREDITS = 50


@router.get("/user/credits", response_model=UserCredits)
async def get_credits(user: dict = Depends(verify_token)):
    """Get user's current credit balance"""
    user_id = user["user_id"]
    credits = user_credits.get(user_id, DEFAULT_CREDITS)
    return UserCredits(credits=credits, user_id=user_id)


@router.post("/user/credits/deduct", response_model=UserCredits)
async def deduct_credits(
    request: CreditDeductRequest,
    user: dict = Depends(verify_token)
):
    """Deduct credits from user's balance"""
    user_id = user["user_id"]
    current = user_credits.get(user_id, DEFAULT_CREDITS)
    
    new_balance = max(0, current - request.amount)
    user_credits[user_id] = new_balance
    
    return UserCredits(credits=new_balance, user_id=user_id)


@router.post("/user/credits/initialize", response_model=UserCredits)
async def initialize_credits(user: dict = Depends(verify_token)):
    """Initialize credits for new user"""
    user_id = user["user_id"]
    if user_id not in user_credits:
        user_credits[user_id] = DEFAULT_CREDITS
    return UserCredits(credits=user_credits[user_id], user_id=user_id)
