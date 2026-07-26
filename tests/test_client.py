"""Unit tests for IntervalsClient API wrapper."""

import pytest
from unittest.mock import MagicMock, patch
import httpx
from intervals_mcp.client import IntervalsClient, IntervalsAPIError


def test_client_init_defaults(monkeypatch):
    monkeypatch.setenv("INTERVALS_API_KEY", "key123")
    monkeypatch.setenv("INTERVALS_ATHLETE_ID", "i9999")
    client = IntervalsClient()
    assert client.api_key == "key123"
    assert client.default_athlete_id == "i9999"
    assert client.base_url == "https://intervals.icu/api/v1"


def test_client_init_missing_api_key(monkeypatch):
    monkeypatch.delenv("INTERVALS_API_KEY", raising=False)
    client = IntervalsClient(api_key=None)
    with pytest.raises(ValueError, match="INTERVALS_API_KEY is not set"):
        client.get_athlete()


@patch("intervals_mcp.client.httpx.Client")
def test_client_get_athlete(mock_httpx_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "i123", "name": "Test Athlete", "icu_ftp": 300}

    mock_client_ctx = MagicMock()
    mock_client_ctx.get.return_value = mock_response
    mock_httpx_client.return_value.__enter__.return_value = mock_client_ctx

    client = IntervalsClient(api_key="testkey")
    athlete = client.get_athlete()
    assert athlete["id"] == "i123"
    assert athlete["icu_ftp"] == 300
    mock_client_ctx.get.assert_called_once_with("/athlete/0")


@patch("intervals_mcp.client.httpx.Client")
def test_client_list_activities(mock_httpx_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": "a1", "name": "Morning Ride"},
        {"id": "a2", "name": "Tempo Run"},
    ]

    mock_client_ctx = MagicMock()
    mock_client_ctx.get.return_value = mock_response
    mock_httpx_client.return_value.__enter__.return_value = mock_client_ctx

    client = IntervalsClient(api_key="testkey")
    activities = client.list_activities(oldest="2026-07-01", newest="2026-07-26")
    assert len(activities) == 2
    assert activities[0]["name"] == "Morning Ride"
    mock_client_ctx.get.assert_called_once_with(
        "/athlete/0/activities", params={"oldest": "2026-07-01", "newest": "2026-07-26"}
    )


@patch("intervals_mcp.client.httpx.Client")
def test_client_error_handling(mock_httpx_client):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Activity not found"}
    mock_response.text = "Activity not found"

    mock_client_ctx = MagicMock()
    mock_client_ctx.get.return_value = mock_response
    mock_httpx_client.return_value.__enter__.return_value = mock_client_ctx

    client = IntervalsClient(api_key="testkey")
    with pytest.raises(IntervalsAPIError) as exc_info:
        client.get_activity("invalid")

    assert exc_info.value.status_code == 404
    assert "Activity not found" in exc_info.value.message
