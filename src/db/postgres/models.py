from sqlalchemy.orm import Mapped, mapped_column
from src.db.postgres.config import Base
from typing import Annotated
import datetime
from sqlalchemy import func, text


class AiModels(Base):
    __tablename__ = 'ai_models'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Annotated[str, 200]]
    available: Mapped[bool]

    created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
    updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now
    )]