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
    applications = relationship("Application")


class DeletedUser(Base):
    __tablename__ = "deleted_user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    deleted_at = Column(DateTime, default=func.now(), nullable=False)

    user_name = relationship("DeletedUserName", uselist=False)
    applications = relationship("DeletedApplication")


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
    user_uuid = Column(
        UUID(as_uuid=True), ForeignKey("deleted_user.uuid"), nullable=False
    )
    name = Column(String(255), nullable=False)

    user = relationship("DeletedUser", back_populates="user_name")


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
)


class Application(Base):
    __tablename__ = "application"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    users = relationship(
        "User", secondary="application_user", back_populates="applications"
    )


application_user = Table(
    "deleted_application_user",
    Base.metadata,
    Column(
        "application_uuid",
        UUID(as_uuid=True),
        ForeignKey("deleted_application.uuid"),
        primary_key=True,
    ),
    Column(
        "user_uuid",
        UUID(as_uuid=True),
        ForeignKey("deleted_user.uuid"),
        primary_key=True,
    ),
)


class DeletedApplication(Base):
    __tablename__ = "deleted_application"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    deleted_at = Column(DateTime, default=func.now(), nullable=False)

    users = relationship(
        "DeletedUser", secondary="application_user", back_populates="applications"
    )
