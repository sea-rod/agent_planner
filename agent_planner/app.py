from fastapi import FastAPI, Depends, Header
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from langgraph.types import Command
from .agent import app, checkpointer
from .utils.user_utils import get_current_user
from .schema.chat_request import ChatRequest
from supabase import create_client,Client
from .utils.google_calendar import GoogleCalendar
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware   

load_dotenv()

server = FastAPI()



origins = [
    "http://localhost.tiangolo.com",
    "https://127.0.0.1:8080",
    "http://localhost",
    "http://localhost:5173",
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
    
    # Create user-specific Google Calendar instance
    google_cal = GoogleCalendar()
    google_cal.connect_with_token(
        access_token=tokens['google_access_token'],
        refresh_token=tokens['google_refresh_token']
    )
    
    # Check if resuming from pause
    state = await app.aget_state(config)
    
    if state.next:
        current_node = state.next[0]
        await app.aupdate_state(
            config, 
            {"messages": [data.message]},
            as_node=current_node
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