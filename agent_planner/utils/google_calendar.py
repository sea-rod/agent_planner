import datetime
from zoneinfo import ZoneInfo
import os.path
import structlog
from supabase import create_client, Client
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

SCOPES = ["https://www.googleapis.com/auth/calendar.events","https://www.googleapis.com/auth/calendar.settings.readonly"]


class GoogleCalendar:
    def __init__(self): ...

    def connect_with_token(
        self, user_id: str, access_token: str, refresh_token: str = None
    ):
        """Initializes the service using a token provided by the frontend."""
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES,
        )

        # ── Token refresh ─────────────────────────────────────────────────────
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                raise

            # Persist refreshed token to Supabase
            try:
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
            except Exception as e:
                raise

        # ── Build service ─────────────────────────────────────────────────────
        try:
            self.__service = build("calendar", "v3", credentials=creds)
        except Exception as e:
            raise

        print(f"Method connect_with_token returned: True")
        return True

    def connect(self, file):
        """Connect via local OAuth flow (dev/local use only)."""
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.__service = build("calendar", "v3", credentials=creds)
        except HttpError as e:
            raise

        print(f"Method connect returned: True")
        return True

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
        """
        now = datetime.now(tz=ZoneInfo("Asia/Kolkata"))

        # ── Resolve end date ──────────────────────────────────────────────────
        if max_period.endswith("d"):
            days = int(max_period[:-1])
            max_ = now + timedelta(days=days)
        elif max_period.endswith("m"):
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

        # ── API call ──────────────────────────────────────────────────────────
        try:
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
        except HttpError as e:
            raise

        events = events_result.get("items", [])

        if not events:
            result = "No Task were found"
            print(f"Method get_events returned: {result}")
            return result

        all_events = [
            {
                "id": event.get("id"),
                "summary": event.get("summary", "No Title"),
                "start": event.get("start"),
                "end": event.get("end"),
                "recurringEventId": event.get("recurringEventId"),
            }
            for event in events
        ]

        print(f"Method get_events returned: {all_events}")
        return all_events

    def create_event(self, events):
        try:
            event = (
                self.__service.events()
                .insert(calendarId="primary", body=events)
                .execute()
            )
            print(f"Method create_event returned: {event}")
            return event
        except HttpError as e:
            raise

    def delete_event(self, event_id: str):
        """
        Deletes an event from the user's primary Google Calendar.

        Parameters:
            event_id (str): The unique ID of the calendar event to delete.
        """
        try:
            self.__service.events().delete(
                calendarId="primary", eventId=event_id
            ).execute()
            print(f"Method delete_event returned: True")
            return True
        except HttpError as e:
            print(f"Method delete_event returned: False")
            return False

    def get_user_timezone(self) -> str:
        """Fetches the IANA timezone string configured in the user's Google Calendar settings."""
        try:
            setting = self.__service.settings().get(setting="timezone").execute()
            timezone = setting.get("value")
            print(f"Method get_user_timezone returned: {timezone}")
            return timezone
        except Exception as e:
            raise