from langchain_core.messages import SystemMessage
from datetime import datetime
from zoneinfo import ZoneInfo
from langchain.chat_models import init_chat_model
from .state import AgentState
from .tools import create_calendar_tools
from dotenv import load_dotenv
from .calendar_helper import get_user_calendar
from .logging_config import log_graph_node, log_groq_call, log_intent
import structlog
import time

load_dotenv()

log = structlog.get_logger("atelier.agent")

base_llm = init_chat_model("groq:openai/gpt-oss-20b",temperature=0,top_p=0)

MAIN_SYSTEM_PROMPT = """
The current time is {current_time}.
You are an assistant that manages reminders and time-blocking events in Google Calendar. Be precise and follow rules exactly.

Goals:
- If user gives a reminder WITHOUT a specific time → ask for the time (do NOT call the calendar).
- If user requests a time-blocking plan and does NOT specify a duration → ask for duration; if user still doesn't know, default to 30 days.
- When calling calendar tools, always use ISO datetimes with timezone +05:30.

Tool usage guidance (exact accepted `get_events()` formats):
- get_events()        → default next 10 days
- get_events("Nd")    → next N days (e.g., "30d")
- get_events("Nm")    → next N months (e.g., "6m")
- get_events("YYYY-MM-DD") → until that date

Output rules:
- Be explicit, minimal, and actionable.
- When you plan, collect all missing info first before creating events.
- When user confirms a plan with "okay", "yes", "go ahead" (or equivalents) do the tool call
"""

CLASSIFY_PROMPT = """
Classify the user's prompt as exactly ONE of: planner OR reminder OR delete.
Rules:
- Return ONLY the single word: planner OR reminder OR delete. No punctuation, no explanation.
- Use planner for multi-day plans, study/project schedules, or when the user asks to create multi-step plans.
- Use reminder for single events or repeating single-slot events (birthdays, single meeting, daily workout).
- Use delete when the user asks to delete/modify multi-step plans.
- Use get_events when user suggest to retrive the events
Examples:
- "Study schedule for 6 months before exams" → planner
- "Remind me to call mom every Sunday" → reminder
- "Delete my study sessions" → delete
- "Get all the events" → get_event
"""

GET_EVENTS_EXTRACTOR_PROMPT = """
Your ONLY job: output exactly ONE token (no quotes, no text) matching one of:
- Nd  (e.g., 30d)
- Nm  (e.g., 6m)
- YYYY-MM-DD

Rules (map natural language → output):
- "next week" → 7d; "next 2 weeks" → 14d
- "this week" → 7d; "this month" → 30d
- "next N months" → Nm
- "until/till/by/on <date>" → YYYY-MM-DD (use ISO date)
- If no period/date found → 10d
Ignore unrelated numbers (times, versions). Output exactly one token only.

Examples:
- "show events next 6 months" → 6m
- "events till 2025-12-31" → 2025-12-31
"""

PLANNER_PROMPT = """
Context: {events}

DO NOT CALL get_events() function

Role: You are a planner that builds multi-day time-blocked schedules before deadlines.

Procedure (strict):
1. Extract goal, deadline, and milestones from the user text.
2. If missing: ask for available hours/day, topics/milestones, and hard deadlines — do not proceed until you have them.
3. Inspect {events} to find free, non-overlapping slots before the deadline.
4. Propose a balanced plan (daily or weekly) listing each session: topic → date → start_time → end_time (ISO +05:30).
5. Do NOT create calendar events yet. Present the plan and any tradeoffs.

Confirmation rule:
- When user explicitly confirms (e.g., "yes", "okay", "go ahead with this plan"), reply exactly: CONFIRM
"""

EVENT_CREATION_PROMPT = """
Role: Event creator. Input = confirmed schedule from planner.

IMPORTANT: When calling tools, use only plain ASCII characters in all arguments. 
Do NOT use typographic hyphens (‑), smart quotes (" "), em dashes (—), or any 
non-ASCII punctuation. Use regular hyphens (-), straight quotes ('), and standard 
ASCII only.

Do NOT wrap the JSON in markdown code blocks (```json), and do NOT add trailing characters like semicolons, parentheses, or closing tags (e.g., ');' or '}};'). Stop generating immediately after the final closing curly brace.

For each session produce a dict:
{{
 "summary": "<short title>",
 "description": "<goal or brief note>",
 "start": {{"dateTime": "<ISO datetime with +05:30>"}},
 "end":   {{"dateTime": "<ISO datetime with +05:30>"}}
}}


If multiple sessions, batch them into a list of event dicts and call create_bulk_events(events: list[dict]) where dict is 
{{
summary:..., description:..., strt_dateTime:..., end_dateTime:...
}}.
If only one session -> call create_event(summary=..., description=..., strt_dateTime=..., end_dateTime=...).

Constraints:
- All datetimes must be ISO and include {time_zone} timezone.
- If More than 1 events are needed to be created then use events_list (list of dicts) and call create_event(events_list=events_list)
- Do not modify existing events; skip conflicting slots and report skipped items.
- Return the tool's output as-is.
"""

