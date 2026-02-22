from typing import List, Optional
from sqlalchemy import Column, String, text, DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
import datetime



class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50),unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc',now())"),
        nullable=False
    )

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user")



