"""Wellness domain tools for Intervals.icu MCP server."""

from typing import Annotated, Any, Dict, List, Optional
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register wellness management tools with FastMCP."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def list_wellness(
        oldest: Annotated[str, Field(description="Start date in YYYY-MM-DD format (e.g. '2026-07-01').")],
        newest: Annotated[str, Field(description="End date in YYYY-MM-DD format (e.g. '2026-07-26').")],
        athlete_id: Annotated[str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")] = "0",
    ) -> List[Dict[str, Any]]:
        """List daily wellness records in a date range.

        Use when tracking trends in sleep, HRV, weight, and readiness over time.
        To inspect a single day's wellness record, use get_wellness.

        Args:
            oldest: Start date (YYYY-MM-DD).
            newest: End date (YYYY-MM-DD).
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.list_wellness(oldest=oldest, newest=newest, athlete_id=athlete_id)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def get_wellness(
        date: Annotated[str, Field(description="Date string in YYYY-MM-DD format.")],
        athlete_id: Annotated[str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")] = "0",
    ) -> Dict[str, Any]:
        """Fetch wellness record for a specific date.

        Use when examining a single day's physiological metrics.
        To list metrics across multiple days, use list_wellness.

        Args:
            date: Date string in YYYY-MM-DD format.
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.get_wellness(date=date, athlete_id=athlete_id)

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=False, idempotentHint=True))
    def update_wellness(
        date: Annotated[str, Field(description="Target date in YYYY-MM-DD format.")],
        weight: Annotated[Optional[float], Field(description="Body weight in kilograms.")] = None,
        resting_hr: Annotated[Optional[int], Field(description="Resting heart rate in beats per minute.")] = None,
        hrv: Annotated[Optional[float], Field(description="Heart rate variability (rmssd).")] = None,
        sleep_secs: Annotated[Optional[int], Field(description="Total sleep duration in seconds.")] = None,
        readiness: Annotated[Optional[int], Field(description="Subjective readiness score (1-10 or 1-100).")] = None,
        fatigue: Annotated[Optional[int], Field(description="Subjective fatigue score (1-7 scale).")] = None,
        mood: Annotated[Optional[int], Field(description="Subjective mood score (1-7 scale).")] = None,
        comments: Annotated[Optional[str], Field(description="Daily notes or subjective comments.")] = None,
        athlete_id: Annotated[str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")] = "0",
    ) -> Dict[str, Any]:
        """Update daily wellness metrics for a given date.

        Use to log or update daily sleep, weight, HRV, and subjective readiness. Updates only specified fields.

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
