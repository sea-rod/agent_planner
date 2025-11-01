from langchain_core.messages import HumanMessage, SystemMessage,ToolMessage
from datetime import datetime, timezone, timedelta
from langchain.chat_models import init_chat_model
from .state import AgentState
from .tools import create_event,get_events

from dotenv import load_dotenv

load_dotenv()


tools = [create_event,get_events]
llm = init_chat_model("groq:meta-llama/llama-4-scout-17b-16e-instruct").bind_tools(tools)


sys_prompt = '''
The current time is {current_time}
You are an AI assistant that manages reminders and time-blocking events in Google Calendar.  
If the user sets a reminder without specifying a time, ask them to provide the time instead of calling the calendar tool else call the tool with the right format.  
If the user requests a time-blocking schedule and does not specify a duration (e.g., "for 6 months") ask the user if he still doesn't know for how long keep , default the plan to 30 days.
'''

def get_current_time(state:AgentState)->AgentState:
    ist = timezone(timedelta(hours=5,minutes=30))
    state["current_time"] = datetime.now(ist).isoformat()
    return state
    
def human_feedback(state: AgentState):
    pass

def should_continue(state:AgentState):
    if state["messages"][-1].tool_calls:
        return "tool"
    return "human_feedback"


def model(state: AgentState) -> AgentState:
    sys_mess = SystemMessage(content=sys_prompt.format(current_time=state["current_time"]))
    state["messages"] = llm.invoke([sys_mess]+state['messages'])
    return state