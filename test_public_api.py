"""Part 2: tests against JSONPlaceholder, a public API.

Complete API_FINDINGS.md before writing any test in this file. Each
assertion below should state what you recorded there, not a value
copied from the documentation.

Run with:
    pytest test_public_api.py -v
"""
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_single_post():
    """GET /posts/1.

    Assert the status code, the Content-Type header, and that the
    response body contains the keys recorded in API_FINDINGS.md, each
    of the correct type.
    """
    pass


def test_get_all_posts():
    """GET /posts.

    Assert the status code, the Content-Type header, and that the
    response body has the shape recorded in API_FINDINGS.md.
    """
    pass


def test_create_post():
    """POST /posts.

    Send the request body recorded in API_FINDINGS.md. Assert the
    status code, the Content-Type header, and that the response body
    contains the fields you sent, plus the field the server adds.
    """
    pass


def test_delete_post():
    """DELETE /posts/1.

    Assert the status code and the Content-Type header recorded in
    API_FINDINGS.md.
    """
    pass
