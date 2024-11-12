from datetime import datetime

from sqlalchemy import Integer, Column, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    __table_args__ = {"schema": "comradewolf"}


class CubeInfo(Base):
    __tablename__ = "cube_info"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(50), unique=True)
    host: Mapped[str] = Column(String(250), unique=False)
    port: Mapped[str] = Column(Integer, unique=False)
    username_env: Mapped[str] = Column(String(50), unique=True)
    password_env: Mapped[str] = Column(String(50), unique=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now)

class AppUser(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(50), unique=True)
    password: Mapped[str] = Column(String(256))
    email: Mapped[str] = Column(String(250), unique=True)
    is_active: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now)

class SavedQuery(Base):
    __tablename__ = "saved_query"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    frontend: Mapped[str] = mapped_column(String(), unique=False)
    query: Mapped[str] = mapped_column(String(), unique=False)
    pages: Mapped[str] = mapped_column(Integer)
    items_per_page: Mapped[int] = mapped_column(Integer)
