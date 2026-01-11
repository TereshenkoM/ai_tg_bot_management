import datetime
from typing import Annotated, Any

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, DateTime, Index, func
from sqlalchemy.dialects.postgresql import JSONB

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

    class Meta:
        admin_title = "AI Models"
        admin_icon = "cpu"
        admin_default_order = ("id",)
        admin_columns = ("id", "name", "available")


class AdminUser(Base):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Annotated[str, 150]] = mapped_column(unique=True, index=True)
    password_hash: Mapped[Annotated[str, 250]]
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
    updated_at = Annotated[
        datetime.datetime,
        mapped_column(
            server_default=text("TIMEZONE('utc', now())"),
            onupdate=datetime.datetime.now,
        ),
    ]


class ModelResponses(Base):
    __tablename__ = "model_responses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
    updated_at = Annotated[
        datetime.datetime,
        mapped_column(
            server_default=text("TIMEZONE('utc', now())"),
            onupdate=datetime.datetime.now,
        ),
    ]

    __table_args__ = (
        Index("ix_json_store_data_gin", "data", postgresql_using="gin"),
    )

    class Meta:
        admin_title = "Model responses"
        admin_icon = "message-square"
        admin_default_order = ("-id",)
        admin_columns = ("id", "data", "created_at")
