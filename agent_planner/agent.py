from utils.nodes import model,human_feedback,should_continue,get_current_time
from utils.state import AgentState
from langchain_core.messages import HumanMessage,ToolMessage
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode
from utils import tools
from langgraph.checkpoint.memory import MemorySaver


agent = StateGraph(AgentState)

tool_node = ToolNode(tools)

agent.add_node("current_time",get_current_time)
agent.add_node("model",model)
agent.add_node("tool",tool_node)
agent.add_node("human_feedback",human_feedback)

agent.set_entry_point("current_time")
agent.add_edge("current_time","model")

agent.add_conditional_edges("model",should_continue)
agent.add_edge("human_feedback","model")
agent.add_edge("tool",END)

memory = MemorySaver()

app = agent.compile(interrupt_before=["human_feedback"],checkpointer=memory)


thread = {"configurable": {"thread_id": "1"}}

initial_input = {"messages":[HumanMessage(content="remind me to buy gocessaries tomorrow morning")]}
# Run the graph until the first interruption
for event in app.stream(initial_input, thread, stream_mode="values"):
    event['messages'][-1].pretty_print()

#%%
print(type(event["messages"][-1]))

if not isinstance(event["messages"][-1],ToolMessage):
    user_input = input("tell the time:")

    app.update_state(thread, {"messages": user_input}, as_node="human_feedback")
    for event in app.stream(None, thread, stream_mode="values"):
        event["messages"][-1].pretty_print()
print("done")
