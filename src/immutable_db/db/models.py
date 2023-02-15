from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.schema import Table

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    user_name = relationship("UserName", cascade="delete", uselist=False)

    applications = relationship("Application", secondary="application_user")


class DeletedUser(Base):
    __tablename__ = "deleted_user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    deleted_at = Column(DateTime, default=func.now(), nullable=False)


class UserName(Base):
    __tablename__ = "user_name"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    user_uuid = Column(
        UUID(as_uuid=True), ForeignKey("user.uuid", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    user = relationship("User", back_populates="user_name")


class DeletedUserName(Base):
    __tablename__ = "deleted_user_name"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    deleted_at = Column(DateTime, default=func.now(), nullable=False)
    user_uuid = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)


application_user = Table(
    "application_user",
    Base.metadata,
    Column(
        "application_uuid",
        UUID(as_uuid=True),
        ForeignKey("application.uuid"),
        primary_key=True,
    ),
    Column("user_uuid", UUID(as_uuid=True), ForeignKey("user.uuid"), primary_key=True),
    Column("created_at", DateTime, default=func.now(), nullable=False),
)


class Application(Base):
    __tablename__ = "application"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    users = relationship(
        "User", secondary="application_user", back_populates="applications"
    )


deleted_application_user = Table(
    "deleted_application_user",
    Base.metadata,
    Column(
        "application_uuid",
        UUID(as_uuid=True),
        primary_key=True,
    ),
    Column(
        "user_uuid",
        UUID(as_uuid=True),
        primary_key=True,
    ),
    Column("created_at", DateTime, default=func.now(), nullable=False),
    Column("deleted_at", DateTime, default=func.now(), nullable=False),
)


class DeletedApplication(Base):
    __tablename__ = "deleted_application"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    deleted_at = Column(DateTime, default=func.now(), nullable=False)
