from app.repositories.token_repo import TokenRepository
from app.repositories.user_repo import UserRepository
from app.services.token_services import AuthService
from app.services.users_services import UserServices
from app.core.jwt_core import decode_token
from app.db.session import get_db

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, ExpiredSignatureError, jwt




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_auth_service():
    token_repository = TokenRepository()
    user_repository = UserRepository()
    return AuthService(token_repository, user_repository)

def get_user_service():
    user_repository = UserRepository()
    return UserServices(user_repository)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = decode_token(token)
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

    except (ExpiredSignatureError, JWTError) as err:
        raise HTTPException(
            status_code=401,
            detail="Could not validate token",
        ) from err

    user = await UserRepository.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user