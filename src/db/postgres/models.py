import datetime
from typing import Annotated

from sqlalchemy import func, text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.postgres.config import Base


class AiModels(Base):
    __tablename__ = "ai_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Annotated[str, 200]]
    available: Mapped[bool]

    created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
    updated_at = Annotated[
        datetime.datetime,
        mapped_column(
            server_default=text("TIMEZONE('utc', now())"),
            onupdate=datetime.datetime.now,
        ),
    ]


class AdminUser(Base):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Annotated[str, 150]] = mapped_column(unique=True, index=True)
    password_hash: Mapped[Annotated[str, 250]]
    is_active: Mapped[bool] = mapped_column(default=True)
