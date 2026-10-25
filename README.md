# Lab 6: REST API Testing

**Duration:** 2 hours  **Work mode:** groups

This lab has two parts. Part 1 establishes the method, against an
application whose contract is given to you. Part 2 applies the same
method to an application whose contract you must establish yourself.

---

# Part 1: Testing a given contract

**Application under test:** `https://pytodo-lab6.onrender.com` (the PyTodo JSON API)

## 1. What you are building

Automated tests that call the API directly with HTTP requests. No
browser, no clicking. Just the `requests` library and `pytest`.

## 2. Setup

```bash
pip install -r requirements.txt
```

Set the app address once per terminal session:

```bash
export PYTODO_URL="https://pytodo-lab6.onrender.com"
```

On Windows PowerShell: `$env:PYTODO_URL="https://pytodo-lab6.onrender.com"`.

This URL is only ever used by your test code, never opened in a browser.

Confirm the app is reachable:

```bash
curl https://pytodo-lab6.onrender.com/health
```

This should print `ok`. If it does not, stop here and check the URL
before continuing.

## 3. Logging in

Demo account for this lab: username `demo`, password `demo1234`.

The API checks this once, then remembers you are logged in through a
session cookie. In `requests`, a `requests.Session()` object keeps
that cookie for you automatically between calls, the same way a
browser does between page loads.

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

Commit `test_api.py` to your repo before moving to Part 2.

| Criterion | Points |
|---|---|
| GET tests understood and run cleanly (already given, but explain them if asked) | 5 |
| POST valid test checks status, headers, and payload | 10 |
| POST invalid test checks for 400 and a non-empty errors list | 10 |
| DELETE existing and DELETE missing, correct status codes | 10 |
| Full create-read-delete flow test | 15 |

---

# Part 2: Establishing a contract from a live API

Part 1 tested an application whose rules were stated for you in
advance. Part 2 reverses this. The rules are not given. You determine
them by reading the API's own documentation and by sending requests to
it, then you record what you found before writing a single test
against it.

This is the ordinary condition of API testing outside a classroom. A
specification is not always available, or does not match what the
server actually does. The tester's first task is always to establish
ground truth from the running system itself.

## 9. The application under test

**JSONPlaceholder**, a public REST API built for exactly this purpose:
`https://jsonplaceholder.typicode.com`

Its guide is published at `https://jsonplaceholder.typicode.com/guide`.
You are permitted, and expected, to read it before sending requests.
Reading documentation is not a shortcut around testing. It is the
first step of testing: forming an expectation before checking whether
the system meets it.

Every request in Part 2 is directed at this address only. Do not
direct any request, of any kind, at a website that is not named in
this document.

## 10. Establish the contract

Before writing any test, complete `API_FINDINGS.md` in this repository.
It asks you to record, for each of four routes:

- the exact method and path
- the status code the server actually returned
- the `Content-Type` header the server actually returned
- the keys present in the response body, and the type of each value

Determine these by sending real requests with `requests` in a plain
Python shell, or with `curl`, and reading the real response. Do not
record a value because the documentation states it. Record the value
the server returned. Where the two disagree, record what the server
returned, and note the disagreement.

The four routes to establish:

| Method | Route |
|---|---|
| GET | `/posts/1` |
| GET | `/posts` |
| POST | `/posts` |
| DELETE | `/posts/1` |

## 11. Write the tests

Open `test_public_api.py`. Four test functions are declared, each with
a docstring stating which route it covers. Using `API_FINDINGS.md` as
your source of truth, write the body of each test, following the same
pattern established in Part 1: assert the status code, assert the
`Content-Type` header, assert the structure of the payload.

No login is required for this API.

```python
BASE_URL = "https://jsonplaceholder.typicode.com"

response = requests.get(f"{BASE_URL}/posts/1")
assert response.status_code == 200
```

## 12. Run your tests

```bash
pytest test_public_api.py -v
```

Every test should show `PASSED`. A test that fails here most often
means `API_FINDINGS.md` recorded a value that does not match what the
server actually returns. Re-check the finding before changing the
test.

## 13. Submit

Commit `API_FINDINGS.md` and `test_public_api.py` to your repository.

| Criterion | Points |
|---|---|
| `API_FINDINGS.md` complete and accurate for all four routes | 25 |
| `test_get_single_post` correct | 10 |
| `test_get_all_posts` correct | 10 |
| `test_create_post` correct | 10 |
| `test_delete_post` correct | 10 |
