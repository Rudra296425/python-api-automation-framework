# Python API Automation Framework

A compact API testing framework that demonstrates a client abstraction, deterministic unit tests, and a CI-ready layout.

## Structure

```
src/api_client.py       HTTP client with dependency injection
tests/test_api_client.py Unit tests using a fake session
```

## Run locally

```bash
python -m pip install -r requirements.txt
python -m pytest
python -m ruff check src tests
```

## Container

```bash
docker build -t python-api-automation .
docker run --rm python-api-automation
```

The tests do not call a live service; the injected session makes them fast and repeatable. A production extension would load a base URL and credentials from environment variables and add contract tests against a controlled test environment.
