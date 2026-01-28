"""
Pydantic models for API requests and responses
"""
from typing import Optional, Literal
from pydantic import BaseModel


# Level Models
class LevelValidation(BaseModel):
    type: Literal["exact", "contains", "regex"]
    expected: str
    case_sensitive: bool = True


class Level(BaseModel):
    id: int
    title: str
    description: str
    goal: str
    mode: Literal["static", "llm"]
    validation: Optional[LevelValidation] = None
    system_prompt: Optional[str] = None
    difficulty: Literal["beginner", "intermediate", "advanced"] = "beginner"


# Judge Models
class JudgeRequest(BaseModel):
    level_id: int
    user_prompt: str
    ai_provider: Optional[Literal["openai", "gemini", "claude", "grok"]] = "openai"


class JudgeResponse(BaseModel):
    success: bool
    feedback: str
    score: int
    ai_output: Optional[str] = None


# User Models
class UserCredits(BaseModel):
    credits: int
    user_id: str


class CreditDeductRequest(BaseModel):
    amount: int = 1
