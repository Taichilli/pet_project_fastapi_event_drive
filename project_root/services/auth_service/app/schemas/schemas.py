from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class CreateUser(UserBase):
    password: str = Field(..., min_length=8, max_length=40)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    password: Optional[str] = Field(None, min_length=8, max_length=40)
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class MessageResponse(BaseModel):
    message: str