"""Lab 6: test the PyTodo JSON API directly, with no browser.

Demo login:
    username: demo
    password: demo1234

The API uses the same login as a normal browser session. requests.Session()
keeps the login cookie between calls, the same way a browser keeps it
between page loads. Log in once per test with the logged_in_session
fixture below, already written for you.

Run with:
    pytest test_api.py -v

GET /api/tasks and the first POST test are finished, as your pattern.
Fill in the sections marked TODO.
"""
import os

import pytest
import requests

BASE_URL = os.environ.get("PYTODO_URL", "http://127.0.0.1:5000")


@pytest.fixture
def logged_in_session():
    """Returns a requests.Session already logged in as the demo user."""
    s = requests.Session()
    response = s.post(
        f"{BASE_URL}/login",
        data={"username": "demo", "password": "demo1234"},
    )
    assert response.status_code == 200
    return s


# ============================================================
# GET /api/tasks — finished, your pattern
# ============================================================

def test_get_tasks_requires_login():
    # A plain requests call, no session, no login.
    response = requests.get(f"{BASE_URL}/api/tasks")
    assert response.status_code == 401


def test_get_tasks_returns_json_list(logged_in_session):
    response = logged_in_session.get(f"{BASE_URL}/api/tasks")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert isinstance(response.json(), list)


# ============================================================
# POST /api/tasks — one example finished, one for you to write
# ============================================================

def test_create_task_with_valid_data(logged_in_session):
    payload = {"title": "Write report", "priority": 3, "due_date": "2026-12-01"}
    response = logged_in_session.post(f"{BASE_URL}/api/tasks", json=payload)

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"

    body = response.json()
    assert body["title"] == "Write report"
    assert body["priority"] == 3
    assert body["due_date"] == "2026-12-01"
    assert body["completed"] is False
    assert "id" in body


def test_create_task_with_invalid_data(logged_in_session):
    # TODO: send a payload that breaks the rules, for example
    # priority=9 (must be 1 to 5), or title="ab" (too short).
    # TODO: assert the status code is 400.
    # TODO: assert response.json() has an "errors" key, and that it
    # is a non-empty list.
    pass


# ============================================================
# DELETE /api/tasks/<id> — write both of these
# ============================================================

def test_delete_existing_task(logged_in_session):
    # TODO: create a task first, so you have a real id to delete.
    # TODO: call logged_in_session.delete(f"{BASE_URL}/api/tasks/{the_id}")
    # TODO: assert status code 200
    # TODO: assert the response JSON says {"status": "deleted", "id": the_id}
    pass


def test_delete_missing_task_returns_404(logged_in_session):
    # TODO: call DELETE on an id that does not exist, for example 999999.
    # TODO: assert status code 404.
    pass


# ============================================================
# Full flow — create, read it back, delete, confirm it is gone
# ============================================================

def test_create_read_delete_flow(logged_in_session):
    # TODO: create a task, keep its id from the response body.
    # TODO: GET /api/tasks and assert a task with that id is in the list.
    # TODO: DELETE that id.
    # TODO: GET /api/tasks again and assert no task with that id remains.
    pass
