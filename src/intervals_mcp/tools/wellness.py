"""Wellness domain tools for Intervals.icu MCP server."""

from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register wellness management tools with FastMCP."""

    @mcp.tool()
    def list_wellness(
        oldest: str,
        newest: str,
        athlete_id: str = "0",
    ) -> List[Dict[str, Any]]:
        """List daily wellness records in a date range.

        Args:
            oldest: Start date (YYYY-MM-DD).
            newest: End date (YYYY-MM-DD).
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.list_wellness(oldest=oldest, newest=newest, athlete_id=athlete_id)

    @mcp.tool()
    def get_wellness(date: str, athlete_id: str = "0") -> Dict[str, Any]:
        """Fetch wellness record for a specific date.

        Args:
            date: Date string in YYYY-MM-DD format.
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.get_wellness(date=date, athlete_id=athlete_id)

    @mcp.tool()
    def update_wellness(
        date: str,
        weight: Optional[float] = None,
        resting_hr: Optional[int] = None,
        hrv: Optional[float] = None,
        sleep_secs: Optional[int] = None,
        readiness: Optional[int] = None,
        fatigue: Optional[int] = None,
        mood: Optional[int] = None,
        comments: Optional[str] = None,
        athlete_id: str = "0",
    ) -> Dict[str, Any]:
        """Update wellness metrics for a given date.

        Args:
            date: Date in YYYY-MM-DD format.
            weight: Body weight in kg.
            resting_hr: Resting heart rate in bpm.
            hrv: Heart rate variability.
            sleep_secs: Total sleep duration in seconds.
            readiness: Readiness score.
            fatigue: Subjective fatigue score.
            mood: Subjective mood score.
            comments: Optional daily notes/comments.
            athlete_id: Athlete ID (defaults to "0").
        """
        wellness_data: Dict[str, Any] = {}
        if weight is not None:
            wellness_data["weight"] = weight
        if resting_hr is not None:
            wellness_data["restingHR"] = resting_hr
        if hrv is not None:
            wellness_data["hrv"] = hrv
        if sleep_secs is not None:
            wellness_data["sleepSecs"] = sleep_secs
        if readiness is not None:
            wellness_data["readiness"] = readiness
        if fatigue is not None:
            wellness_data["fatigue"] = fatigue
        if mood is not None:
            wellness_data["mood"] = mood
        if comments is not None:
            wellness_data["comments"] = comments

        if not wellness_data:
            raise ValueError("No wellness fields provided to update.")

        client = IntervalsClient()
        return client.update_wellness(date=date, wellness_data=wellness_data, athlete_id=athlete_id)
