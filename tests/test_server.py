"""Unit tests for server setup."""

from intervals_mcp.server import mcp, _is_routed_mode


def test_server_tools_registered():
    tools = list(mcp._tool_manager._tools.keys())  # type: ignore[attr-defined]
    assert len(tools) >= 15
    assert "get_athlete_profile" in tools
    assert "list_activities" in tools
    assert "list_events" in tools
    assert "list_wellness" in tools
    assert "list_workouts" in tools


def test_routed_mode_flag(monkeypatch):
    monkeypatch.setenv("TOOL_ROUTING", "true")
    assert _is_routed_mode() is True

    monkeypatch.setenv("TOOL_ROUTING", "false")
    assert _is_routed_mode() is False
