"""Athlete domain tools for Intervals.icu MCP server."""

from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register athlete tools with FastMCP."""

    @mcp.tool()
    def get_athlete_profile(athlete_id: str = "0") -> Dict[str, Any]:
        """Fetch athlete profile details, including FTP, LTHR, weight, max HR, and zones.

        Args:
            athlete_id: Athlete ID (defaults to "0" for the authenticated athlete).
        """
        client = IntervalsClient()
        return client.get_athlete(athlete_id=athlete_id)
