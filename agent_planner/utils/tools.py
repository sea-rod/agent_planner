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
        """Returns calendar events within a given period starting from today."""
        return google_cal.get_events(max_period)

    @tool
    def create_event(
        summary: str = None,
        description: str = None,
        strt_dateTime: str = None,
        end_dateTime: str = None,
        events_list: list[dict] = None,
        **kwargs
    ) -> list[dict]:
        """Creates one or more events on Google Calendar."""
        created_events = []
        
        if events_list is not None:
            for ev in events_list:
                created = google_cal.create_event(ev)
                created_events.append(created)
        else:
            if None in (summary, description, strt_dateTime, end_dateTime):
                raise ValueError("Must supply either events_list or all parameters")
            event_payload = {
                "summary": summary,
                "description": description,
                "start": {"dateTime": strt_dateTime},
                "end": {"dateTime": end_dateTime},
            }
            created = google_cal.create_event(event_payload)
            created_events.append(created)
        
        return created_events

    @tool
    def delete_event(event_id: str):
        """Deletes an event from the user's primary Google Calendar."""
        return google_cal.delete_event(event_id)

    return [create_event, get_events, delete_event]