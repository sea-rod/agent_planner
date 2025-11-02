# %%
from utils.nodes import (
    model,
    human_feedback,
    should_continue,
    get_current_time,
    classify_model,
    route_classifier,
    get_events_node,
    model_schedule,
    model_add,
)
from utils.state import AgentState
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from utils import tools
from langgraph.checkpoint.memory import MemorySaver


agent = StateGraph(AgentState)

tool_node = ToolNode(tools)

agent.add_node("current_time", get_current_time)
agent.add_node("model", model)
agent.add_node("refine_model", model)
agent.add_node("get_event", get_events_node)
agent.add_node("scheduler", model_schedule)
agent.add_node("classify_model", classify_model)
agent.add_node("tool", tool_node)
agent.add_node("human_feedback_reminder", human_feedback)
agent.add_node("human_feedback_planner", human_feedback)
agent.add_node("model_add", model_add)



agent.set_entry_point("current_time")
agent.add_edge("current_time", "get_event")
agent.add_edge("get_event","classify_model")
agent.add_conditional_edges(
    "classify_model", route_classifier, {"planner": "scheduler", "reminder": "model"}
)

agent.add_conditional_edges(
    "model",
    should_continue,
    {"tool": "tool", "human_feedback": "human_feedback_reminder"},
)
agent.add_edge("human_feedback_reminder", "model")
agent.add_edge("tool", "refine_model")
agent.add_edge("refine_model", END)
agent.add_edge("scheduler","model_add")
agent.add_conditional_edges(
    "scheduler",
    should_continue,
    {"tool": "model_add", "human_feedback": "human_feedback_planner"},
)
agent.add_edge("human_feedback_planner", "scheduler")
agent.add_edge("model_add","tool")


memory = MemorySaver()

app = agent.compile(
    interrupt_before=["human_feedback_reminder", "human_feedback_planner"],
    checkpointer=memory,
)
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))
# %%

thread = {"configurable": {"thread_id": "1"}}
input_ = input("Enter prompt:")

initial_input = {"messages": [HumanMessage(content=input_)]}
for event in app.stream(initial_input, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()
print("hellloo donkwy:", event.get("task_type"))
while (
    isinstance(event["messages"][-1], AIMessage)
    and not isinstance(event["messages"][-2], ToolMessage)
    and event.get("task_type") == "reminder"
):
    user_input = input("tell the time:")
    app.update_state(
        thread, {"messages": user_input}, as_node="human_feedback_reminder"
    )
    for event in app.stream(None, thread, stream_mode="values"):
        event["messages"][-1].pretty_print()

while (
    isinstance(event["messages"][-1], AIMessage)
    and not isinstance(event["messages"][-2], ToolMessage)
    and event.get("task_type") == "planner"
):
    user_input = input("user:")
    app.update_state(thread, {"messages": user_input}, as_node="human_feedback_planner")
    for event in app.stream(None, thread, stream_mode="values"):
        event["messages"][-1].pretty_print()

print("done")
