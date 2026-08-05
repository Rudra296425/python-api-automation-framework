"""Small, testable HTTP client for JSON APIs."""

from __future__ import annotations

from typing import Any

import requests
from config import APISettings
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APIClient:
    """Wrap a requests session and expose intention-revealing API methods."""

    def __init__(
        self,
        base_url: str | None = None,
        session: requests.Session | None = None,
        timeout: int | None = None,
    ) -> None:
        settings = APISettings.from_environment()
        self.base_url = (base_url or settings.base_url).rstrip("/")
        self.session = session or requests.Session()
        self.timeout = timeout or settings.timeout
        if settings.token:
            self.session.headers.update({"Authorization": f"Bearer {settings.token}"})
        if session is None:
            retry = Retry(
                total=3, backoff_factor=0.2, status_forcelist=[429, 500, 502, 503]
            )
            self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        response = self.session.request(
            method, f"{self.base_url}{path}", timeout=self.timeout, **kwargs
        )
        response.raise_for_status()
        return response

    def list_users(self) -> list[dict[str, Any]]:
        return self._request("GET", "/users").json()

    def get_user(self, user_id: int) -> dict[str, Any]:
        """Fetch one user and raise for a non-success HTTP response."""
        return self._request("GET", f"/users/{user_id}").json()

    def create_post(self, title: str, body: str, user_id: int) -> dict[str, Any]:
        payload = {"title": title, "body": body, "userId": user_id}
        return self._request("POST", "/posts", json=payload).json()

    def update_post(self, post_id: int, **changes: Any) -> dict[str, Any]:
        return self._request("PATCH", f"/posts/{post_id}", json=changes).json()

    def delete_post(self, post_id: int) -> None:
        self._request("DELETE", f"/posts/{post_id}")
