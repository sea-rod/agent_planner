import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent import app  # replace with your actual import


thread = {"configurable": {"thread_id": "1"}}


def chat_with_agent(user_input, history):
    # Add user message to history
    history = history + [(user_input, None)]

    initial_input = {"messages": [HumanMessage(content=user_input)]}
    final_output = ""
    event_data = None

    # Stream LLM output
    for event in app.stream(initial_input, thread, stream_mode="values"):
        msg = event["messages"][-1]
        if isinstance(msg, AIMessage):
            final_output = msg.content
        event_data = event

    # Handle reminder flow
    if (
        isinstance(event_data["messages"][-1], AIMessage)
        and not isinstance(event_data["messages"][-2], ToolMessage)
        and event_data.get("task_type") == "reminder"
    ):
        bot_reply = final_output + "\n\n⏰ Please specify the time for the reminder."
        history[-1] = (user_input, bot_reply)
        return history, history

    # Handle planner flow
    elif (
        isinstance(event_data["messages"][-1], AIMessage)
        and not isinstance(event_data["messages"][-2], ToolMessage)
        and event_data.get("task_type") == "planner"
    ):
        bot_reply = final_output + "\n\n📅 Can you confirm or adjust your plan?"
        history[-1] = (user_input, bot_reply)
        return history, history
        
    # Handle delete flow
    elif (
        isinstance(event_data["messages"][-1], AIMessage)
        and not isinstance(event_data["messages"][-2], ToolMessage)
        and event_data.get("task_type") == "delete"
    ):
        bot_reply = final_output + "\n\n🗑️ Can you confirm which events to delete?"
        history[-1] = (user_input, bot_reply)
        return history, history

    # Default AI response
    bot_reply = final_output or "✅ Done!"
    history[-1] = (user_input, bot_reply)
    return history, history


# Optional: handle follow-up
def handle_follow_up(user_input, history, task_type):
    if task_type == "reminder":
        app.update_state(thread, {"messages": user_input}, as_node="human_feedback_reminder")
    elif task_type == "planner":
        app.update_state(thread, {"messages": user_input}, as_node="human_feedback_planner")
    elif task_type == "delete":
        app.update_state(thread, {"messages": user_input}, as_node="human_feedback_delete")

    final_output = ""
    for event in app.stream(None, thread, stream_mode="values"):
        msg = event["messages"][-1]
        if isinstance(msg, AIMessage):
            final_output = msg.content

    history = history + [(user_input, final_output)]
    return history, history


# Gradio Interface
with gr.Blocks(title="AI Planner & Reminder") as demo:
    gr.Markdown("# 🧠 AI Planner & Reminder Assistant\nChat with your AI agent below:")

    chat = gr.Chatbot(label="Conversation")
    user_input = gr.Textbox(label="Type your message...")
    send_btn = gr.Button("Send")

    send_btn.click(chat_with_agent, [user_input, chat], [chat, chat])

demo.launch()
