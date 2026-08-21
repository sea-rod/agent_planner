# tools.py
from .calendar_helper import get_user_calendar
from datetime import datetime, timedelta
import pytz


def create_calendar_tools(state):
    """Factory function that creates tools bound to a specific user's calendar"""
    user_id = state.user_id

    if not user_id:
        raise ValueError("user_id not found in state")

    google_cal = get_user_calendar(user_id)

    def get_events(max_period: str = "10d") -> list:
        """
        Returns calendar events within a given period starting from today.

        Parameters:
            max_period (str): Defines the maximum date range to fetch events.
                Supported formats:
                    - "{N}d" → N days from today (e.g., "30d")
                    - "{N}m" → N months from today (e.g., "6m")
                    - "YYYY-MM-DD" → specific end date (e.g., "2022-11-14")
                Default is "10d" (10 days).

        Example:
            get_events()                # events for next 10 days
            get_events("30d")           # events for next 30 days
            get_events("6m")            # events for next 6 months
            get_events("2022-12-31")    # events until specific date
        """
        result = google_cal.get_events(max_period)
        print(f"Tool get_events returned: {result}")
        return result

    def create_event(
        summary: str,
        description: str,
        strt_dateTime: str,
        end_dateTime: str,
    ) -> dict:
        """
        Creates a SINGLE event on Google Calendar.
        Use this only when creating exactly one event.
        Parameters:
            summary: Event title
            description: Event description
            strt_dateTime: Start in naive local format e.g. "2026-06-03T19:00:00"
            end_dateTime: End in naive local format e.g. "2026-06-03T21:00:00"
        """
        timezone = google_cal.get_user_timezone()
        tz = pytz.timezone(timezone)

        start_dt = tz.localize(datetime.strptime(strt_dateTime, "%Y-%m-%dT%H:%M:%S"))
        end_dt = tz.localize(datetime.strptime(end_dateTime, "%Y-%m-%dT%H:%M:%S"))

        event_payload = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_dt.isoformat()},
            "end": {"dateTime": end_dt.isoformat()},
        }

        result = google_cal.create_event(event_payload)
        print(f"Tool create_event returned: {result}")
        return result

    def create_recurring_events(
        summary: str,
        description: str,
        start_time: str,
        end_time: str,
        start_date: str,
        end_date: str,
        frequency: str = "daily",
        interval: int = 1,
    ) -> dict:

        timezone = google_cal.get_user_timezone()

        if frequency not in ("daily", "weekly"):
            raise ValueError(f"Unsupported frequency: {frequency}")

        if interval < 1:
            raise ValueError("interval must be >= 1")

        tz = pytz.timezone(timezone)

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

        if end_date_obj < start_date_obj:
            raise ValueError("end_date must be >= start_date")

        start_dt = tz.localize(
            datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        )

        end_dt = tz.localize(
            datetime.strptime(f"{start_date} {end_time}", "%Y-%m-%d %H:%M")
        )

        # Google Calendar RRULE uses an exclusive UNTIL boundary.
        # Convert the final occurrence's date to the end of that day.
        until_dt = tz.localize(datetime.combine(end_date_obj, datetime.max.time()))

        # RRULE UNTIL should be in UTC when DTSTART contains timezone info.
        until_utc = until_dt.astimezone(pytz.UTC)

        freq = "DAILY" if frequency == "daily" else "WEEKLY"

        recurrence_rule = (
            f"RRULE:FREQ={freq};"
            f"INTERVAL={interval};"
            f"UNTIL={until_utc.strftime('%Y%m%dT%H%M%SZ')}"
        )

        event_payload = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": timezone,
            },
            "recurrence": [recurrence_rule],
        }

        result = google_cal.create_event(event_payload)

        print(f"Created recurring event: {result}")

        return result

    def delete_event(event_id: str):
        """
        Deletes an event from the user's primary Google Calendar.
        use the get_event tool to extract the event id

        Parameters:
            event_id (str): The unique ID of the calendar event to delete.

        Example:
            delete_event("abc123xyz")
        """
        result = google_cal.delete_event(event_id)
        print(f"Tool delete_event returned: {result}")
        return result

    return [create_event, create_recurring_events, get_events, delete_event]


get_events_tool = {
    "type": "function",
    "function": {
        "name": "get_events",
        "description": "Returns calendar events within a given period starting from today. Supported formats: '{N}d' for N days from today (e.g. '30d'), '{N}m' for N months from today (e.g. '6m'), or 'YYYY-MM-DD' for a specific end date (e.g. '2022-11-14'). Default is '10d' (10 days).",
        "parameters": {
            "type": "object",
            "properties": {
                "max_period": {
                    "type": "string",
                    "description": "Date range to fetch events for. Formats: '{N}d' (N days from today), '{N}m' (N months from today), or 'YYYY-MM-DD' (specific end date). Default '10d'.",
                    "default": "10d",
                }
            },
            "required": [],
        },
    },
}

create_event_tool = {
    "type": "function",
    "function": {
        "name": "create_event",
        "description": "Creates a SINGLE event on Google Calendar. Use this only when creating exactly one event.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Event title"},
                "description": {"type": "string", "description": "Event description"},
                "strt_dateTime": {
                    "type": "string",
                    "description": "Start time in ISO format, e.g. '2026-06-03T19:00:00+05:30'",
                },
                "end_dateTime": {
                    "type": "string",
                    "description": "End time in ISO format, e.g. '2026-06-03T21:00:00+05:30'",
                },
            },
            "required": ["summary", "description", "strt_dateTime", "end_dateTime"],
        },
    },
}

create_recurring_events_tool = {
    "type": "function",
    "function": {
        "name": "create_recurring_events",
        "description": "Creates a recurring daily event between start_date and end_date, at the same time each day. The LLM should NOT enumerate each event — just pass the date range and time. Use this when the user wants the same event repeated across multiple days.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Event title"},
                "description": {"type": "string", "description": "Event description"},
                "start_time": {
                    "type": "string",
                    "description": "Daily start time in HH:MM 24-hour format, e.g. '19:00'",
                },
                "end_time": {
                    "type": "string",
                    "description": "Daily end time in HH:MM 24-hour format, e.g. '21:00'",
                },
                "start_date": {
                    "type": "string",
                    "description": "First occurrence date in YYYY-MM-DD format",
                },
                "end_date": {
                    "type": "string",
                    "description": "Last occurrence date in YYYY-MM-DD format",
                },
            },
            "required": [
                "summary",
                "description",
                "start_time",
                "end_time",
                "start_date",
                "end_date",
            ],
        },
    },
}

delete_event_tool = {
    "type": "function",
    "function": {
        "name": "delete_event",
        "description": "Deletes an event from the user's primary Google Calendar. Use the get_events tool to extract the event id first.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The unique ID of the calendar event to delete, e.g. 'abc123xyz'",
                }
            },
            "required": ["event_id"],
        },
    },
}
