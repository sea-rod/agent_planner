from dataclasses import dataclass
from typing import Optional
from .google_calendar import GoogleCalendar

@dataclass
class AgentState:
    messages: list
    current_time: str = ""
    task_type: str = ""
    tasks: list = None
    user_id: str = ""
    thread_id: str = ""
    time_zone: str = "UTC"
    relevant_preferences: Optional[list] = None
    similar_conversations: Optional[list] = None
    scheduling_patterns: Optional[list] = None

    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []
