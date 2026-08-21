from fastapi import FastAPI, Depends
from agent import run_pipeline
from utils.user_utils import get_current_user
from schema.chat_request import ChatRequest
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from google_connect import make_flow
from utils.persistence import load_thread_state, save_thread_state, get_state_from_data
import time

load_dotenv()

origins = [
    os.environ.get("FRONTEND_HOST"),
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:4173",
]

server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@server.post("/agent-chat")
async def chat(data: ChatRequest, user_id: str = Depends(get_current_user)):
    t0 = time.perf_counter()

    # ── Resume thread state ─────────────────────────────────────────────────────
    thread_data = load_thread_state(data.thread_id)
    if thread_data:
        state = get_state_from_data(thread_data)
        history = thread_data["history"]
    else:
        state = None
        history = []

    try:
        # Execute the pipeline
        result = run_pipeline(
            user_id=user_id,
            user_message=data.message,
            history=history,
            state=state
        )

        # Save updated state and history
        save_thread_state(data.thread_id, result["state"], result["history"])

        if result["status"] == "planning":
            return {
                "reply": result["response"],
                "is_paused": True,
                "waiting_for": "human_feedback",
            }
        else:
            # Summarize results for the reply
            summary = "Plan executed successfully:\n"
            for item in result["results"]:
                res = item["result"]
                if isinstance(res, dict) and "error" in res:
                    summary += f"- {item['step']}: ❌ {res['error']}\n"
                else:
                    summary += f"- {item['step']}: ✓ Success\n"

            return {
                "reply": summary,
                "is_paused": False,
                "waiting_for": None,
            }

    except Exception as e:
        raise


@server.get("/auth/google/url")
def get_auth_url(user_id: str):
    flow = make_flow()
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        state=user_id,
        prompt="consent",
    )
    return {"url": auth_url}


@server.get("/auth/google/callback")
def google_callback(code: str, state: str):
    user_id = state

    # ── Exchange code for tokens ──────────────────────────────────────────────
    try:
        flow = make_flow()
        flow.fetch_token(code=code)
        creds = flow.credentials
    except Exception as e:
        raise

    # ── Persist to Supabase ───────────────────────────────────────────────────
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE")
    )

    try:
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

    return HTMLResponse("""
        <html><body><script>
            window.opener.postMessage({ type: 'GOOGLE_AUTH_SUCCESS' }, '*');
            window.close();
        </script></body></html>
    """)