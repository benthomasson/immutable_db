from uuid import uuid4

import sqlalchemy as sa

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Table

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
    JSON,
    func,
)


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    user_name = relationship("UserName", cascade="delete")


class DeletedUser(Base):
    __tablename__ = "deleted_user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    deleted_at = Column(DateTime, default=func.now(), nullable=False)


class UserName(Base):
    __tablename__ = "user_name"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    user = relationship("User", back_populates="user_name")


class DeletedUserName(Base):
    __tablename__ = "deleted_user_name"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    deleted_at = Column(DateTime, default=func.now(), nullable=False)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("deleted_user.uuid"), nullable=False)
    name = Column(String(255), nullable=False)

