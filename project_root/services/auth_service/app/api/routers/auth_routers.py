from fastapi import APIRouter, Depends, Cookie, Response,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.session import get_db
from app.api.deps import get_auth_service,get_user_service,get_current_user
from app.schemas.schemas import  CreateUser,LoginRequest,UserRead,Token,MessageResponse
from app.services.users_services import UserServices
from app.services.token_services import AuthService



router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead)
async def register_user(
        user_data: CreateUser,
        db: AsyncSession = Depends(get_db),
        service: UserServices = Depends(get_user_service),
):

    new_user = await service.register_user(db,user_data)

    return new_user


@router.post("/login", response_model=Token)
async def login_user(
        user_data: LoginRequest,
        response: Response,
        db: AsyncSession = Depends(get_db),
        service: AuthService = Depends(get_auth_service),
):

    login_response = await service.login_user(
        db,
        user_data.email,
        user_data.password
    )

    response.set_cookie(
        key="refresh_token",
        value=login_response["refresh_token"],
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=7 * 24 * 60 * 60,

    )

    return {
        "access_token": login_response["access_token"],
        "token_type": "bearer",
    }



@router.post("/refresh", response_model=Token)
async def refresh_user(
        response: Response,
        refresh_token: Annotated[str, Cookie()],
        db: AsyncSession = Depends(get_db),
        service: AuthService = Depends(get_auth_service),
):

        refresh_token_response = await service.refresh_token(db,refresh_token)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token_response["refresh_token"],
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return {
            "access_token": refresh_token_response["access_token"],
            "token_type": "bearer",
        }

@router.post("/logout",response_model=MessageResponse)
async def logout(
        response: Response,
        refresh_token: Annotated[str, Cookie()],
        db: AsyncSession = Depends(get_db),
        service: AuthService = Depends(get_auth_service),

):
        await service.logout(db,refresh_token)

        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return {"message": "logout successful"}


@router.post("/logout-all",response_model=MessageResponse)
async def logout_all(
        response: Response,
        refresh_token: Annotated[str, Cookie()],
        db: AsyncSession = Depends(get_db),
        service: AuthService = Depends(get_auth_service),
):
        if not refresh_token:
            raise HTTPException(status_code=401, detail="No token provided")

        await service.logout_all(db,refresh_token)

        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return {"message": "logout all devices successful"}

