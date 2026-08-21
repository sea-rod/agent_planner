import gradio as gr
from agent import run_pipeline
import uuid
import signal
import sys
import atexit

# Import for cleanup
from utils.memory_node import get_memory_store_for_cleanup

def get_user_session(user_id: str = None):
    """Generate or retrieve user session"""
    if user_id is None:
        user_id = str(uuid.uuid4())[:8]
    return {"user_id": user_id}, user_id


def chat_with_agent(user_input, history, session_state=None):
    """Enhanced chat function with memory tracking"""

    # Initialize or retrieve session
    if session_state is None:
        session_info, user_id = get_user_session()
        session_state = session_info
    else:
        user_id = session_state["user_id"]

    # Convert Gradio history [(user, bot), ...] to list of dicts for the pipeline
    pipeline_history = []
    for user_msg, bot_msg in history:
        pipeline_history.append({"role": "user", "content": user_msg})
        if bot_msg:
            pipeline_history.append({"role": "assistant", "content": bot_msg})

    try:
        # Execute the pipeline
        result = run_pipeline(
            user_id=user_id,
            user_message=user_input,
            history=pipeline_history
        )

        if result["status"] == "planning":
            bot_reply = result["response"]
            history.append((user_input, bot_reply))
        else:
            # If completed, summarize results into a response
            summary = "Plan executed successfully:\n"
            for item in result["results"]:
                res = item["result"]
                if isinstance(res, dict) and "error" in res:
                    summary += f"- {item['step']}: ❌ {res['error']}\n"
                else:
                    summary += f"- {item['step']}: ✓ Success\n"

            # If the planner had a final response, we could use it, but usually, we summary the tool results
            bot_reply = summary

            history.append((user_input, bot_reply))

        return history, history, session_state

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append((user_input, error_msg))
        return history, history, session_state


# ============ CLEANUP HANDLERS ============


def cleanup_resources():
    """Clean up Weaviate connection and other resources"""
    ("\n🧹 Cleaning up resources...")
    try:
        store = get_memory_store_for_cleanup()
        if store is not None:
            store.close()
            ("✓ Weaviate connection closed")
    except Exception as e:
        (f"⚠ Cleanup warning: {e}")


def signal_handler(sig, frame):
    """Handle Ctrl+C and other termination signals"""
    ("\n\n⚠ Shutdown signal received...")
    cleanup_resources()
    sys.exit(0)


# Register cleanup handlers
atexit.register(cleanup_resources)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# ============ GRADIO INTERFACE ============

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 AI Agent Planner with Memory")
    gr.Markdown("Your intelligent scheduling assistant with semantic memory")

    # FIXED: Remove type='messages' to use default tuple format
    chatbot = gr.Chatbot(label="Conversation")

    msg = gr.Textbox(
        label="Your message", placeholder="Schedule a meeting tomorrow at 10 AM"
    )
    session_state = gr.State()

    msg.submit(
        chat_with_agent,
        [msg, chatbot, session_state],
        [chatbot, chatbot, session_state],
    )

    clear = gr.Button("Clear Conversation")
    clear.click(lambda: ([], None), None, [chatbot, session_state])

    gr.Examples(
        examples=[
            "Schedule a team meeting tomorrow at 10 AM",
            "Plan my day with 3 hours of focused work",
            "What events do I have this week?",
            "Delete my meeting on Monday",
        ],
        inputs=msg,
    )

if __name__ == "__main__":
    try:
        ("🚀 Starting AI Agent Planner...")
        demo.launch()
    except KeyboardInterrupt:
        ("\n⚠ Keyboard interrupt detected")
    finally:
        cleanup_resources()
