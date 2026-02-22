from typing import List,Optional
from sqlalchemy import ForeignKey,String,DateTime,Boolean,text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
import datetime


class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc',now())"),
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc',now())"),
        nullable=False
    )
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
