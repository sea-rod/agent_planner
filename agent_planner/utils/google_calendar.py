import datetime
from zoneinfo import ZoneInfo
import os.path
import time
import structlog
from supabase import create_client, Client
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .logging_config import log_token_refresh, log_calendar_api

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

log = structlog.get_logger("atelier.calendar")


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
            log.info("token_refresh_attempt", user_id=user_id, provider="google")
            try:
                creds.refresh(Request())
                log_token_refresh(user_id=user_id, provider="google", success=True)
            except Exception as e:
                log_token_refresh(user_id=user_id, provider="google", success=False, error=str(e))
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
                log.info("refreshed_token_persisted", user_id=user_id, provider="google")
            except Exception as e:
                log.error("refreshed_token_persist_failed", user_id=user_id, error=str(e), exc_info=True)
                raise

        # ── Build service ─────────────────────────────────────────────────────
        try:
            self.__service = build("calendar", "v3", credentials=creds)
            log.info("calendar_service_connected", user_id=user_id, method="frontend_token")
        except Exception as e:
            log.error("calendar_service_connect_failed", user_id=user_id, error=str(e), exc_info=True)
            raise

    def connect(self, file):
        """Connect via local OAuth flow (dev/local use only)."""
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            log.debug("token_loaded_from_file")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                log.info("token_refresh_attempt", method="local_file")
                creds.refresh(Request())
                log.info("token_refreshed", method="local_file")
            else:
                log.info("oauth_flow_starting", file=file)
                flow = InstalledAppFlow.from_client_secrets_file(file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            log.info("token_saved_to_file")

        try:
            self.__service = build("calendar", "v3", credentials=creds)
            log.info("calendar_service_connected", method="local_file")
        except HttpError as e:
            log.error("calendar_service_connect_failed", method="local_file", error=str(e), exc_info=True)
            raise

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
        log.info("get_events_start", max_period=max_period)

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
                log.error("get_events_invalid_period", max_period=max_period)
                raise ValueError(
                    "Invalid max_period format. Use '{N}d', '{N}m', or 'YYYY-MM-DD'."
                )

        log.debug("get_events_range", date_from=now.date().isoformat(), date_to=max_.date().isoformat())

        # ── API call ──────────────────────────────────────────────────────────
        t0 = time.perf_counter()
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
            elapsed_ms = (time.perf_counter() - t0) * 1000
            log_calendar_api(method="events.list", calendar_id="primary", status_code=200, latency_ms=elapsed_ms)
        except HttpError as e:
            elapsed_ms = (time.perf_counter() - t0) * 1000
            log_calendar_api(method="events.list", calendar_id="primary", status_code=e.status_code, latency_ms=elapsed_ms)
            log.error("get_events_api_error", error=str(e), exc_info=True)
            raise

        events = events_result.get("items", [])

        if not events:
            log.info("get_events_empty", max_period=max_period)
            return "No Task were found"

        all_events = [
            {
                "id": event.get("id"),
                "summary": event.get("summary", "No Title"),
                "start": event.get("start"),
                "end": event.get("end"),
            }
            for event in events
        ]

        log.info("get_events_done", event_count=len(all_events), max_period=max_period)
        return all_events

    def create_event(self, events):
        log.info("create_event_start", is_batch=isinstance(events, list),
                 event_count=len(events) if isinstance(events, list) else 1)

        t0 = time.perf_counter()
        try:
            event = (
                self.__service.events()
                .insert(calendarId="primary", body=events)
                .execute()
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
            log_calendar_api(method="events.insert", calendar_id="primary", status_code=200, latency_ms=elapsed_ms)
            log.info("create_event_done", event_id=event.get("id"), html_link=event.get("htmlLink"))
        except HttpError as e:
            elapsed_ms = (time.perf_counter() - t0) * 1000
            log_calendar_api(method="events.insert", calendar_id="primary", status_code=e.status_code, latency_ms=elapsed_ms)
            log.error("create_event_failed", error=str(e), exc_info=True)
            raise

        return event

    def delete_event(self, event_id: str):
        """
        Deletes an event from the user's primary Google Calendar.

        Parameters:
            event_id (str): The unique ID of the calendar event to delete.
        """
        log.info("delete_event_start", event_id=event_id)

        t0 = time.perf_counter()
        try:
            self.__service.events().delete(
                calendarId="primary", eventId=event_id
            ).execute()
            elapsed_ms = (time.perf_counter() - t0) * 1000
            log_calendar_api(method="events.delete", calendar_id="primary", status_code=200, latency_ms=elapsed_ms)
            log.info("delete_event_done", event_id=event_id)
            return True
        except HttpError as e:
            elapsed_ms = (time.perf_counter() - t0) * 1000
            log_calendar_api(method="events.delete", calendar_id="primary", status_code=e.status_code, latency_ms=elapsed_ms)
            log.error("delete_event_failed", event_id=event_id, status_code=e.status_code, error=str(e), exc_info=True)
            return False