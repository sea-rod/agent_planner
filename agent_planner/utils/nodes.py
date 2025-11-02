from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from datetime import datetime, timezone, timedelta
from langchain.chat_models import init_chat_model
from .state import AgentState
from .tools import create_event, get_events, delete_event

from dotenv import load_dotenv

load_dotenv()


tools = [create_event, get_events,delete_event]
llm = init_chat_model("groq:openai/gpt-oss-20b").bind_tools(
    tools
)


sys_prompt = """
The current time is {current_time}
You are an AI assistant that manages reminders and time-blocking events in Google Calendar.  
If the user sets a reminder without specifying a time, ask them to provide the time instead of calling the calendar tool else call the tool with the right format.  
If the user requests a time-blocking schedule and does not specify a duration (e.g., "for 6 months") ask the user if he still doesn't know for how long keep , default the plan to 30 days.
For get_events function this is the format
```get_events()                # events for next 10 days
            get_events("30d")           # events for next 30 days
            get_events("6m")            # events for next 6 months
            get_events("2022-12-31")    # events until specific date
```
"""


def get_current_time(state: AgentState) -> AgentState:
    ist = timezone(timedelta(hours=5, minutes=30))
    state["current_time"] = datetime.now(ist).isoformat()
    return state


def human_feedback(state: AgentState):
    pass


def should_continue(state: AgentState):
    if state["messages"][-1].tool_calls or state["messages"][-1].content=="CONFIRM":
        print("toolllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
        return "tool"
    return "human_feedback"


def model(state: AgentState) -> AgentState:
    sys_mess = SystemMessage(
        content=sys_prompt.format(current_time=state["current_time"])
    )
    state["messages"] = llm.invoke([sys_mess] + state["messages"])
    return state


def classify_model(state: AgentState) -> AgentState:
    sys_prompt = """
                Classify the following task as either 'planner' or 'reminder' for the following user prompt.

- Use 'planner' if it involves creating or scheduling a multi-day plan. Also say planner if you need to delete an event (e.g., completing syllabus chapters before an exam, preparing a project in phases, etc.).
- Use 'reminder' if it is a single or repeating event (e.g., wish someone happy birthday, buy groceries, workout daily at 6 AM, etc.).

Return only ONE word — exactly 'planner' or 'reminder'. No punctuation, no explanation, no extra text.
                """
    sys_mess = SystemMessage(
        content=sys_prompt.format(current_time=state["current_time"])
    )
    state["task_type"] = llm.invoke([sys_mess] + state["messages"]).content
    return state


def route_classifier(state: AgentState):
    if state["task_type"] == "planner":
        return "planner"
    else:
        return "reminder"


### scheduler ###


def get_events_node(state: AgentState):
    sys_prompt = """
You extract the correct argument for the `get_events()` function from user text.

Your ONLY task is to output ONE value — no words, no explanations — exactly matching one of these formats:
- "Nd" → number of days (e.g. "30d")
- "Nm" → number of months (e.g. "6m")
- "YYYY-MM-DD" → exact date

If no clear period or date is mentioned, output "10d".

**Rules:**
- Convert phrases like “next week” → "7d", “next 2 weeks” → "14d", “next 3 months” → "3m".
- If user says “until/till/by/in <date>”, return that date in "YYYY-MM-DD" format.
- If they mention “this month” or “this week”, assume "30d" or "7d".
- Ignore unrelated numbers (like meeting times or version numbers).
- Output must be **only** the value (no quotes, no text, no symbols).

**Examples:**
User: “show upcoming events” → 10d  
User: “get events for next 6 months” → 6m  
User: “events till 2025-12-31” → 2025-12-31  
User: “events next 2 weeks” → 14d  
User: “show me calendar for this week” → 7d  
User: “show events for this month” → 30d  
User: “get events” → 10d  


    """
    period = llm.invoke([sys_prompt]+state["messages"]).content
    print(period)
    state["tasks"] = get_events(period)
    return state


def model_schedule(state:AgentState)->AgentState:
    sys_prompt = """this are the events {events}
    You are a smart planner whose job is to **collect information and build a schedule** (or time-block) for study or project tasks before their deadlines.

Use the following process:
1. Ask for the goal, its deadline, and the type of task (exam, paper, project).
2. Ask how many hours per day you can allocate, and ask for the topics or milestones to cover.
3. Using the existing calendar events (provided in the `events` parameter) identify available slots **before the deadline** (no overlaps allowed).
4. Create and provide a balanced schedule with timings for each topic or milestone.
5. If any essential detail is missing (for example exact time available each day or full list of topics), ask for it **before** proceeding to build the plan.
6. Once everything is set, you will then generate the calendar entries (with timezone +05:30) to add each topic as an event.

⚙️ Confirmation rule:
If the user explicitly confirms the plan — by saying “okay”, “yes”, “go ahead with this plan”, or any equivalent — then respond with **only one word:** `CONFIRM`.

For now: **just gather the information and build the plan** (topics + timings). Do not add events until the plan is confirmed.
"""
    state["messages"] = llm.invoke([sys_prompt.format(events=state["tasks"])]+state["messages"])
    return state



def model_add(state:AgentState)->AgentState:
    sys_prompt = """You are an event creation agent responsible for adding the planned study or project sessions generated by the planner node to Google Calendar.

Follow these steps carefully:

1. Take the confirmed schedule provided by the planner — it may contain one or more topics, each with a specific date, start time, and end time.

2. For each topic or session:
   - Create a dictionary with the following keys:
     {
       "summary": "<short title of the topic or task>",
       "description": "<brief description or goal>",
       "start": {"dateTime": "<ISO format start time with +05:30 timezone>"},
       "end": {"dateTime": "<ISO format end time with +05:30 timezone>"}
     }

3. Combine all such dictionaries into a list called `events_list`.

4. Call the `create_event` tool with:
   - `events_list=events_list`  (if multiple events)
   - OR with individual fields (`summary`, `description`, `strt_dateTime`, `end_dateTime`) if there is only one event.

5. Return the output of the tool, which will contain the confirmation and details of the created Google Calendar events.

Note: All times must include the timezone `+05:30`. Avoid overlaps with existing events in the calendar.
"""
    state["messages"] = llm.invoke([sys_prompt]+state["messages"])
    return state