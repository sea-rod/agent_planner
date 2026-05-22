import datetime
from zoneinfo import ZoneInfo
import os.path
import json
from supabase import create_client, Client
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


class GoogleCalendar:
    def __init__(self): ...

    def connect_with_token(
        self, user_id: str, access_token: str, refresh_token: str = None
    ):
        """
        Initializes the service using a token provided by the frontend.
        """
        # Note: You still need your Client ID and Secret if you want
        # the library to handle token refreshing automatically.

        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

        print(client_id, client_secret)

        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES,
        )

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            supabase: Client = create_client(
                os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE")
            )
            supabase.table("calendar_tokens").upsert(
                {
                    "user_id": user_id,
                    "provider": "google",
                    "access_token": creds.token,
                    "refresh_token": creds.refresh_token,
                    "token_uri": creds.token_uri,
                    "client_id": creds.client_id,
                    "client_secret": creds.client_secret,
                    "scopes": list(creds.scopes),
                },
                on_conflict="user_id,provider",
            ).execute()

        try:
            self.__service = build("calendar", "v3", credentials=creds)
            print(" Connected successfully via frontend token")
        except Exception as error:
            print(f"Connection failed: {error}")

    def connect(self, file):
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.__service = build("calendar", "v3", credentials=creds)
            print("connected successful")
        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_events(self, max_period: str = "10d"):
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
        now = datetime.now(tz=ZoneInfo("Asia/Kolkata"))
        print(max_period)
        # Determine end date
        if max_period.endswith("d"):  # days
            days = int(max_period[:-1])
            max_ = now + timedelta(days=days)
        elif max_period.endswith("m"):  # months
            months = int(max_period[:-1])
            max_ = now + relativedelta(months=months)
        else:
            try:
                max_ = datetime.fromisoformat(max_period).replace(
                    tzinfo=ZoneInfo("Asia/Kolkata")
                ) + timedelta(days=1)
            except ValueError:
                raise ValueError(
                    "Invalid max_period format. Use '{N}d', '{N}m', or 'YYYY-MM-DD'."
                )

        print(f"Getting events from {now.date()} to {max_.date()} {max_.isoformat()}")

        events_result = (
            self.__service.events()
            .list(
                calendarId="primary",
                timeMin=now.isoformat(),
                timeMax=max_.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            return "No Task were found"

        all_events = []

        for event in events:
            event_dict = {
                "id": event.get("id"),
                "summary": event.get("summary", "No Title"),
                "start": event.get("start"),
                "end": event.get("end"),
            }
            all_events.append(event_dict)

        return all_events

    def create_event(self, events):
        print("hello function called")
        event = (
            self.__service.events().insert(calendarId="primary", body=events).execute()
        )
        print(f"Event created:{event.get('htmlLink')}")
        return event

    def delete_event(self, event_id: str):
        """
        Deletes an event from the user's primary Google Calendar.

        Parameters:
            event_id (str): The unique ID of the calendar event to delete.

        Example:
            delete_event("abc123xyz")
        """
        try:
            self.__service.events().delete(
                calendarId="primary", eventId=event_id
            ).execute()
            print(f"Event deleted successfully (ID: {event_id})")
            return True
        except HttpError as error:
            print(f"An error occurred while deleting the event: {error}")
            return False
