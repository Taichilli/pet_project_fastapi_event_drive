from app.repositories.user_repo import UserRepository
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.schemas.schemas import CreateUser, UpdateUser


class UserServices:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, db: AsyncSession, user: CreateUser):
        examination = await self.repo.get_by_email(db, user.email)

        if examination is not None:
            raise HTTPException(status_code=400, detail="This email is already in use.")

        hashed_password = hash_password(user.password)

        new_user = await self.repo.create_user(
            db, user.name, user.email, hashed_password
        )

        try:
            await db.commit()
            await db.refresh(new_user)
        except IntegrityError as err:
            await db.rollback()
            raise HTTPException(status_code=400, detail="User already exists") from err
        except OperationalError as err:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Database error") from err

        return new_user

    async def update_user(self, db: AsyncSession, user_id: int, data: UpdateUser):
        user = await self.repo.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if data.name:
            user.name = data.name

        if data.email:
            user.email = data.email

        if data.password:
            user.hashed_password = hash_password(data.password)

        try:
            await db.commit()
            await db.refresh(user)
        except IntegrityError as err:
            await db.rollback()
            raise HTTPException(status_code=400, detail="User already exists") from err

        return user

    async def delete_user(self, db, user_id):
        user = await self.repo.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.repo.delete_user(db, user)
        await db.commit()

        return {"message": "deleted"}
