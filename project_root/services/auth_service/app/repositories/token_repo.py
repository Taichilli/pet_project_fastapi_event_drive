from app.models.refresh_tokens import RefreshToken
from datetime import timedelta, datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class TokenRepository:

    @staticmethod
    async def create_token(db: AsyncSession, user_id: int, token: str, expires_at: datetime = None):
        if not expires_at:
            expires_at = datetime.now(timezone.utc)

        refresh_token_obj = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at + timedelta(days=7),
            revoked=False
        )

        db.add(refresh_token_obj)
        return refresh_token_obj

    @staticmethod
    async def get_by_token(db: AsyncSession, token: str):
        result = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
        return result.scalar_one_or_none()

    @staticmethod
    async def revoke_token(db: AsyncSession, token: str):
        result = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
        refresh_token_obj = result.scalar_one_or_none()
        if not refresh_token_obj:
            return None

        refresh_token_obj.revoked = True
        return refresh_token_obj

    @staticmethod
    async def revoke_all_user_tokens(db: AsyncSession, user_id: int):
        await db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .values(revoked=True)
        )
        # делаю через булк чтобы не грузить в память если вдруг токенов будет 1000 к примеру

    @staticmethod
    async def delete_expired_tokens(db: AsyncSession):
        result = await db.execute(select(RefreshToken).where(RefreshToken.expires_at < datetime.now(timezone.utc)))
        delete_token_obj = result.scalars().all()

        if not delete_token_obj:
            return False

        for token_delete in delete_token_obj:
            db.delete(token_delete)

        return True