DELETE_PROMPT = """
Role: Event deleter. Input = user request to delete events.
All Events: {events}

1.  Identify the events the user wants to delete from the context.
2.  Extract the event IDs of the events to be deleted from All Events.
3.  If you are unsure which events to delete, ask for clarification.
4.  Before deleting, ask for confirmation from the user.
5.  call the delete_event node
6.  When user explicitly confirms (e.g., "yes", "okay", "go ahead with this plan"), call the `delete_event` tool for each `event_id`.
"""


# ── Utility nodes ────────────────────────────────────────────────────────────

def get_current_time(state: AgentState) -> AgentState:
    tz = ZoneInfo(state["time_zone"])
    state["current_time"] = datetime.now(tz).isoformat()
    log.debug("current_time_set", time_zone=state["time_zone"], current_time=state["current_time"])
    return state


def human_feedback(state: AgentState):
    pass


def should_continue(state: AgentState):
    last_msg = state["messages"][-1]
    has_tool_calls = bool(last_msg.tool_calls)
    is_confirm = last_msg.content == "CONFIRM"

    if has_tool_calls or is_confirm:
        log.debug("should_continue_routing", route="tool", has_tool_calls=has_tool_calls, is_confirm=is_confirm)
        return "tool"

    log.debug("should_continue_routing", route="human_feedback")
    return "human_feedback"


# ── Main model ───────────────────────────────────────────────────────────────

def model(state: AgentState):
    """Enhanced model with memory context."""
    t0 = time.perf_counter()

    tools = create_calendar_tools(state)
    llm = base_llm.bind_tools(tools)

    preferences     = state.get("relevant_preferences", [])
    similar_convos  = state.get("similar_conversations", [])
    patterns        = state.get("scheduling_patterns", [])

    log.debug(
        "model_context_loaded",
        preferences_count=len(preferences),
        similar_convos_count=len(similar_convos),
        patterns_count=len(patterns),
    )

    memory_context = "\n\n=== RELEVANT USER CONTEXT ===\n"
    if preferences:
        memory_context += "\nUSER PREFERENCES:\n"
        for pref in preferences[:3]:
            memory_context += f"- {pref['text']}\n"
    if similar_convos:
        memory_context += "\nSIMILAR PAST CONVERSATIONS:\n"
        for conv in similar_convos[:2]:
            memory_context += f"- User asked: {conv['user_message'][:60]}...\n"
    if patterns:
        memory_context += "\nSCHEDULING PATTERNS:\n"
        for pattern in patterns[:3]:
            memory_context += f"- {pattern['description']}\n"

    enhanced_prompt = (
        MAIN_SYSTEM_PROMPT.format(current_time=state["current_time"]) + memory_context
    )

    messages = [SystemMessage(content=enhanced_prompt)] + state["messages"]

    try:
        response = llm.invoke(messages)
    except Exception as e:
        log.error("model_invoke_failed", node="model", error=str(e), exc_info=True)
        raise

    elapsed_ms = (time.perf_counter() - t0) * 1000
    log_graph_node("model", elapsed_ms=elapsed_ms)

    # Log token usage if available
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        u = response.usage_metadata
        log_groq_call(
            model="gpt-oss-20b",
            prompt_tokens=u.get("input_tokens", 0),
            completion_tokens=u.get("output_tokens", 0),
            latency_ms=elapsed_ms,
        )

    has_tool_calls = bool(getattr(response, "tool_calls", None))
    log.info("model_response", has_tool_calls=has_tool_calls, elapsed_ms=round(elapsed_ms, 2))

    return state


# ── Classifier ───────────────────────────────────────────────────────────────

_classifier_pipeline = None

def _get_classifier():
    global _classifier_pipeline
    if _classifier_pipeline is None:
        log.info("bert_classifier_loading", model="sea-rod/bert-AIPlanner-classification")
        import torch
        from transformers import pipeline
        _classifier_pipeline = pipeline(
            "text-classification",
            "sea-rod/bert-AIPlanner-classification",
            torch_dtype=torch.float16,
            device="cpu",
        )
        log.info("bert_classifier_loaded")
    return _classifier_pipeline


