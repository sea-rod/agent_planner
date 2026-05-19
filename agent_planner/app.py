from fastapi import FastAPI, Depends, Header
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from langgraph.types import Command
from .agent import app, checkpointer
from .utils.user_utils import get_current_user
from .schema.chat_request import ChatRequest
from supabase import create_client, Client
from .utils.google_calendar import GoogleCalendar
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .google_connect import make_flow

load_dotenv()

server = FastAPI()


origins = [
    os.environ.get("FRONTEND_HOST"),
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:4173",
]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.py
@server.post("/agent-chat")
async def chat(data: ChatRequest, user_id: str = Depends(get_current_user)):
    config = {"configurable": {"thread_id": data.thread_id}}

    # Fetch tokens and create Google Calendar instance
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY")
    )

    response = (
        supabase.table("user_integrations")
        .select("google_access_token, google_refresh_token")
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    tokens = response.data

    # Create user-specific Google Calendar instance
    google_cal = GoogleCalendar()
    google_cal.connect_with_token(
        access_token=tokens["google_access_token"],
        refresh_token=tokens["google_refresh_token"],
    )

    # Check if resuming from pause
    state = await app.aget_state(config)

    if state.next:
        current_node = state.next[0]
        await app.aupdate_state(
            config, {"messages": [data.message]}, as_node=current_node
        )
        inputs = None
    else:
        # Pass google_cal in initial state
        inputs = {
            "messages": [("user", data.message)],
            "user_id": user_id,
        }

    final_output = ""
    async for event in app.astream(inputs, config=config, stream_mode="values"):
        final_output = event["messages"][-1].content

    new_state = await app.aget_state(config)

    return {
        "reply": final_output,
        "is_paused": len(new_state.next) > 0,
        "waiting_for": new_state.next[0] if new_state.next else None,
    }


@server.get("/auth/google/url")
def get_auth_url(user_id: str):
    flow = make_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        # include_granted_scopes="true",
        state=user_id,  # pass user_id through state so callback knows who this is
        prompt="consent",
    )
    return {"url": auth_url}


@server.get("/auth/google/callback")
def google_callback(code: str, state: str):
    user_id = state  # we passed user_id as state
    flow = make_flow()
    flow.fetch_token(code=code)
    creds = flow.credentials

    # Store in Supabase
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

    # Close the popup — return a page that sends postMessage to opener
    return HTMLResponse("""
        <html><body><script>
            window.opener.postMessage({ type: 'GOOGLE_AUTH_SUCCESS' }, '*');
            window.close();
        </script></body></html>
    """)
