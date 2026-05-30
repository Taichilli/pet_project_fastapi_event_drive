from fastapi import APIRouter
from app.schemas.schemas import  UserBase,CreateUser,LoginRequest,UpdateUser,UserRead,Token,MassegeResponse

router = APIRouter()



@router.get("/me")
async def get_me():
    pass


@router.patch("/me")
async def patch_me():
    pass

@router.delete("/me")
async def delete_me():
    pass
