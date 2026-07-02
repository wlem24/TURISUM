from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
from app.schemas.user import UserOut
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: RegisterRequest, session: AsyncSession = Depends(get_db)):
    service = AuthService(session)
    user = await service.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, response: Response, session: AsyncSession = Depends(get_db)):
    service = AuthService(session)
    result = await service.login(data.email, data.password)
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 3600,
    )
    return TokenResponse(
        access_token=result["access_token"],
        token_type=result["token_type"],
        role=result["role"],
        user_id=result["user_id"],
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, response: Response, session: AsyncSession = Depends(get_db)):
    service = AuthService(session)
    result = await service.refresh(data.refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 3600,
    )
    return TokenResponse(
        access_token=result["access_token"],
        token_type=result["token_type"],
        role=result["role"],
        user_id=result["user_id"],
    )


@router.post("/logout", status_code=204)
async def logout(response: Response, _: User = Depends(get_current_user)):
    response.delete_cookie("refresh_token")
