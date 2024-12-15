from datetime import datetime
from typing import List

from sqlalchemy import Integer, Column, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    __table_args__ = {"schema": "comradewolf"}


# Used for many-to-many relation AppUser and OlapTable
user_olap_table = Table(
    "user_olap",
    Base.metadata,
    Column("user_id", ForeignKey("comradewolf.app_user.id"), primary_key=True),
    Column("olap_id", ForeignKey("comradewolf.olap_table.id"), primary_key=True),
)



class OlapTable(Base):
    __tablename__ = "olap_table"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(50), unique=True)
    host: Mapped[str] = Column(String(250), unique=False)
    port: Mapped[str] = Column(Integer, unique=False)
    username_env: Mapped[str] = Column(String(50), unique=True)
    password_env: Mapped[str] = Column(String(50), unique=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now)

    # One-to-many relationship
    app_users: Mapped[List["AppUser"]] = relationship(
        secondary=user_olap_table, back_populates="olap_tables"
    )


class SavedQuery(Base):
    __tablename__ = "saved_query"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    frontend: Mapped[str] = mapped_column(String(), unique=False)
    query: Mapped[str] = mapped_column(String(), unique=False)
    pages: Mapped[str] = mapped_column(Integer)
    items_per_page: Mapped[int] = mapped_column(Integer)


class ConfirmationCode(Base):
    __tablename__ = "confirmation_code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = Column(String(256))
    active: Mapped[bool] = Column(Boolean, default=True)
    created_at: Mapped[datetime] = Column(DateTime)
    expires_at: Mapped[datetime] = Column(DateTime)

    user_id: Mapped[int] = mapped_column(ForeignKey("comradewolf.app_user.id"))
    user: Mapped["AppUser"] = relationship(back_populates="confirmation_codes")

class ForgotPasswordCode(Base):
    __tablename__ = "forgot_password_code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("comradewolf.app_user.id"))
    code: Mapped[str] = Column(String(256), unique=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    expires_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    is_active: Mapped[bool] = Column(Boolean, default=True)

    user: Mapped["AppUser"] = relationship(back_populates="forgot_password_code")

class AppUser(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(50), unique=True)
    password: Mapped[str] = Column(String(512))
    email: Mapped[str] = Column(String(250), unique=True)
    is_active: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime] = Column(DateTime)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now)

    confirmation_codes: Mapped[List["ConfirmationCode"]] = relationship(back_populates="user")
    olap_tables: Mapped[List["OlapTable"]] = relationship(
        secondary=user_olap_table, back_populates="app_users"
    )

    forgot_password_code: Mapped[List["ForgotPasswordCode"]] = relationship(back_populates="user")

