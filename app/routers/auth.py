from fastapi import APIRouter, HTTPException, status

from app.core.security import authenticate_admin, create_access_token
from app.schemas.auth import LoginRequest, TokenResponse


router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    if not authenticate_admin(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=payload.username, role="admin")
    return TokenResponse(access_token=access_token)
