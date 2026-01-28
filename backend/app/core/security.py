"""
Security utilities for JWT validation with Supabase
"""
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from supabase import create_client, Client

from app.core.config import settings

security = HTTPBearer()


def get_supabase_client() -> Client:
    """Create Supabase client"""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Verify Supabase JWT token and return user data
    """
    token = credentials.credentials
    
    try:
        supabase = get_supabase_client()
        # Verify token with Supabase
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        
        return {
            "user_id": user_response.user.id,
            "email": user_response.user.email,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Optional[dict]:
    """
    Optionally verify token - returns None if no token provided
    """
    if not credentials:
        return None
    return await verify_token(credentials)
