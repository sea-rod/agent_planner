# utils/memory_nodes.py - Memory retrieval and storage nodes with lazy init

from .state import AgentState
from langchain_core.messages import HumanMessage, AIMessage
import time
import structlog

log = structlog.get_logger("atelier.memory.nodes")

# Lazy initialization - don't create connection until first use
_memory_store = None


def get_memory_store():
    """Lazy initialization of memory store."""
    global _memory_store
    if _memory_store is None:
        log.info("memory_store_initializing")
        try:
            from utils.weaviate_memory import WeaviateMemoryStore
            _memory_store = WeaviateMemoryStore()
            log.info("memory_store_initialized")
        except Exception as e:
            log.error("memory_store_init_failed", error=str(e), exc_info=True)
            _memory_store = False  # Mark as failed to avoid retrying
    return _memory_store if _memory_store is not False else None


def retrieve_semantic_memory(state: AgentState) -> AgentState:
    """Retrieve relevant memories from Weaviate before processing."""
    t0 = time.perf_counter()

    store = get_memory_store()
    if store is None:
        log.warning("memory_store_unavailable", node="retrieve_semantic_memory")
        return state

    user_id = state.get("user_id", "default_user")
    messages = state["messages"]

    # Build query from recent user messages
    recent_context = ""
    for msg in reversed(messages[-3:]):
        if isinstance(msg, HumanMessage) and hasattr(msg, "content"):
            recent_context = msg.content + " " + recent_context
    recent_context = recent_context.strip()

    if not recent_context:
        log.debug("memory_retrieval_skipped", reason="no_recent_context", user_id=user_id)
        return state

    try:
        preferences    = store.get_relevant_preferences(user_id=user_id, query=recent_context, limit=3)
        similar_convos = store.retrieve_similar_conversations(user_id=user_id, current_context=recent_context, limit=2)
        patterns       = store.find_similar_patterns(user_id=user_id, task_description=recent_context, limit=3)

        log.info(
            "memory_retrieved",
            user_id=user_id,
            preferences_count=len(preferences),
            conversations_count=len(similar_convos),
            patterns_count=len(patterns),
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
        )

        return {
            **state,
            "relevant_preferences":  preferences,
            "similar_conversations": similar_convos,
            "scheduling_patterns":   patterns,
        }

    except Exception as e:
        log.error(
            "memory_retrieval_failed",
            user_id=user_id,
            error=str(e),
            exc_info=True,
        )
        return state  # degrade gracefully — don't break the graph


def store_interaction_memory(state: AgentState) -> AgentState:
    """Store completed interaction in Weaviate for future learning."""
    t0 = time.perf_counter()

    store = get_memory_store()
    if store is None:
        log.warning("memory_store_unavailable", node="store_interaction_memory")
        return state

    user_id   = state.get("user_id", "default_user")
    thread_id = state.get("thread_id", "default_thread")
    messages  = state["messages"]
    task_type = state.get("task_type", "unknown")

    try:
        # Find last user and assistant messages
        user_msg      = None
        assistant_msg = None

        for msg in reversed(messages):
            if isinstance(msg, HumanMessage) and user_msg is None:
                user_msg = msg.content
            elif isinstance(msg, AIMessage) and assistant_msg is None:
                assistant_msg = msg.content
            if user_msg and assistant_msg:
                break

        if not (user_msg and assistant_msg):
            log.warning(
                "memory_store_skipped",
                reason="missing_user_or_assistant_message",
                user_id=user_id,
                thread_id=thread_id,
            )
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
        tasks = state.get("tasks", [])
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
                log.error(
                    "scheduling_pattern_store_failed",
                    user_id=user_id,
                    task_summary=summary,
                    error=str(e),
                )

        log.info(
            "interaction_memory_stored",
            user_id=user_id,
            thread_id=thread_id,
            task_type=task_type,
            patterns_stored=len(tasks) - failed_patterns,
            patterns_failed=failed_patterns,
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
        )

        return state

    except Exception as e:
        log.error(
            "store_interaction_memory_failed",
            user_id=user_id,
            thread_id=thread_id,
            error=str(e),
            exc_info=True,
        )
        return state  # degrade gracefully


def get_memory_store_for_cleanup():
    """Get memory store instance for cleanup."""
    return _memory_store if isinstance(_memory_store, object) else None