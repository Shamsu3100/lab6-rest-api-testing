# Lab 6: REST API Testing

**Duration:** 2 hours  **Work mode:** groups

**Application under test:** `<APP_URL>` (the PyTodo JSON API)

## 1. What you are building

Automated tests that call the API directly with HTTP requests. No
browser, no clicking. Just the `requests` library and `pytest`.

## 2. Setup

```bash
pip install -r requirements.txt
```

Set the app address once per terminal session:

```bash
export PYTODO_URL="<APP_URL>"
```

On Windows PowerShell: `$env:PYTODO_URL="<APP_URL>"`.

Confirm the app is reachable:

```bash
curl <APP_URL>/health
```

This should print `ok`. If it does not, stop here and check the URL
before continuing.

## 3. Logging in

The API uses the same login as a normal website: a username and
password, checked once, then remembered by a session cookie. In
`requests`, a `requests.Session()` object keeps that cookie for you
automatically between calls, the same way a browser does between page
loads.

```python
import requests

s = requests.Session()
s.post(f"{BASE_URL}/login", data={"username": "demo", "password": "demo1234"})
# s now carries the login cookie. Every call made with s is logged in.
response = s.get(f"{BASE_URL}/api/tasks")
```

A fixture that does this for you, `logged_in_session`, is already
written in `test_api.py`. Use it as an argument to any test that needs
to be logged in.

## 4. The three routes you are testing

| Method | Route | What it does |
|---|---|---|
| GET | `/api/tasks` | returns every task as a JSON list |
| POST | `/api/tasks` | creates one task from a JSON body |
| DELETE | `/api/tasks/<id>` | deletes the task with that id |

Every route needs a login first. Without it, every route replies
`401`.

## 5. What a test checks

For each call, check three things:

1. **The status code.** 200 means it worked. 201 means something new
   was created. 400 means your request was invalid. 404 means the
   thing you asked for does not exist.
2. **The headers.** The response should say
   `Content-Type: application/json`.
3. **The payload.** The actual JSON body: does it have the fields you
   expect, with the values you expect?

```python
response = logged_in_session.get(f"{BASE_URL}/api/tasks")
assert response.status_code == 200
assert response.headers["Content-Type"] == "application/json"
assert isinstance(response.json(), list)
```

## 6. Your task

Open `test_api.py`. The first two tests (`GET /api/tasks`) and the
first `POST` test are already written, as your pattern. Fill in every
section marked `TODO`:

1. `test_create_task_with_invalid_data`: send data that breaks a rule
   (title too short, priority out of range, due_date missing), check
   you get a `400` and an `errors` list back.
2. `test_delete_existing_task`: create a task, delete it by its real
   id, check you get a `200` and the correct confirmation body.
3. `test_delete_missing_task_returns_404`: delete an id that was
   never created, check you get a `404`.
4. `test_create_read_delete_flow`: create a task, confirm it shows up
   in the list, delete it, confirm it no longer shows up.

## 7. Run your tests

```bash
pytest test_api.py -v
```

Every test should show `PASSED`. If one fails, read the assertion
error, it tells you exactly which value did not match what you
expected.

## 8. Submit

Commit `test_api.py` to your repo.

| Criterion | Points |
|---|---|
| GET tests understood and run cleanly (already given, but explain them if asked) | 10 |
| POST valid test checks status, headers, and payload | 15 |
| POST invalid test checks for 400 and a non-empty errors list | 25 |
| DELETE existing and DELETE missing, correct status codes | 25 |
| Full create-read-delete flow test | 25 |
