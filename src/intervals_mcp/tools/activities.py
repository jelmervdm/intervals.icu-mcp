"""Activities domain tools for Intervals.icu MCP server."""

from typing import Annotated, Any, Dict, List, Optional
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register activity management tools with FastMCP."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def list_activities(
        oldest: Annotated[str, Field(description="Start date in YYYY-MM-DD format (e.g. '2026-07-01').")],
        newest: Annotated[str, Field(description="End date in YYYY-MM-DD format (e.g. '2026-07-26').")],
        athlete_id: Annotated[str, Field(description="Athlete ID (defaults to '0' for authenticated athlete).")] = "0",
    ) -> List[Dict[str, Any]]:
        """List completed workout activities within a date range.

        Use when retrieving activity summaries across a date range. To fetch detailed power/HR
        streams or intervals for a single activity, use get_activity.

        Args:
            oldest: Start date in YYYY-MM-DD format (e.g. "2026-07-01").
            newest: End date in YYYY-MM-DD format (e.g. "2026-07-26").
            athlete_id: Athlete ID (defaults to "0" for authenticated athlete).
        """
        client = IntervalsClient()
        return client.list_activities(oldest=oldest, newest=newest, athlete_id=athlete_id)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def get_activity(
        activity_id: Annotated[str, Field(description="The unique ID of the activity.")],
    ) -> Dict[str, Any]:
        """Get full details and detailed metrics for a single activity.

        Use when analyzing specific workout metrics (e.g. Normalized Power, TSS, HR zones).
        To list multiple activities across dates, use list_activities.

        Args:
            activity_id: The unique ID of the activity.
        """
        client = IntervalsClient()
        return client.get_activity(activity_id=activity_id)

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=False, idempotentHint=True))
    def update_activity(
        activity_id: Annotated[str, Field(description="ID of the activity to update.")],
        name: Annotated[Optional[str], Field(description="New title for the activity.")] = None,
        description: Annotated[Optional[str], Field(description="Updated description or coach notes.")] = None,
        type: Annotated[
            Optional[str],
            Field(description="Activity type (e.g., 'Ride', 'Run', 'Swim', 'WeightTraining')."),
        ] = None,
        gear: Annotated[Optional[List[str]], Field(description="List of gear names or IDs used.")] = None,
    ) -> Dict[str, Any]:
        """Update metadata fields on an activity. Only specified fields are updated.

        Use when editing activity titles, descriptions, types, or gear assignment.
        To post a comment message, use add_activity_message instead.

        Args:
            activity_id: ID of the activity to update.
            name: New name for the activity.
            description: Updated description or notes.
            type: Activity type (e.g., "Ride", "Run", "Swim", "WeightTraining").
            gear: List of gear names or IDs used.
        """
        updates: Dict[str, Any] = {}
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        if type is not None:
            updates["type"] = type
        if gear is not None:
            updates["gear"] = gear

        if not updates:
            raise ValueError("No update fields provided.")

        client = IntervalsClient()
        return client.update_activity(activity_id=activity_id, updates=updates)

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=True, idempotentHint=True))
    def delete_activity(
        activity_id: Annotated[str, Field(description="Unique activity ID to delete.")],
    ) -> Dict[str, Any]:
        """Delete an activity by ID from Intervals.icu calendar.

        Use to permanently remove duplicate or invalid uploaded activity files.

        Args:
            activity_id: Unique activity ID to delete.
        """
        client = IntervalsClient()
        return client.delete_activity(activity_id=activity_id)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def list_activity_messages(activity_id: Annotated[str, Field(description="Activity ID.")]) -> List[Dict[str, Any]]:
        """Retrieve comments and coach messages associated with an activity.

        Use to view discussion thread on an activity. To post a new message, use add_activity_message.

        Args:
            activity_id: Activity ID.
        """
        client = IntervalsClient()
        return client.get_activity_messages(activity_id=activity_id)

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=False, idempotentHint=False))
    def add_activity_message(
        activity_id: Annotated[str, Field(description="Activity ID.")],
        text: Annotated[str, Field(description="Comment or message text to attach.")],
    ) -> Dict[str, Any]:
        """Post a comment/note to an activity conversation thread.

        Use to add athlete/coach feedback to a workout.
        To edit activity description directly, use update_activity instead.

        Args:
            activity_id: Activity ID.
            text: Comment or message text to attach.
        """
        client = IntervalsClient()
        return client.add_activity_message(activity_id=activity_id, text=text)
