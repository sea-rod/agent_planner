from fastapi import FastAPI, Depends
from langgraph.types import Command
from .agent import app, checkpointer
from .utils.user_utils import get_current_user
from .schema.chat_request import ChatRequest
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import structlog
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .google_connect import make_flow
from .utils.logging_config import (
    setup_logging,
    UVICORN_LOG_CONFIG,
    RequestLoggingMiddleware,
    log_oauth_callback,
    log_token_refresh,
    log_graph_node,
    bind_request_context,
)
import time

load_dotenv()

setup_logging(
    level=os.getenv("LOG_LEVEL", "INFO"),
    pretty=os.getenv("ENV", "production") == "development",
)

log = structlog.get_logger("atelier.server")

origins = [
    os.environ.get("FRONTEND_HOST"),
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:4173",
]

server = FastAPI()

server.add_middleware(RequestLoggingMiddleware)  # logs every request automatically
server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@server.post("/agent-chat")
async def chat(data: ChatRequest, user_id: str = Depends(get_current_user)):
    # Bind user_id so every downstream log in this request carries it
    bind_request_context(user_id=user_id)

    log.info(
        "agent_chat_received",
        thread_id=data.thread_id,
        message_preview=data.message[:80],  # truncate — don't log full user input
    )

    config = {"configurable": {"thread_id": data.thread_id}}

    # ── Resume paused graph or start fresh ───────────────────────────────────
    t0 = time.perf_counter()
    state = await app.aget_state(config)

    if state.next:
        current_node = state.next[0]
        log.info("agent_resuming_paused_graph", node=current_node, thread_id=data.thread_id)
        await app.aupdate_state(
            config, {"messages": [data.message]}, as_node=current_node
        )
        inputs = None
    else:
        log.info("agent_starting_fresh", thread_id=data.thread_id, time_zone=data.time_zone)
        inputs = {
            "messages": [("user", data.message)],
            "user_id": user_id,
            "time_zone": data.time_zone,
        }

    # ── Stream graph ─────────────────────────────────────────────────────────
    final_output = ""
    event_count = 0
    try:
        async for event in app.astream(inputs, config=config, stream_mode="values"):
            final_output = event["messages"][-1].content
            event_count += 1
    except Exception as e:
        log.error(
            "agent_stream_error",
            thread_id=data.thread_id,
            error=str(e),
            elapsed_ms=round((time.perf_counter() - t0) * 1000, 2),
            exc_info=True,
        )
        raise

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
    new_state = await app.aget_state(config)
    is_paused = len(new_state.next) > 0

    log.info(
        "agent_chat_completed",
        thread_id=data.thread_id,
        elapsed_ms=elapsed_ms,
        event_count=event_count,
        is_paused=is_paused,
        waiting_for=new_state.next[0] if new_state.next else None,
    )

    return {
        "reply": final_output,
        "is_paused": is_paused,
        "waiting_for": new_state.next[0] if new_state.next else None,
    }


@server.get("/auth/google/url")
def get_auth_url(user_id: str):
    log.info("google_auth_url_requested", user_id=user_id)
    flow = make_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        state=user_id,
        prompt="consent",
    )
    log.debug("google_auth_url_generated", user_id=user_id)
    return {"url": auth_url}


@server.get("/auth/google/callback")
def google_callback(code: str, state: str):
    user_id = state
    bind_request_context(user_id=user_id)
    log.info("google_callback_received", user_id=user_id)

    # ── Exchange code for tokens ──────────────────────────────────────────────
    try:
        flow = make_flow()
        flow.fetch_token(code=code)
        creds = flow.credentials
    except Exception as e:
        log.error("google_token_exchange_failed", user_id=user_id, error=str(e), exc_info=True)
        raise

    log.info(
        "google_token_exchange_succeeded",
        user_id=user_id,
        scopes=list(creds.scopes),
        has_refresh_token=creds.refresh_token is not None,
    )

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
        log.info("calendar_tokens_upserted", user_id=user_id, provider="google")
    except Exception as e:
        log.error(
            "calendar_tokens_upsert_failed",
            user_id=user_id,
            provider="google",
            error=str(e),
            exc_info=True,
        )
        raise

    # Emit structured OAuth callback event
    log_oauth_callback(user_id=user_id, provider="google", scopes=list(creds.scopes))

    return HTMLResponse("""
        <html><body><script>
            window.opener.postMessage({ type: 'GOOGLE_AUTH_SUCCESS' }, '*');
            window.close();
        </script></body></html>
    """)