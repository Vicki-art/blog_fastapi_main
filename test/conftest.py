from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest
from app import models
from app.oauth2 import create_token


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}" \
                          f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Testing_SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine )

# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     db = Testing_SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# client = TestClient(app)

@pytest.fixture()
def session():
    # run our code before we run our tests
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # command.upgrade("head")
    # command.upgrade("base")
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "vika@gmail.com",
                 "password": "123"}
    res = client.post("/users/", json = user_data)
    assert res.status_code ==201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "vika2@gmail.com",
                 "password": "123"}
    res = client.post("/users/", json = user_data)
    assert res.status_code ==201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd user post",
        "content": "2nd user content",
        "owner_id": test_user2['id']
    }, {
        "title": "2nd user post",
        "content": "2nd user content",
        "published": False,
        "owner_id": test_user['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                  models.Post(title="second title", content="second content", owner_id=test_user['id']),
    #                   models.Post(title="third title", content="third content", owner_id=test_user['id'])])
    session.commit()
    posts = session.query(models.Post).all()
    return posts



