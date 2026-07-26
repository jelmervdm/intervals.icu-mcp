"""Activities domain tools for Intervals.icu MCP server."""

from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from intervals_mcp.client import IntervalsClient


def register(mcp: FastMCP) -> None:
    """Register activity management tools with FastMCP."""

    @mcp.tool()
    def list_activities(
        oldest: str,
        newest: str,
        athlete_id: str = "0",
    ) -> List[Dict[str, Any]]:
        """List activities within a date range.

        Args:
            oldest: Start date in YYYY-MM-DD format (e.g. "2026-07-01").
            newest: End date in YYYY-MM-DD format (e.g. "2026-07-26").
            athlete_id: Athlete ID (defaults to "0" for authenticated athlete).
        """
        client = IntervalsClient()
        return client.list_activities(oldest=oldest, newest=newest, athlete_id=athlete_id)

    @mcp.tool()
    def get_activity(activity_id: str) -> Dict[str, Any]:
        """Get full details and metrics for a single activity.

        Args:
            activity_id: The unique ID of the activity.
        """
        client = IntervalsClient()
        return client.get_activity(activity_id=activity_id)

    @mcp.tool()
    def update_activity(
        activity_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[str] = None,
        gear: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Update metadata fields on an activity. Only specified fields are updated.

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

    @mcp.tool()
    def delete_activity(activity_id: str) -> Dict[str, Any]:
        """Delete an activity by ID.

        Args:
            activity_id: Unique activity ID to delete.
        """
        client = IntervalsClient()
        return client.delete_activity(activity_id=activity_id)

    @mcp.tool()
    def list_activity_messages(activity_id: str) -> List[Dict[str, Any]]:
        """Retrieve comments and messages associated with an activity.

        Args:
            activity_id: Activity ID.
        """
        client = IntervalsClient()
        return client.get_activity_messages(activity_id=activity_id)

    @mcp.tool()
    def add_activity_message(activity_id: str, text: str) -> Dict[str, Any]:
        """Post a comment/note to an activity.

        Args:
            activity_id: Activity ID.
            text: Comment or message text to attach.
        """
        client = IntervalsClient()
        return client.add_activity_message(activity_id=activity_id, text=text)
