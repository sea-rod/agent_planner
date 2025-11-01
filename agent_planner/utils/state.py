from typing import Annotated, TypedDict
from langgraph.graph.message import BaseMessage, add_messages


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    current_time:str