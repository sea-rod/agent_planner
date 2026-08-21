# utils/memory_nodes.py - Memory retrieval and storage nodes with lazy init

from .state import AgentState
from langchain_core.messages import HumanMessage, AIMessage
import time

# Lazy initialization - don't create connection until first use
_memory_store = None


def get_memory_store():
    """Lazy initialization of memory store."""
    global _memory_store
    if _memory_store is None:
        try:
            from agent_planner.utils.pinecone_memory import PineconeMemoryStore
            _memory_store = PineconeMemoryStore()
        except Exception as e:
            _memory_store = False  # Mark as failed to avoid retrying
    return _memory_store if _memory_store is not False else None


def retrieve_semantic_memory(state: AgentState) -> AgentState:
    """Retrieve relevant memories from Weaviate before processing."""
    store = get_memory_store()
    if store is None:
        return state

    user_id = state.user_id if hasattr(state, 'user_id') else "default_user"
    messages = state.messages

    # Build query from recent user messages
    recent_context = ""
    for msg in reversed(messages[-3:]):
        if isinstance(msg, HumanMessage) and hasattr(msg, "content"):
            recent_context = msg.content + " " + recent_context
        elif isinstance(msg, str):
            recent_context = msg + " " + recent_context
    recent_context = recent_context.strip()

    if not recent_context:
        return state

    try:
        preferences    = store.get_relevant_preferences(user_id=user_id, query=recent_context, limit=3)
        similar_convos = store.retrieve_similar_conversations(user_id=user_id, current_context=recent_context, limit=2)
        patterns       = store.find_similar_patterns(user_id=user_id, task_description=recent_context, limit=3)

        state.relevant_preferences = preferences
        state.similar_conversations = similar_convos
        state.scheduling_patterns = patterns
        print(f"Node retrieve_semantic_memory returned: {state}")
        return state

    except Exception as e:
        return state  # degrade gracefully — don't break the graph


def store_interaction_memory(state: AgentState) -> AgentState:
    """Store completed interaction in Weaviate for future learning."""
    store = get_memory_store()
    if store is None:
        return state

    user_id   = state.user_id if hasattr(state, 'user_id') else "default_user"
    thread_id = state.thread_id if hasattr(state, 'thread_id') else "default_thread"
    messages  = state.messages
    task_type = state.task_type if hasattr(state, 'task_type') else "unknown"

    try:
        # Find last user and assistant messages
        user_msg      = None
        assistant_msg = None

        for msg in reversed(messages):
            content = msg.content if hasattr(msg, 'content') else msg
            if isinstance(msg, HumanMessage) or (isinstance(msg, dict) and msg.get('role') == 'user'):
                if user_msg is None:
                    user_msg = content
            elif isinstance(msg, AIMessage) or (isinstance(msg, dict) and msg.get('role') == 'assistant'):
                if assistant_msg is None:
                    assistant_msg = content
            if user_msg and assistant_msg:
                break

        if not (user_msg and assistant_msg):
            return state

        store.store_conversation_turn(
            user_id=user_id,
            thread_id=thread_id,
            user_message=user_msg,
            assistant_response=assistant_msg,
            task_type=task_type,
            successful=True,
        )

        # Store per-task scheduling patterns
        tasks = state.tasks or []
        failed_patterns = 0

        for task in tasks:
            summary    = task.get("summary", "Untitled Task")
            start_time = task.get("start", "")
            if isinstance(start_time, dict):
                start_time = start_time.get("dateTime", "")
            start_time_str = str(start_time) if start_time else "unspecified time"

            pattern_desc = f"User scheduled '{summary}' at {start_time_str}"

            try:
                store.store_scheduling_pattern(
                    user_id=user_id,
                    pattern_description=pattern_desc,
                    task_type=task_type,
                    task_data=task,
                )
            except Exception as e:
                failed_patterns += 1

        print(f"Node store_interaction_memory returned: {state}")
        return state

    except Exception as e:
        return state  # degrade gracefully


def get_memory_store_for_cleanup():
    """Get memory store instance for cleanup."""
    return _memory_store if isinstance(_memory_store, object) else None