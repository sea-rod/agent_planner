from langchain_core.tools import tool
from .google_calendar import GoogleCalendar

google_cal = GoogleCalendar()
google_cal.connect("../credentials.json")


@tool()
def get_events(max_period:str = "10d") -> list:
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
def create_event(summary, description, strt_dateTime, end_dateTime, **kwargs) -> dict:
    """
    creates an event on google calendar
    you pass a json param
    param:
        events (str): in the following format
        {
            'summary': 'Google I/O 2015',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
            'dateTime': '2025-10-23T09:00:00+05:30',
            },'end': {
            'dateTime': '2025-10-23T10:00:00+05:30',
            }}
    """
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": strt_dateTime},
        "end": {"dateTime": end_dateTime},
    }
    return google_cal.create_event(event)

@tool
def delete_event(event_id:str):
    """
        Deletes an event from the user's primary Google Calendar.
        use the get_event tool to extract the event id

        Parameters:
            event_id (str): The unique ID of the calendar event to delete.

        Example:
            delete_event("abc123xyz")
        """
