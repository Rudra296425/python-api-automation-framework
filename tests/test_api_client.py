"""Tests for the API client without a network dependency."""

import sys
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from api_client import APIClient  # noqa: E402


class FakeResponse:
    def __init__(self, payload, error=None):
        self.payload = payload
        self.error = error

    def raise_for_status(self):
        if self.error:
            raise self.error

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def request(self, method, url, timeout, **kwargs):
        self.calls.append((method, url, timeout, kwargs))
        return self.response


def test_get_user_returns_json_and_uses_configured_timeout():
    session = FakeSession(FakeResponse({"id": 7, "name": "Ada"}))
    client = APIClient("https://api.example.test/", session=session, timeout=3)

    assert client.get_user(7) == {"id": 7, "name": "Ada"}
    assert session.calls == [("GET", "https://api.example.test/users/7", 3, {})]


def test_get_user_propagates_http_errors():
    session = FakeSession(FakeResponse({}, requests.HTTPError("404 client error")))
    client = APIClient("https://api.example.test", session=session)

    with pytest.raises(requests.HTTPError, match="404"):
        client.get_user(404)


def test_post_lifecycle_uses_expected_http_methods_and_payloads():
    session = FakeSession(FakeResponse({"id": 11, "title": "new"}))
    client = APIClient("https://api.example.test", session=session)

    assert client.create_post("new", "body", 1)["id"] == 11
    assert session.calls[0] == (
        "POST", "https://api.example.test/posts", 10,
        {"json": {"title": "new", "body": "body", "userId": 1}},
    )
