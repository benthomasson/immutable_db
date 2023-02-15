import logging
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import scoped_session, sessionmaker

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


def model_data(o):
    data = o.__dict__.copy()
    data.pop("_sa_instance_state")
    return data


def test_delete_user(db_session):
    user = models.User()
    db_session.add(user)
    db_session.commit()
    assert user.uuid

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one()
    assert o.uuid == user.uuid

    deleted_user = models.DeletedUser(**model_data(user))
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


def test_user_name(db_session):
    user = models.User(uuid=uuid4())
    name = models.UserName(name="test", user_uuid=user.uuid)
    db_session.add(user)
    db_session.add(name)
    db_session.commit()
    assert user.uuid

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one()
    assert o.uuid == user.uuid

    o = db_session.query(models.UserName).where(models.UserName.name == "test").one()
    assert o.user_uuid == user.uuid


def test_delete_user_name_cascade(db_session):
    user = models.User(uuid=uuid4())
    name = models.UserName(name="test_delete", user_uuid=user.uuid)
    db_session.add(user)
    db_session.add(name)
    db_session.commit()
    assert user.uuid

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one()
    assert o.uuid == user.uuid

    o = (
        db_session.query(models.UserName)
        .where(models.UserName.name == "test_delete")
        .one()
    )
    assert o.user_uuid == user.uuid

    # db_session.delete(name)
    # db_session.commit()
    db_session.delete(user)
    db_session.commit()

    o = (
        db_session.query(models.UserName)
        .where(models.UserName.name == "test_delete")
        .all()
    )
    assert len(o) == 0


def test_delete_user_name_no_cascade(db_session):
    user = models.User(uuid=uuid4())
    name = models.UserName(name="test_delete", user_uuid=user.uuid)
    db_session.add(user)
    db_session.add(name)
    db_session.commit()
    assert user.uuid

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one()
    assert o.uuid == user.uuid

    o = (
        db_session.query(models.UserName)
        .where(models.UserName.name == "test_delete")
        .one()
    )
    assert o.user_uuid == user.uuid

    db_session.delete(name)
    db_session.commit()
    db_session.delete(user)
    db_session.commit()

    o = (
        db_session.query(models.UserName)
        .where(models.UserName.name == "test_delete")
        .all()
    )
    assert len(o) == 0


def test_delete_user_name_copy(db_session):
    user = models.User(uuid=uuid4())
    name = models.UserName(name="test_delete", user_uuid=user.uuid)
    db_session.add(user)
    db_session.add(name)
    db_session.commit()
    assert user.uuid

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one()
    assert o.uuid == user.uuid

    o = (
        db_session.query(models.UserName)
        .where(models.UserName.name == "test_delete")
        .one()
    )
    assert o.user_uuid == user.uuid

    deleted_user = models.DeletedUser(**model_data(user))
    deleted_user_name = models.DeletedUserName(**model_data(name))
    db_session.add(deleted_user)
    db_session.add(deleted_user_name)
    db_session.delete(user)
    db_session.commit()

    o = (
        db_session.query(models.UserName)
        .where(models.UserName.name == "test_delete")
        .all()
    )
    assert len(o) == 0

    o = (
        db_session.query(models.DeletedUserName)
        .where(models.DeletedUserName.name == "test_delete")
        .all()
    )
    assert len(o) == 1

    assert o[0].user_uuid == user.uuid


def test_user_application(db_session):
    app = models.Application(uuid=uuid4())
    user = models.User(uuid=uuid4())
    db_session.add(app)
    db_session.add(user)
    db_session.commit()
    app.users.append(user)
    db_session.commit()
    # q = insert(models.application_user).values(
    #    application_uuid=app.uuid, user_uuid=user.uuid, created_at=datetime.utcnow()
    # )
    # db_session.execute(q)
    assert user.uuid

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one()
    assert o.uuid == user.uuid

    o = (
        db_session.query(models.Application)
        .where(models.Application.uuid == app.uuid)
        .one()
    )
    assert o.uuid == app.uuid

    assert len(o.users) == 1
    assert o.users[0].uuid == user.uuid


def test_user_application_delete(db_session):
    app = models.Application(uuid=uuid4())
    user = models.User(uuid=uuid4())
    db_session.add(app)
    db_session.add(user)
    db_session.commit()
    app.users.append(user)
    db_session.commit()
    # q = insert(models.application_user).values(
    #    application_uuid=app.uuid, user_uuid=user.uuid, created_at=datetime.utcnow()
    # )
    # db_session.execute(q)
    assert user.uuid, "Expected user to have a uuid"

    o = db_session.query(models.User).where(models.User.uuid == user.uuid).one()
    assert o.uuid == user.uuid, "Expected to find user by uuid"

    o = (
        db_session.query(models.Application)
        .where(models.Application.uuid == app.uuid)
        .one()
    )
    assert o.uuid == app.uuid, "did not find app"

    assert len(o.users) == 1, "user not added to application"
    assert o.users[0].uuid == user.uuid, "user not added to application"

    q = select(models.application_user).where(
        models.application_user.c.user_uuid == user.uuid
    )
    assert db_session.execute(q).fetchone() is not None, "user not added to application"

    # Save the user into the deleted table
    deleted_user = models.DeletedUser(**model_data(user))
    db_session.add(deleted_user)

    # Save the user application relationship into the deleted table
    for an_app in user.applications:
        q = insert(models.deleted_application_user).values(
            user_uuid=user.uuid, application_uuid=an_app.uuid
        )
        db_session.execute(q)
    # Delete the user
    db_session.delete(user)
    db_session.commit()

    o = (
        db_session.query(models.Application)
        .where(models.Application.uuid == app.uuid)
        .one()
    )
    assert o.uuid == app.uuid

    assert len(o.users) == 0, "Expected no users"

    o = (
        db_session.query(models.DeletedUser)
        .where(models.DeletedUser.uuid == user.uuid)
        .one()
    )
    assert o.uuid == user.uuid, "Expected deleted user"

    q = select(models.application_user).where(
        models.application_user.c.user_uuid == user.uuid
    )
    assert db_session.execute(q).fetchone() is None, "Expected no application_user"

    q = select(models.deleted_application_user).where(
        models.deleted_application_user.c.user_uuid == user.uuid
    )
    assert (
        db_session.execute(q).fetchone() is not None
    ), "Expected deleted_application_user"
