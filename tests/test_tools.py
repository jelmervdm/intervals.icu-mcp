"""Unit tests for domain tools."""

import pytest
from unittest.mock import patch, MagicMock
from intervals_mcp.tools import athlete, activities, events, wellness, workouts
from mcp.server.fastmcp import FastMCP


@pytest.fixture
def mcp_server():
    server = FastMCP("test_intervals")
    athlete.register(server)
    activities.register(server)
    events.register(server)
    wellness.register(server)
    workouts.register(server)
    return server


def test_tool_registration(mcp_server):
    tool_names = list(mcp_server._tool_manager._tools.keys())  # type: ignore[attr-defined]
    assert "get_athlete_profile" in tool_names
    assert "list_activities" in tool_names
    assert "get_activity" in tool_names
    assert "update_activity" in tool_names
    assert "delete_activity" in tool_names
    assert "list_activity_messages" in tool_names
    assert "add_activity_message" in tool_names
    assert "list_events" in tool_names
    assert "get_event" in tool_names
    assert "create_event" in tool_names
    assert "update_event" in tool_names
    assert "delete_event" in tool_names
    assert "list_wellness" in tool_names
    assert "get_wellness" in tool_names
    assert "update_wellness" in tool_names
    assert "list_workout_folders" in tool_names
    assert "list_workouts" in tool_names


@patch("intervals_mcp.tools.athlete.IntervalsClient")
def test_get_athlete_profile_tool(mock_client_cls, mcp_server):
    mock_instance = MagicMock()
    mock_instance.get_athlete.return_value = {"id": "0", "name": "Athlete"}
    mock_client_cls.return_value = mock_instance

    tool = mcp_server._tool_manager._tools["get_athlete_profile"]  # type: ignore[attr-defined]
    result = tool.fn(athlete_id="0")
    assert result["name"] == "Athlete"
    mock_instance.get_athlete.assert_called_once_with(athlete_id="0")


@patch("intervals_mcp.tools.wellness.IntervalsClient")
def test_update_wellness_tool(mock_client_cls, mcp_server):
    mock_instance = MagicMock()
    mock_instance.update_wellness.return_value = {"id": "2026-07-26", "weight": 70.5}
    mock_client_cls.return_value = mock_instance

    tool = mcp_server._tool_manager._tools["update_wellness"]  # type: ignore[attr-defined]
    result = tool.fn(date="2026-07-26", weight=70.5)
    assert result["weight"] == 70.5
    mock_instance.update_wellness.assert_called_once_with(
        date="2026-07-26",
        wellness_data={"weight": 70.5},
        athlete_id="0",
    )
