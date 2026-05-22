# utils/calendar_helper.py
from supabase import create_client, Client
from .google_calendar import GoogleCalendar
import os

def get_user_calendar(user_id: str) -> GoogleCalendar:
    """
    Fetches Google Calendar instance for a specific user.
    Called fresh in each node that needs it.
    """
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"), 
        os.getenv("SUPABASE_SERVICE_ROLE")
    )
    
    response = (
        supabase.table("calendar_tokens")
        .select("access_token, refresh_token")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    
    tokens = response.data
    
    google_cal = GoogleCalendar()
    google_cal.connect_with_token(
        user_id,
        access_token=tokens['access_token'],
        refresh_token=tokens['refresh_token']
    )
    
    return google_cal