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
        os.getenv("SUPABASE_ANON_KEY")
    )
    
    response = (
        supabase.table("user_integrations")
        .select("google_access_token, google_refresh_token")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    
    tokens = response.data
    
    google_cal = GoogleCalendar()
    google_cal.connect_with_token(
        access_token=tokens['google_access_token'],
        refresh_token=tokens['google_refresh_token']
    )
    
    return google_cal