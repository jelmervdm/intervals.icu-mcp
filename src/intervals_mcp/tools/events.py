"""Events & Calendar domain tools for Intervals.icu MCP server."""

from typing import Annotated, Any, Dict, List, Optional
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register calendar and event management tools with FastMCP."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def list_events(
        oldest: Annotated[str, Field(description="Start date in YYYY-MM-DD format (e.g. '2026-07-01').")],
        newest: Annotated[str, Field(description="End date in YYYY-MM-DD format (e.g. '2026-07-26').")],
        athlete_id: Annotated[
            str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")
        ] = "0",
    ) -> List[Dict[str, Any]]:
        """List calendar events and planned workouts between dates.

        Use when browsing planned workouts, notes, or race events on the calendar. To fetch details of a specific planned event, use get_event.

        Args:
            oldest: Start date (YYYY-MM-DD).
            newest: End date (YYYY-MM-DD).
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.list_events(oldest=oldest, newest=newest, athlete_id=athlete_id)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def get_event(
        event_id: Annotated[int, Field(description="Calendar event ID.")],
        athlete_id: Annotated[
            str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")
        ] = "0",
    ) -> Dict[str, Any]:
        """Fetch details of a single calendar event or planned workout.

        Use when inspecting target workout steps or race plans for a specific calendar item. To list events across a date range, use list_events.

        Args:
            event_id: Calendar event ID.
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.get_event(event_id=event_id, athlete_id=athlete_id)

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=False, idempotentHint=False))
    def create_event(
        start_date_local: Annotated[
            str,
            Field(description="Local start time in YYYY-MM-DDTHH:MM:SS format (e.g. '2026-07-27T08:00:00')."),
        ],
        name: Annotated[str, Field(description="Title of event or planned workout.")],
        description: Annotated[
            Optional[str], Field(description="Workout prescription steps or description text.")
        ] = None,
        type: Annotated[
            Optional[str], Field(description="Activity type (e.g. 'Ride', 'Run', 'Swim').")
        ] = None,
        category: Annotated[
            str, Field(description="Event category: 'WORKOUT', 'RACE', or 'NOTE'.")
        ] = "WORKOUT",
        athlete_id: Annotated[
            str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")
        ] = "0",
    ) -> Dict[str, Any]:
        """Create a new planned workout, race event, or note on the calendar.

        Use when scheduling upcoming training or race events. To modify an existing calendar event, use update_event.

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

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=False, idempotentHint=True))
    def update_event(
        event_id: Annotated[int, Field(description="Calendar event ID to update.")],
        start_date_local: Annotated[
            Optional[str], Field(description="Updated local start time (YYYY-MM-DDTHH:MM:SS).")
        ] = None,
        name: Annotated[Optional[str], Field(description="Updated event title.")] = None,
        description: Annotated[
            Optional[str], Field(description="Updated workout prescription steps or notes.")
        ] = None,
        athlete_id: Annotated[
            str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")
        ] = "0",
    ) -> Dict[str, Any]:
        """Update an existing calendar event or planned workout.

        Use when modifying workout targets, start dates, or titles. To schedule a new event, use create_event.

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
        return client.update_event(event_id=event_id, event_data=event_data, athlete_id=athlete_id)

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=True, idempotentHint=True))
    def delete_event(
        event_id: Annotated[int, Field(description="ID of the event to delete.")],
        athlete_id: Annotated[
            str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")
        ] = "0",
    ) -> Dict[str, Any]:
        """Delete a calendar event or planned workout by ID.

        Use to remove canceled workouts or events from the training calendar.

        Args:
            event_id: ID of the event to delete.
            athlete_id: Athlete ID (defaults to "0").
        """
        client = IntervalsClient()
        return client.delete_event(event_id=event_id, athlete_id=athlete_id)

