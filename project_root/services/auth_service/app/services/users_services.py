from app.core.security import hash_password, verify_password
from app.repositories.users_repository import UserRepository
from app.schemas.schemas import CreateUser
from fastapi import HTTPException, WebSocketException
from sqlalchemy.ext.asyncio import AsyncSession


class UserServices:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, db: AsyncSession, user: CreateUser):
        examination = await self.repo.get_by_email(db, user.email)

        if examination is not None:
            raise HTTPException(status_code=400, detail="This email is already in use.")

        hashed_password = hash_password(user.password)

        new_users = await self.repo.create_user(
            db,
            user.name,
            user.email,
            hashed_password
        )

        try:
            await db.commit()
            await db.refresh(new_users)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="User already exists")
        except OperationalError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Database error")

        return new_users
