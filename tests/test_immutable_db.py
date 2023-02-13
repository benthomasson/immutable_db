import logging

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, scoped_session, sessionmaker

from immutable_db.db import models

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def connection():
    engine = create_engine("postgresql://@localhost:5432/immutable_db_test")
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    with connection.begin():
        models.Base.metadata.create_all(bind=connection)

    yield

    models.Base.metadata.drop_all(bind=connection)


@pytest.fixture
def db_session(setup_database, connection):
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )


def test_user(db_session):
    user = models.User()
    db_session.add(user)
    db_session.commit()
    assert user.uuid

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one()
    assert o.uuid == user.uuid


def test_delete_user(db_session):
    user = models.User()
    db_session.add(user)
    db_session.commit()
    assert user.uuid

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one()
    assert o.uuid == user.uuid

    deleted_user = models.DeletedUser(uuid=user.uuid, created_at=user.created_at)
    db_session.add(deleted_user)
    db_session.delete(user)
    db_session.commit()

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one_or_none()
    assert o is None

    o = (
        db_session.query(models.DeletedUser)
        .where(models.DeletedUser.uuid == user.uuid)
        .one()
    )
    assert o.uuid == user.uuid
    assert o.created_at == user.created_at
    assert o.deleted_at == deleted_user.deleted_at
