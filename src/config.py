"""Runtime configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class APISettings:
    base_url: str
    token: str | None = None
    timeout: int = 10

    @classmethod
    def from_environment(cls) -> "APISettings":
        return cls(
            base_url=os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com"),
            token=os.getenv("API_TOKEN"),
            timeout=int(os.getenv("API_TIMEOUT", "10")),
        )
