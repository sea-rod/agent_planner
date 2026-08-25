from typing import List, Optional
from utils.state import AgentState
from utils.persistence import load_thread_state, save_thread_state, get_state_from_data
from utils.nodes import (
    get_current_time,
    fetch_calendar_events,
    scheduling_chat_turn,
    extract_steps,
    classify_steps,
    node_add,
    node_remove,
    node_get_events,
    node_time_blocking,
)
from utils.memory_node import retrieve_semantic_memory, store_interaction_memory

def run_pipeline(user_id: str, user_message: str, history: List[dict], state: Optional[AgentState] = None):
    """
    Main entry point for the scheduling agent pipeline.
    Replaces the LangGraph state machine with a vanilla Python flow.
    """
    if state is None:
        state = AgentState(
            user_id=user_id,
            messages=history,
            time_zone="Asia/Kolkata" # Default, should be handled by user preferences
        )
    else:
        state.messages = history

    # 1. Retrieve Memory
    state = retrieve_semantic_memory(state)

    # 2. Setup Context
    state = get_current_time(state)

    # Add current user message to state for parameter extraction
    state.messages.append({"role": "user", "content": user_message})

    state = fetch_calendar_events(state)

    # 3. Planner (Human-in-the-loop stage)
    # The planner is a pure chat loop. It only moves to execution once the user confirms.
    updated_history = scheduling_chat_turn(
        existing_events=state.tasks,
        history=list(history),
        user_message=user_message
    )

    # Confirmation heuristic
    print("\n\n\n\n updated history",updated_history[-1])
    # confirmation_keywords = ["yes", "confirm","CONFRIM", "proceed", "looks good", "do it", "correct"]
    # is_confirmed = any(kw in updated_history[-1]["content"] for kw in confirmation_keywords)

    if not updated_history[-1]["content"]=="CONFIRM":
        return {
            "status": "planning",
            "response": updated_history[-1]["content"],
            "history": updated_history,
            "state": state
        }

    # 4. Execution Phase (once confirmed)

    # a. Extract discrete action steps from the confirmed chat history
    steps = extract_steps(updated_history)

    # b. Classify each step
    classified_steps = classify_steps(steps)

    # c. Dispatch loop
    results = []
    for item in classified_steps:
        step_text = item["step"]
        label = item["label"]

        if label == "add":
            res = node_add(step_text, state)
        elif label == "delete":
            res = node_remove(step_text, state)
        elif label == "get_events":
            res = node_get_events(step_text, state)
        elif label == "time_block":
            res = node_time_blocking(step_text, state)
        else:
            res = {"error": f"Unknown action label: {label}"}

        results.append({"step": step_text, "result": res})

    # 5. Store Memory
    state.tasks = []
    for r in results:
        if isinstance(r["result"], list):
            state.tasks.extend(r["result"])
        elif isinstance(r["result"], dict) and "event" in r["result"]:
            state.tasks.append(r["result"]["event"])

    state.messages = updated_history
    store_interaction_memory(state)

    return {
        "status": "completed",
        "results": results,
        "history": updated_history,
        "state": state
    }

if __name__ == "__main__":
    # Simple CLI loop for testing the pipeline with resumption
    user_id = "test_user_123"
    thread_id = "test_thread_456"

    # Resume from disk if available
    thread_data = load_thread_state(thread_id)
    if thread_data:
        print(f"Resuming thread {thread_id}...")
        history = thread_data["history"]
        state = get_state_from_data(thread_data)
    else:
        print(f"Starting fresh thread {thread_id}...")
        history = []
        state = None

    print("--- AI Planner CLI Test Loop ---")
    print("Type 'exit' or 'quit' to stop.")
    print("Say 'yes' or 'confirm' to execute a plan.")
    print("-------------------------------")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            result = run_pipeline(
                user_id=user_id,
                user_message=user_input,
                history=history,
                state=state
            )

            history = result["history"]
            state = result["state"]

            # Save state after every turn
            save_thread_state(thread_id, state, history)

            if result["status"] == "planning":
                print(f"\nAgent: {result['response']}")
            else:
                print("\n--- Execution Results ---")
                for item in result["results"]:
                    res = item["result"]
                    status = "✓" if not (isinstance(res, dict) and "error" in res) else "❌"
                    print(f"{status} {item['step']} -> {res}")
                print("-------------------------")
                print("\nAgent: I have executed the requested changes to your calendar.")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
