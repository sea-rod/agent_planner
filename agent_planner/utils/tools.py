# tools.py
from langchain_core.tools import tool
from .calendar_helper import get_user_calendar

def create_calendar_tools(state):
    """Factory function that creates tools bound to a specific user's calendar"""
    user_id = state.get("user_id")
    
    if not user_id:
        raise ValueError("user_id not found in state")
    
    google_cal = get_user_calendar(user_id)

    @tool()
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
        return google_cal.get_events(max_period)

    @tool
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
            strt_dateTime: Start in ISO format e.g. "2026-06-03T19:00:00+05:30"
            end_dateTime: End in ISO format
        """
        event_payload = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": strt_dateTime},
            "end": {"dateTime": end_dateTime},
        }
        return google_cal.create_event(event_payload)


    @tool
    def create_recurring_events(
        summary: str,
        description: str,
        start_time: str,       # "HH:MM" e.g. "19:00"
        end_time: str,         # "HH:MM" e.g. "21:00"
        start_date: str,       # "YYYY-MM-DD"
        end_date: str,         # "YYYY-MM-DD"
        timezone: str = "Asia/Kolkata"
    ) -> list[dict]:
        """
        Creates a recurring daily event between start_date and end_date.
        The LLM should NOT enumerate each event — just pass the date range and time.
        Use this when user wants the same event repeated across multiple days.
        
        Parameters:
            summary: Event title
            description: Event description
            start_time: Daily start time in HH:MM (24hr)
            end_time: Daily end time in HH:MM
            start_date: First occurrence YYYY-MM-DD
            end_date: Last occurrence YYYY-MM-DD
            timezone: Timezone string, default Asia/Kolkata
        """
        from datetime import date, timedelta, datetime
        import pytz

        tz = pytz.timezone(timezone)
        current = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        created = []
        while current <= end:
            start_dt = tz.localize(datetime.strptime(f"{current} {start_time}", "%Y-%m-%d %H:%M"))
            end_dt = tz.localize(datetime.strptime(f"{current} {end_time}", "%Y-%m-%d %H:%M"))
            print("p")
            event_payload = {
                "summary": summary,
                "description": description,
                "start": {"dateTime": start_dt.isoformat()},
                "end": {"dateTime": end_dt.isoformat()},
            }
            created.append(google_cal.create_event(event_payload))
            current += timedelta(days=1)
        
        return created

    @tool
    def delete_event(event_id: str):
        """
        Deletes an event from the user's primary Google Calendar.
        use the get_event tool to extract the event id

        Parameters:
            event_id (str): The unique ID of the calendar event to delete.

        Example:
            delete_event("abc123xyz")
        """
        return google_cal.delete_event(event_id)

    return [create_event, create_recurring_events, get_events, delete_event]