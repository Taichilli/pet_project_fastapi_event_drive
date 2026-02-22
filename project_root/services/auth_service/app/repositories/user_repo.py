from app.db.session import async_session
from app.models.user import User
from app.models.refresh_token import RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession




async def create_user(async_session):



async def get_by_email(user):
    async with async_session.connect() as session:
        await session.execute()
        pass


async def get_by_id(user):
    async with async_session.connect() as session:
        await session.execute()
        pass


async def update_user(user):
    async with async_session.connect() as session:
        await session.execute()
        pass


async def delete_user(user):
    async with async_session.connect() as session:
        await session.execute()
        pass
