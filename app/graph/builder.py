from langgraph.graph import StateGraph, END
from app.graph.state import AgentState,GraphState
from app.graph.nodes import input_node, llm_node
from app.graph.nodes import call_model, take_action, exists_action


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("input", input_node)
    graph.add_node("llm", llm_node)

    graph.set_entry_point("input")

    graph.add_edge("input", "llm")
    graph.add_edge("llm", END)

    return graph.compile()



def build_agent_graph(model, tools, system=""):
    graph = StateGraph(AgentState)

    tool_map = {t.name: t for t in tools}
    model = model.bind_tools(tools)

    graph.add_node("llm", lambda s: call_model(s, model, system))
    graph.add_node("action", lambda s: take_action(s, tool_map))

    graph.add_conditional_edges(
        "llm",
        exists_action,
        {True: "action", False: END},
    )

    graph.add_edge("action", "llm")
    graph.set_entry_point("llm")

    return graph.compile()
