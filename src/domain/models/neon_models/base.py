from datetime import datetime
from sqlalchemy import MetaData, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata_ = MetaData()


class MinimalBase(DeclarativeBase):
    """Neon DB models"""
    __abstract__ = True
    metadata = metadata_


class IDOrmModel(MinimalBase):
    """Basic abstract class for using with all Neon models"""
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_delete: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
