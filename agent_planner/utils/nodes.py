from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from datetime import datetime, timezone, timedelta
from langchain.chat_models import init_chat_model
from .state import AgentState
from .tools import create_event, get_events, delete_event

from dotenv import load_dotenv

load_dotenv()


tools = [create_event, get_events,delete_event]
llm = init_chat_model("groq:meta-llama/llama-4-scout-17b-16e-instruct").bind_tools(
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
    if state["messages"][-1].tool_calls:
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
    sys_prompt = """You are a smart planner that helps schedule study or project tasks before their deadlines.
            All current calendar events are in the events parameter.
            When user gives a new task or exam, do the following:

            1. Identify goal, deadline, and type (exam, paper, project).

            2. Ask how many hours per day they can give and what topics/milestones to cover.

            3. Check events for free time before the deadline — no overlaps allowed.

            4. Create and confirm a balanced plan or time-block schedule.

            5. If details (like time or topics) are missing, ask before adding to schedule.

            6. Finally add these topics to the google calendar using the create_event function
            """
    state["messages"] = llm.invoke([sys_prompt]+state["messages"])
    return state