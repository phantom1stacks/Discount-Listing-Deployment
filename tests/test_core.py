import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite://")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_homepage_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200

def test_register_and_login(client):
    rv = client.post("/register", data={
        "name":"My Shop", "email":"a@b.com",
        "pwd":"secret", "submit":True
    }, follow_redirects=True)
    assert b"Registration successful" in rv.data

    rv = client.post("/login", data={
        "email":"a@b.com", "pwd":"secret", "submit":True
    }, follow_redirects=True)
    assert b"My Shop" in rv.data
