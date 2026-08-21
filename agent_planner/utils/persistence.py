import json
import os
from typing import Optional, List, Any
from .state import AgentState

# Simple file-based persistence for thread state
# This can be easily replaced with Supabase/Redis later
STATE_DIR = "thread_states"

def _ensure_dir():
    if not os.path.exists(STATE_DIR):
        os.makedirs(STATE_DIR)

def save_thread_state(thread_id: str, state: AgentState, history: List[dict]):
    """Saves the agent state and conversation history to a JSON file."""
    _ensure_dir()
    file_path = os.path.join(STATE_DIR, f"{thread_id}.json")

    # Convert dataclass to dict
    state_dict = {
        "user_id": state.user_id,
        "current_time": state.current_time,
        "task_type": state.task_type,
        "tasks": state.tasks,
        "time_zone": state.time_zone,
        "relevant_preferences": state.relevant_preferences,
        "similar_conversations": state.similar_conversations,
        "scheduling_patterns": state.scheduling_patterns,
    }

    data = {
        "state": state_dict,
        "history": history
    }

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def load_thread_state(thread_id: str) -> Optional[dict]:
    """Loads the agent state and conversation history from a JSON file."""
    file_path = os.path.join(STATE_DIR, f"{thread_id}.json")
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading thread state {thread_id}: {e}")
        return None

def get_state_from_data(data: dict) -> AgentState:
    """Reconstructs AgentState dataclass from saved dictionary."""
    s_dict = data["state"]
    return AgentState(
        user_id=s_dict.get("user_id", ""),
        current_time=s_dict.get("current_time", ""),
        task_type=s_dict.get("task_type", ""),
        tasks=s_dict.get("tasks", []),
        time_zone=s_dict.get("time_zone", "UTC"),
        relevant_preferences=s_dict.get("relevant_preferences"),
        similar_conversations=s_dict.get("similar_conversations"),
        scheduling_patterns=s_dict.get("scheduling_patterns"),
        messages=[] # History is handled separately
    )
