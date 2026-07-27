"""Athlete domain tools for Intervals.icu MCP server."""

from typing import Annotated, Any, Dict
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register athlete tools with FastMCP."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def get_athlete_profile(
        athlete_id: Annotated[str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")] = "0",
    ) -> Dict[str, Any]:
        """Fetch athlete profile details, including FTP, LTHR, weight, max HR, and training zones.

        Use to inspect baseline athletic physiological metrics and training zone configurations.

        Args:
            athlete_id: Athlete ID (defaults to "0" for the authenticated athlete).
        """
        client = IntervalsClient()
        return client.get_athlete(athlete_id=athlete_id)
