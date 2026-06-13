from datetime import datetime, timedelta, timezone

from app.repositories.user_repo import UserRepository
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt_core import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
)
from app.core.security import verify_password
from app.repositories.token_repo import TokenRepository


class AuthService:
    def __init__(self, t_repo: TokenRepository, u_repo: UserRepository):
        self.t_repo = t_repo
        self.u_repo = u_repo

    async def login_user(self, db: AsyncSession, email: str, password: str):
        user = await self.u_repo.get_by_email(db, email)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        now = datetime.now(timezone.utc)

        try:
            raw_token, token_hash = generate_refresh_token()
            await self.t_repo.create_token(
                db, user.id, token_hash, expires_at=now + timedelta(days=7)
            )

            await db.commit()

        except IntegrityError as err:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail="Internal Server Error"
            ) from err

        access_token = create_access_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": raw_token,
            "token_type": "bearer",
        }

    async def refresh_token(self, db: AsyncSession, raw_refresh_token: str):

        rehash_token = hash_refresh_token(raw_refresh_token)
        search_in_db_token = await self.t_repo.get_by_token(db, rehash_token)

        if not search_in_db_token:
            raise HTTPException(status_code=401, detail="Token not found")
        if search_in_db_token.revoked:
            raise HTTPException(status_code=401, detail="Token revoked")
        if search_in_db_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="refresh token expired")

        user_id = search_in_db_token.user_id

        new_access_token = create_access_token(user_id)

        # rotation
        await self.t_repo.revoke_token(db, search_in_db_token)

        raw_new, new_hash = generate_refresh_token()

        await self.t_repo.create_token(
            db,
            user_id,
            new_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )

        await db.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": raw_new,
            "token_type": "bearer",
        }

    async def logout(self, db: AsyncSession, refresh_token: str):
        rehash = hash_refresh_token(refresh_token)

        find_token = await self.t_repo.get_by_token(db, rehash)
        if not find_token or find_token.revoked:
            raise HTTPException(status_code=401, detail="Token not found or revoked")

        await self.t_repo.revoke_token(db, find_token)
        await db.commit()

    async def logout_all_devices(self, db: AsyncSession, refresh_token: str):
        rehash = hash_refresh_token(refresh_token)

        find_token = await self.t_repo.get_by_token(db, rehash)
        if not find_token or find_token.revoked:
            raise HTTPException(status_code=401, detail="Token not found or revoked")

        user_id = find_token.user_id
        await self.t_repo.revoke_all_user_tokens(db, user_id)
        await db.commit()
