from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class CreateUser(UserBase):
    name: str
    email: EmailStr
    password: str

class UpdateUser(UserBase):
    password: Optional[str] = None

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str