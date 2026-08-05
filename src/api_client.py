"""Small, testable HTTP client for JSON APIs."""

from typing import Any, Optional

import requests


class APIClient:
    """Wrap a requests session and expose intention-revealing API methods."""

    def __init__(
        self,
        base_url: str,
        session: Optional[requests.Session] = None,
        timeout: int = 10,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.timeout = timeout

    def get_user(self, user_id: int) -> dict[str, Any]:
        """Fetch one user and raise for a non-success HTTP response."""
        response = self.session.get(
            f"{self.base_url}/users/{user_id}", timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
