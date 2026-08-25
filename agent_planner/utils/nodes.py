from datetime import datetime
from zoneinfo import ZoneInfo
from .state import AgentState
from .prompts import (
    SCHEDULING_SYSTEM_PROMPT,
    EXTRACT_STEPS_PROMPT,
    ADD_EVENT_PROMPT,
    TIME_BLOCK_PROMPT,
    DELETE_EVENT_PROMPT,
    EVENT_PARAMS_PROMPT,
)
from .tools import (
    create_event_tool,
    create_recurring_events_tool,
    get_events_tool,
    delete_event_tool,
    create_calendar_tools,
)
from dotenv import load_dotenv
from .calendar_helper import get_user_calendar
from .llm import chat_model
import time
import json

load_dotenv()


# ── Tool Execution Helper ──────────────────────────────────────────────────────


def execute_tool_call(tool_call, state: AgentState):
    """Executes a tool call from the LLM using the user's calendar tools"""
    tools = create_calendar_tools(state)
    tool_map = {t.__name__: t for t in tools}

    function_name = tool_call.function.name
    if function_name not in tool_map:
        return {"error": f"Tool {function_name} not found"}

    args = json.loads(tool_call.function.arguments)

    try:
        result = tool_map[function_name](**args)
        print(f"Tool {function_name} returned: {result}")
        return result
    except Exception as e:
        return {"error": str(e)}


# ── Utility nodes ────────────────────────────────────────────────────────────


def get_current_time(state: AgentState) -> AgentState:
    tz = ZoneInfo(state.time_zone)
    state.current_time = datetime.now(tz).isoformat()
    print(f"Node get_current_time returned: {state}")
    return state


# ── Classifier ───────────────────────────────────────────────────────────────

_classifier_pipeline = None


def _get_classifier():
    global _classifier_pipeline
    if _classifier_pipeline is None:
        import torch
        from transformers import pipeline

        _classifier_pipeline = pipeline(
            "text-classification",
            "sea-rod/bert-AIPlanner-classification",
            torch_dtype=torch.float16,
            device="cpu",
        )
    return _classifier_pipeline


def classify_model(state: AgentState) -> AgentState:
    t0 = time.perf_counter()
    pipe = _get_classifier()

    user_message = (
        state.messages[-1].content
        if hasattr(state.messages[-1], "content")
        else state.messages[-1]
    )
    result = pipe(user_message)[0]
    task_type = result["label"]
    confidence = result["score"]

    state.task_type = task_type

    print(f"Node classify_model returned: {state}")
    return state


def classify_steps(steps: list[str]) -> list[dict]:
    pipe = _get_classifier()
    results = []
    for step in steps:
        res = pipe(step)[0]
        results.append(
            {"step": step, "label": res["label"], "confidence": res["score"]}
        )
    print(f"Node classify_steps returned: {results}")
    return results


# ── Scheduler nodes ──────────────────────────────────────────────────────────


def fetch_calendar_events(state: AgentState):
    # ── 1. Determine Event Range ────────────────────────────────────────────────

    response = chat_model(
        model="openai/gpt-oss-20b",
        msg=[
            {
                "role": "system",
                "content": EVENT_PARAMS_PROMPT.format(today=state.current_time)
            },
            {"role": "user", "content": state.messages[-1]["content"]},
        ],
        temperature=0,
    )

    try:
        params = json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Error parsing event params: {e}")
        params = {"max_period": "10d", "time_min": None, "time_max": None}

    print(f"Determined event range: {params}")

    # ── 2. Fetch Events ───────────────────────────────────────────────────────────
    try:
        google_cal = get_user_calendar(state.user_id)

        events = google_cal.get_events(
            max_period=params.get("max_period", "10d"),
            time_min=params.get("time_min"),
            time_max=params.get("time_max")
        )

        if isinstance(events, list):
            # If the events are too many it returns only the top 7
            events = events[:7]

    except Exception as e:
        print(f"Error in fetch_calendar_events: {e}")
        events = []

    state.tasks = events
    print(f"Node fetch_calendar_events returned: {state}")
    return state


