from fastapi import APIRouter, Depends, Response
from app.schemas.schemas import  UpdateUser,UserRead,MessageResponse
from app.api.deps import get_current_user,get_user_service
from app.services.users_services import UserServices
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/users", tags=["Users"])



@router.get("/me", response_model=UserRead)
async def get_me(
        current_user = Depends(get_current_user),
    ):

    return current_user


@router.patch("/me", response_model=UserRead)
async def patch_me(
        user_data: UpdateUser,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user),
        services: UserServices = Depends(get_user_service),
    ):
    update_current_user = await services.update_user(
        db,
        current_user.id,
        user_data
    )

    return update_current_user

@router.delete("/me",response_model=MessageResponse)
async def delete_me(
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user),
        services: UserServices = Depends(get_user_service),
    ):

    await services.delete_user(db,current_user.id)

    return {"message": "delete user successfully"}

