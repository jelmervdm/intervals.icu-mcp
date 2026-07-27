"""Workout library domain tools for Intervals.icu MCP server."""

from typing import Annotated, Any, Dict, List, Optional
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register workout library tools with FastMCP."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def list_workout_folders(
        athlete_id: Annotated[
            str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")
        ] = "0"
    ) -> List[Dict[str, Any]]:
        """List workout folders in the athlete library.

        Use when browsing workout library structure. To list workouts within a folder, use list_workouts.

        Args:
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.list_folders(athlete_id=athlete_id)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def list_workouts(
        folder_id: Annotated[
            Optional[int], Field(description="Optional workout folder ID to filter by.")
        ] = None,
        athlete_id: Annotated[
            str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")
        ] = "0",
    ) -> List[Dict[str, Any]]:
        """List structured library workouts.

        Use when browsing reusable workout templates. To schedule a workout onto the calendar, use create_event.

        Args:
            folder_id: Optional workout folder ID to filter by.
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.list_workouts(folder_id=folder_id, athlete_id=athlete_id)

