import datetime
from zoneinfo import ZoneInfo
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_core.tools import tool


SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendar:
    def __init__(self): ...

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

    def get_events(self):
        """
        It returns the events in the calendar
        params:
            self is reference to the function it will be sent automatically just call without arguments
        """
        # Call the Calendar API
        now = datetime.datetime.now(tz=ZoneInfo("Asia/Kolkata")) - datetime.timedelta(
            days=5
        )
        now = now.isoformat()
        print("Getting the upcoming 10 events")
        events_result = (
            self.__service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                # maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        import json

        f = open("res.json", "w")
        json.dump(events, f)
        return events

    def create_event(self, events):
        print("hello function called")
        event = (
            self.__service.events().insert(calendarId="primary", body=events).execute()
        )
        print(f"Event created:{event.get('htmlLink')}")
        return event


if "__main__" == __name__:
    google_cal = GoogleCalendar()

    google_cal.connect("credentials.json")
    google_cal.get_events()

    event = {
        "summary": "Google I/O 2015",
        "location": "800 Howard St., San Francisco, CA 94103",
        "description": "A chance to hear more about Google's developer products.",
        "start": {
            "dateTime": "2025-10-23T09:00:00+05:30",
            # 'timeZone': 'India/Kolkota',
        },
        "end": {
            "dateTime": "2025-10-23T10:00:00+05:30",
            # 'timeZone': 'India/Kolkota',
        },
    }

    google_cal.create_event(event)
