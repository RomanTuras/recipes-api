from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata_ = MetaData()


class MinimalBase(DeclarativeBase):
    """Sqlite DB models"""
    __abstract__ = True
    metadata = metadata_


class IDOrmModel(MinimalBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(name="_id", primary_key=True)
