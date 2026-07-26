"""Pytest fixtures for Intervals.icu MCP test suite."""

import pytest


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Set default dummy environment variables for tests."""
    monkeypatch.setenv("INTERVALS_API_KEY", "dummy_test_api_key")
    monkeypatch.setenv("INTERVALS_ATHLETE_ID", "0")
    monkeypatch.setenv("INTERVALS_BASE_URL", "https://intervals.icu/api/v1")
