"""Events & Calendar domain tools for Intervals.icu MCP server."""

from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register calendar and event management tools with FastMCP."""

    @mcp.tool()
    def list_events(
        oldest: str,
        newest: str,
        athlete_id: str = "0",
    ) -> List[Dict[str, Any]]:
        """List calendar events and planned workouts between dates.

        Args:
            oldest: Start date (YYYY-MM-DD).
            newest: End date (YYYY-MM-DD).
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.list_events(oldest=oldest, newest=newest, athlete_id=athlete_id)

    @mcp.tool()
    def get_event(event_id: int, athlete_id: str = "0") -> Dict[str, Any]:
        """Fetch details of a single calendar event or planned workout.

        Args:
            event_id: Calendar event ID.
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.get_event(event_id=event_id, athlete_id=athlete_id)

    @mcp.tool()
    def create_event(
        start_date_local: str,
        name: str,
        description: Optional[str] = None,
        type: Optional[str] = None,
        category: str = "WORKOUT",
        athlete_id: str = "0",
    ) -> Dict[str, Any]:
        """Create a new planned workout or calendar event.

        Args:
            start_date_local: Local start time in YYYY-MM-DDTHH:MM:SS format (e.g. "2026-07-27T08:00:00").
            name: Title of event/workout.
            description: Workout steps or description text.
            type: Activity type (e.g. "Ride", "Run", "Swim").
            category: Event category (e.g. "WORKOUT", "RACE", "NOTE").
            athlete_id: Athlete ID (defaults to "0").
        """
        event_data: Dict[str, Any] = {
            "start_date_local": start_date_local,
            "name": name,
            "category": category,
        }
        if description is not None:
            event_data["description"] = description
        if type is not None:
            event_data["type"] = type

        client = IntervalsClient()
        return client.create_event(event_data=event_data, athlete_id=athlete_id)

    @mcp.tool()
    def update_event(
        event_id: int,
        start_date_local: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        athlete_id: str = "0",
    ) -> Dict[str, Any]:
        """Update an existing calendar event or planned workout.

        Args:
            event_id: Calendar event ID to update.
            start_date_local: Updated local start time (YYYY-MM-DDTHH:MM:SS).
            name: Updated name.
            description: Updated workout description or details.
            athlete_id: Athlete ID (defaults to "0").
        """
        event_data: Dict[str, Any] = {}
        if start_date_local is not None:
            event_data["start_date_local"] = start_date_local
        if name is not None:
            event_data["name"] = name
        if description is not None:
            event_data["description"] = description

        if not event_data:
            raise ValueError("No fields provided to update.")

        client = IntervalsClient()
        return client.update_event(
            event_id=event_id, event_data=event_data, athlete_id=athlete_id
        )

    @mcp.tool()
    def delete_event(event_id: int, athlete_id: str = "0") -> Dict[str, Any]:
        """Delete a calendar event by ID.

        Args:
            event_id: ID of the event to delete.
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.delete_event(event_id=event_id, athlete_id=athlete_id)
