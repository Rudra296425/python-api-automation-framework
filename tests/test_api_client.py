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

    def get(self, url, timeout):
        self.calls.append((url, timeout))
        return self.response


def test_get_user_returns_json_and_uses_configured_timeout():
    session = FakeSession(FakeResponse({"id": 7, "name": "Ada"}))
    client = APIClient("https://api.example.test/", session=session, timeout=3)

    assert client.get_user(7) == {"id": 7, "name": "Ada"}
    assert session.calls == [("https://api.example.test/users/7", 3)]


def test_get_user_propagates_http_errors():
    session = FakeSession(FakeResponse({}, requests.HTTPError("404 client error")))
    client = APIClient("https://api.example.test", session=session)

    with pytest.raises(requests.HTTPError, match="404"):
        client.get_user(404)
