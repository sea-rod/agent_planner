from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import BaseMessage, add_messages
from .google_calendar import GoogleCalendar

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    current_time: str
    task_type: str
    tasks: list[dict]
    user_id: str
    thread_id: str
    relevant_preferences: Optional[list]
    similar_conversations: Optional[list]
    scheduling_patterns: Optional[list]