def classify_model(state: AgentState) -> AgentState:
    t0 = time.perf_counter()
    pipe = _get_classifier()

    user_message = state["messages"][-1].content
    result = pipe(user_message)[0]
    task_type = result["label"]
    confidence = result["score"]

    # log_intent hashes the text, flags low confidence < 0.6
    log_intent(text=user_message, intent=task_type, confidence=confidence)

    state["task_type"] = task_type

    log_graph_node("classify_model", elapsed_ms=(time.perf_counter() - t0) * 1000)
    return state


def route_classifier(state: AgentState):
    task_type = state.get("task_type", "")
    route_map = {
        "planner":   "planner",
        "delete":    "delete",
        "get_event": "get_event",
    }
    route = route_map.get(task_type, "reminder")
    log.info("route_classifier", task_type=task_type, route=route)
    return route


# ── Scheduler nodes ──────────────────────────────────────────────────────────

def get_events_node(state: AgentState):
    t0 = time.perf_counter()
    log.info("get_events_node_start", user_id=state["user_id"])

    try:
        google_cal = get_user_calendar(state["user_id"])
        period = "10d"
        events = google_cal.get_events(period)
    except Exception as e:
        log.error("get_events_failed", user_id=state["user_id"], error=str(e), exc_info=True)
        raise

    state["tasks"] = events
    log_graph_node("get_events_node", elapsed_ms=(time.perf_counter() - t0) * 1000)
    log.info("get_events_node_done", period=period, event_count=len(events) if isinstance(events, list) else "unknown")
    return state


def model_schedule(state: AgentState) -> AgentState:
    t0 = time.perf_counter()
    tools = create_calendar_tools(state)
    llm = base_llm.bind_tools(tools)

    sys_mess = SystemMessage(content=PLANNER_PROMPT.format(events=state.get("tasks", [])))

    try:
        response = llm.invoke([sys_mess] + state["messages"])
    except Exception as e:
        log.error("model_schedule_failed", error=str(e), exc_info=True)
        raise

    state["messages"] = response

    print("\n\n\n",response,end="\n\n\n")

    log_graph_node("model_schedule", elapsed_ms=(time.perf_counter() - t0) * 1000)
    log.info("model_schedule_done", has_tool_calls=bool(getattr(response, "tool_calls", None)))
    return state

import json
def sanitize_messages(messages):
    import unicodedata
    cleaned = []
    
    for msg in messages:
        # print()
        print("\n\n\n\n\n\n", msg,end="\n\n\n\n\n\n")
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            # Fix unicode in tool call arguments
            clean_tool_calls = []
            for tc in msg.tool_calls:

                print("tccccccccccccc:",tc)
                
                if isinstance(tc.get('arguments'), dict):
                    clean_args = json.loads(
                        unicodedata.normalize("NFKD", json.dumps(tc['arguments']))
                        .encode("ascii", "ignore").decode("ascii")
                    )
                    tc = {**tc, 'arguments': clean_args}
                clean_tool_calls.append(tc)
            msg = msg.copy(update={"tool_calls": clean_tool_calls})
        cleaned.append(msg)
    return cleaned

def model_add(state: AgentState) -> AgentState:
    t0 = time.perf_counter()
    tools = create_calendar_tools(state)
    llm = base_llm.bind_tools(tools)
    sys_mess = SystemMessage(content=EVENT_CREATION_PROMPT.format(time_zone=state["time_zone"]))
    try:
        clean_messages = sanitize_messages(state["messages"][-4:])
        response = llm.invoke([sys_mess] + clean_messages)
    except Exception as e:
        log.error("model_add_failed", time_zone=state["time_zone"], error=str(e), exc_info=True)
        raise

    state["messages"] = response
    print("\n\n\n add node:",response,end="\n\n\n")
    log_graph_node("model_add", elapsed_ms=(time.perf_counter() - t0) * 1000)

    tool_calls = getattr(response, "tool_calls", [])
    log.info(
        "model_add_done",
        tool_calls_count=len(tool_calls),
        tools_called=[tc["name"] for tc in tool_calls] if tool_calls else [],
    )
    return state


def model_delete(state: AgentState) -> AgentState:
    t0 = time.perf_counter()
    tools = create_calendar_tools(state)
    llm = base_llm.bind_tools(tools)

    sys_mess = SystemMessage(content=DELETE_PROMPT.format(events=state.get("tasks", [])))

    try:
        response = llm.invoke([sys_mess] + state["messages"])
    except Exception as e:
        log.error("model_delete_failed", error=str(e), exc_info=True)
        raise

    state["messages"] = response
    log_graph_node("model_delete", elapsed_ms=(time.perf_counter() - t0) * 1000)

    tool_calls = getattr(response, "tool_calls", [])
    log.info(
        "model_delete_done",
        tool_calls_count=len(tool_calls),
        tools_called=[tc["name"] for tc in tool_calls] if tool_calls else [],
    )
    return state