"""Workout library domain tools for Intervals.icu MCP server."""

from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register workout library tools with FastMCP."""

    @mcp.tool()
    def list_workout_folders(athlete_id: str = "0") -> List[Dict[str, Any]]:
        """List workout folders in the athlete library.

        Args:
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.list_folders(athlete_id=athlete_id)

    @mcp.tool()
    def list_workouts(
        folder_id: Optional[int] = None, athlete_id: str = "0"
    ) -> List[Dict[str, Any]]:
        """List structured library workouts.

        Args:
            folder_id: Optional workout folder ID to filter by.
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.list_workouts(folder_id=folder_id, athlete_id=athlete_id)
