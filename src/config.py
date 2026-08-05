"""Runtime configuration loaded from environment variables."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class APISettings:
    base_url: str
    token: Optional[str] = None
    timeout: int = 10

    @classmethod
    def from_environment(cls) -> "APISettings":
        return cls(
            base_url=os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com"),
            token=os.getenv("API_TOKEN"),
            timeout=int(os.getenv("API_TIMEOUT", "10")),
        )
