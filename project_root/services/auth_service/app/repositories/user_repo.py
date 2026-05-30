from typing import Optional

from app.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    @staticmethod
    async def create_user(
        db: AsyncSession, name: str, email: str, password: str
    ) -> User:

        user = User(
            name=name,
            email=email,
            hashed_password=password,
        )
        db.add(user)
        return user

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:

        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:

        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        password: str = None,
        name: str = None,
        email: str = None,
    ) -> Optional[User]:

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None

        if password is not None:
            user.hashed_password = password
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email

        return user

    # commit -> services

    @staticmethod
    async def delete_user(db: AsyncSession, user: User):
        await db.delete(user)

    # commit -> services
