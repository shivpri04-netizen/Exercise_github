import copy
import pytest

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    try:
        yield
    finally:
        activities.clear()
        activities.update(original)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant():
    email = "testuser@example.com"
    resp = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_rejected():
    email = "dup@example.com"
    resp1 = client.post(f"/activities/Programming%20Class/signup?email={email}")
    assert resp1.status_code == 200
    resp2 = client.post(f"/activities/Programming%20Class/signup?email={email}")
    assert resp2.status_code == 400


def test_remove_participant():
    email = "john@mergington.edu"
    resp = client.delete(f"/activities/Gym%20Class/participants?email={email}")
    assert resp.status_code == 200
    assert email not in activities["Gym Class"]["participants"]
