
import pytest
import sys
from pathlib import Path

# Make the backend importable when tests run from the project root.
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "backend"))

import app as gallery_app


@pytest.fixture
def client(monkeypatch):
    gallery_app.app.config.update(
        TESTING=True,
        SECRET_KEY="test-only-secret",
    )

    # Prevent tests from depending on the real database.
    monkeypatch.setattr(gallery_app, "viewAllRooms", lambda: [])
    monkeypatch.setattr(gallery_app, "seeCurrentRoom", lambda user_id: "Gallery")
    monkeypatch.setattr(gallery_app, "seeAuditHistory", lambda: [])
    monkeypatch.setattr(gallery_app, "viewAllUsers", lambda: [])
    monkeypatch.setattr(gallery_app, "seeEventHistory", lambda: [])
    monkeypatch.setattr(gallery_app, "addSession", lambda *args: 1)
    monkeypatch.setattr(gallery_app, "endSession", lambda *args: None)

    with gallery_app.app.test_client() as test_client:
        yield test_client


def login_as(client, role="Guest"):
    with client.session_transaction() as session:
        session["loggedin"] = True
        session["id"] = 1
        session["username"] = "testuser"
        session["role"] = role
        session["sessionID"] = 1


def test_home_redirects_when_logged_out(client):
    response = client.get("/home")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logged_in_user_can_view_home(client):
    login_as(client)

    response = client.get("/home")

    assert response.status_code == 200
    assert b"testuser" in response.data


def test_admin_can_view_users(client):
    login_as(client, role="Admin")

    response = client.get("/users")

    assert response.status_code == 200


def test_guest_cannot_view_user_management(client):
    login_as(client, role="Guest")

    response = client.get("/users")

    assert response.status_code == 302
    assert "/home" in response.headers["Location"]


def test_guest_cannot_create_room(client):
    login_as(client, role="Guest")

    response = client.post(
        "/create_room",
        data={
            "name": "Test Room",
            "numPeople": "0",
            "art": "Test artwork",
        },
    )

    assert response.status_code == 302
    assert "/home" in response.headers["Location"]


def test_employee_can_view_event_history(client):
    login_as(client, role="Employee")

    response = client.get("/event_history")

    # This route currently allows any logged-in role.
    # Change the expected result if you restrict this route.
    assert response.status_code == 200
