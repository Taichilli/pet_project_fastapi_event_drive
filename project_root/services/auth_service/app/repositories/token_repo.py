from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_tokens import RefreshToken


class TokenRepository:
    @staticmethod
    async def create_token(
        db: AsyncSession, user_id: int, token_hash: str, expires_at: datetime = None
    ):
        if not expires_at:
            expires_at = datetime.now(timezone.utc)

        refresh_token_obj = RefreshToken(
            user_id=user_id, token_hash=token_hash, expires_at=expires_at, revoked=False
        )

        db.add(refresh_token_obj)
        return refresh_token_obj

    @staticmethod
    async def get_by_token(db: AsyncSession, token_hash: str):
        result = await db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def revoke_token(db: AsyncSession, token: RefreshToken):
        token.revoked = True
        return token

    @staticmethod
    async def revoke_all_user_tokens(db: AsyncSession, user_id: int):
        await db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .values(revoked=True)
        )


    @staticmethod
    async def delete_expired_tokens(db: AsyncSession):
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.expires_at < datetime.now(timezone.utc)
            )
        )
        delete_token_obj = result.scalars().all()

        if not delete_token_obj:
            return False

        for token_delete in delete_token_obj:
            db.delete(token_delete)

        return True
