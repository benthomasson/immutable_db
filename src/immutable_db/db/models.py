
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
    func
)


Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime, nullable=True)


class DeletedUser(Base):

    __tablename__ = 'deleted_user'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime, default=func.now())

