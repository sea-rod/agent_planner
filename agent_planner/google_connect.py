from google_auth_oauthlib.flow import Flow
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def make_flow():

    config = {
        "web": {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "redirect_uris": [os.environ["GOOGLE_REDIRECT_URI"]],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    return Flow.from_client_config(
        config,
        scopes=SCOPES,
        redirect_uri=os.environ["GOOGLE_CALLBACK"],
    )


if __name__ == "__main__":
    flow = make_flow()
    print(
        flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            state="helloworld",  # pass user_id through state so callback knows who this is
            prompt="consent",
        )
    )