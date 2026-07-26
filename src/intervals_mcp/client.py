"""Intervals.icu REST API Client."""

import os
from typing import Any, Dict, List, Optional, Tuple, cast
import httpx

DEFAULT_BASE_URL = "https://intervals.icu/api/v1"


class IntervalsAPIError(Exception):
    """Exception raised when an API call fails."""

    def __init__(self, status_code: int, message: str, details: Any = None):
        super().__init__(f"Intervals.icu API Error ({status_code}): {message}")
        self.status_code = status_code
        self.message = message
        self.details = details


class IntervalsClient:
    """Client for interacting with the Intervals.icu REST API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_athlete_id: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ):
        self.api_key = api_key or os.environ.get("INTERVALS_API_KEY")
        self.default_athlete_id = default_athlete_id or os.environ.get("INTERVALS_ATHLETE_ID") or "0"
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout

    def _get_auth(self) -> Tuple[str, str]:
        if not self.api_key:
            raise ValueError("INTERVALS_API_KEY is not set. Please set the INTERVALS_API_KEY environment variable.")
        # Intervals.icu uses HTTP Basic authentication with username "API_KEY" and the key as password
        return ("API_KEY", self.api_key)

    def _client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            auth=self._get_auth(),
            headers={"Content-Type": "application/json"},
            timeout=self.timeout,
        )

    def _handle_response(self, response: httpx.Response) -> Any:
        if response.status_code >= 400:
            try:
                data = response.json()
                msg = data.get("error", data.get("message", response.text))
            except Exception:
                msg = response.text
                data = None
            raise IntervalsAPIError(response.status_code, msg, details=data)

        if response.status_code == 204 or not response.content:
            return {"success": True}

        return response.json()

    # ---------------------------------------------------------------------------
    # Athlete Endpoints
    # ---------------------------------------------------------------------------

    def get_athlete(self, athlete_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch athlete profile details."""
        ath_id = athlete_id or self.default_athlete_id
        with self._client() as c:
            res = c.get(f"/athlete/{ath_id}")
            return cast(Dict[str, Any], self._handle_response(res))

    # ---------------------------------------------------------------------------
    # Activity Endpoints
    # ---------------------------------------------------------------------------

    def list_activities(
        self,
        oldest: str,
        newest: str,
        athlete_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List activities within a date range (ISO format YYYY-MM-DD)."""
        ath_id = athlete_id or self.default_athlete_id
        params = {"oldest": oldest, "newest": newest}
        with self._client() as c:
            res = c.get(f"/athlete/{ath_id}/activities", params=params)
            return cast(List[Dict[str, Any]], self._handle_response(res))

    def get_activity(self, activity_id: str) -> Dict[str, Any]:
        """Retrieve details of a single activity by ID."""
        with self._client() as c:
            res = c.get(f"/activity/{activity_id}")
            return cast(Dict[str, Any], self._handle_response(res))

    def update_activity(self, activity_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update metadata of an existing activity."""
        with self._client() as c:
            res = c.put(f"/activity/{activity_id}", json=updates)
            return cast(Dict[str, Any], self._handle_response(res))

    def delete_activity(self, activity_id: str) -> Dict[str, Any]:
        """Delete an activity by ID."""
        with self._client() as c:
            res = c.delete(f"/activity/{activity_id}")
            return cast(Dict[str, Any], self._handle_response(res))

    def get_activity_messages(self, activity_id: str) -> List[Dict[str, Any]]:
        """Get comments/messages attached to an activity."""
        with self._client() as c:
            res = c.get(f"/activity/{activity_id}/messages")
            return cast(List[Dict[str, Any]], self._handle_response(res))

    def add_activity_message(self, activity_id: str, text: str) -> Dict[str, Any]:
        """Post a comment/note to an activity."""
        with self._client() as c:
            res = c.post(f"/activity/{activity_id}/messages", json={"content": text})
            return cast(Dict[str, Any], self._handle_response(res))

    # ---------------------------------------------------------------------------
    # Calendar & Event Endpoints
    # ---------------------------------------------------------------------------

    def list_events(self, oldest: str, newest: str, athlete_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List calendar events and planned workouts between dates."""
        ath_id = athlete_id or self.default_athlete_id
        params = {"oldest": oldest, "newest": newest}
        with self._client() as c:
            res = c.get(f"/athlete/{ath_id}/events", params=params)
            return cast(List[Dict[str, Any]], self._handle_response(res))

    def get_event(self, event_id: int, athlete_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch details of a single calendar event."""
        ath_id = athlete_id or self.default_athlete_id
        with self._client() as c:
            res = c.get(f"/athlete/{ath_id}/events/{event_id}")
            return cast(Dict[str, Any], self._handle_response(res))

    def create_event(self, event_data: Dict[str, Any], athlete_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a planned workout or calendar event."""
        ath_id = athlete_id or self.default_athlete_id
        with self._client() as c:
            res = c.post(f"/athlete/{ath_id}/events", json=event_data)
            return cast(Dict[str, Any], self._handle_response(res))

    def update_event(
        self, event_id: int, event_data: Dict[str, Any], athlete_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update an existing calendar event or planned workout."""
        ath_id = athlete_id or self.default_athlete_id
        with self._client() as c:
            res = c.put(f"/athlete/{ath_id}/events/{event_id}", json=event_data)
            return cast(Dict[str, Any], self._handle_response(res))

    def delete_event(self, event_id: int, athlete_id: Optional[str] = None) -> Dict[str, Any]:
        """Delete a calendar event."""
        ath_id = athlete_id or self.default_athlete_id
        with self._client() as c:
            res = c.delete(f"/athlete/{ath_id}/events/{event_id}")
            return cast(Dict[str, Any], self._handle_response(res))

    # ---------------------------------------------------------------------------
    # Wellness Endpoints
    # ---------------------------------------------------------------------------

    def list_wellness(self, oldest: str, newest: str, athlete_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List daily wellness records in a date range."""
        ath_id = athlete_id or self.default_athlete_id
        params = {"oldest": oldest, "newest": newest}
        with self._client() as c:
            res = c.get(f"/athlete/{ath_id}/wellness", params=params)
            return cast(List[Dict[str, Any]], self._handle_response(res))

    def get_wellness(self, date: str, athlete_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch wellness metrics for a single date (YYYY-MM-DD)."""
        ath_id = athlete_id or self.default_athlete_id
        with self._client() as c:
            res = c.get(f"/athlete/{ath_id}/wellness/{date}")
            return cast(Dict[str, Any], self._handle_response(res))

    def update_wellness(
        self, date: str, wellness_data: Dict[str, Any], athlete_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update daily wellness metrics for a specific date."""
        ath_id = athlete_id or self.default_athlete_id
        with self._client() as c:
            res = c.put(f"/athlete/{ath_id}/wellness/{date}", json=wellness_data)
            return cast(Dict[str, Any], self._handle_response(res))

    # ---------------------------------------------------------------------------
    # Workout Library Endpoints
    # ---------------------------------------------------------------------------

    def list_folders(self, athlete_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List workout folders in athlete library."""
        ath_id = athlete_id or self.default_athlete_id
        with self._client() as c:
            res = c.get(f"/athlete/{ath_id}/folders")
            return cast(List[Dict[str, Any]], self._handle_response(res))

    def list_workouts(self, folder_id: Optional[int] = None, athlete_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List workouts from library."""
        ath_id = athlete_id or self.default_athlete_id
        params = {}
        if folder_id is not None:
            params["folder_id"] = folder_id
        with self._client() as c:
            res = c.get(f"/athlete/{ath_id}/workouts", params=params)
            return cast(List[Dict[str, Any]], self._handle_response(res))