def node_get_events(step: str, state: AgentState) -> dict:
    response = chat_model(
        model="openai/gpt-oss-20b",
        msg=[
            {
                "role": "system",
                "content": "You are a calendar assistant. Use the get_events tool to fetch events for the requested period.",
            },
            {"role": "user", "content": step},
        ],
        tools=[get_events_tool],
        tool_choice="auto",
        temperature=0,
    )

    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        return {"error": "LLM failed to produce a tool call"}

    result = execute_tool_call(tool_calls[0], state)
    print(f"Node node_get_events returned: {result}")
    return result


def scheduling_chat_turn(
    existing_events: list, history: list, user_message: str
) -> str:
    history.append({"role": "user", "content": user_message})

    messages = [
        {
            "role": "system",
            "content": (
                f"{SCHEDULING_SYSTEM_PROMPT}\n\n"
                f"Today's date: {datetime.now().strftime('%Y-%m-%d')}\n"
                f"Existing events: {json.dumps(existing_events)}"
            ),
        },
        *history,
    ]

    response = chat_model(  # swap for your Groq/Gemini client
        model="openai/gpt-oss-20b",
        msg=messages,
    )
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    print(f"Node scheduling_chat_turn returned: {history}")
    return history


def extract_steps(history: list) -> list[str]:
    messages = [
        {"role": "system", "content": EXTRACT_STEPS_PROMPT},
        {"role": "user", "content": json.dumps(history)},
    ]

    response = chat_model(  # swap for your Groq/Gemini client
        model="openai/gpt-oss-20b",
        msg=messages,
        temperature=0,
    )

    result = json.loads(response.choices[0].message.content.strip())

    print(f"Node extract_steps returned: {result}\nlength:{len(result)}")
    return result["steps"]


# ---------- add event / reminder ----------


def node_add(step: str, state: AgentState) -> dict:

    response = chat_model(
        model="openai/gpt-oss-20b",
        msg=[
            {
                "role": "system",
                "content": ADD_EVENT_PROMPT.format(today=state.current_time),
            },
            {"role": "user", "content": step},
        ],
        tools=[create_event_tool],
        tool_choice="auto",
        temperature=0,
    )

    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        return {"error": "LLM failed to produce a tool call"}

    result = execute_tool_call(tool_calls[0], state)
    print(f"Node node_add returned: {result}")
    return result


# ---------- time block ----------


def node_time_blocking(step: str, state: AgentState) -> dict:

    response = chat_model(
        model="openai/gpt-oss-20b",
        msg=[
            {
                "role": "system",
                "content": TIME_BLOCK_PROMPT.format(today=state.current_time),
            },
            {"role": "user", "content": step},
        ],
        tools=[create_recurring_events_tool],
        tool_choice="auto",
        temperature=0,
    )

    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        return {"error": "LLM failed to produce a tool call"}

    result = execute_tool_call(tool_calls[0], state)
    print(f"Node node_time_blocking returned: {result}")
    return result


# ---------- delete ----------


def node_remove(step: str, state: AgentState) -> dict:
    user_id = state.user_id

    if not user_id:
        raise ValueError("user_id not found in state")

    google_cal = get_user_calendar(user_id)
    # events = google_cal.get_events()
    response = chat_model(
        model="openai/gpt-oss-20b",
        msg=[
            {"role": "system", "content": DELETE_EVENT_PROMPT.format(events=state.tasks)},
            {"role": "user", "content": step},
        ],
        tools=[delete_event_tool],
        tool_choice="required",
        temperature=0,
    )

    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        return {"error": "LLM failed to produce a tool call"}

    result = execute_tool_call(tool_calls[0], state)
    print(f"Node node_remove returned: {result}")
    return result
