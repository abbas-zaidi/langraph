from app.llm.deepseek_client import DeepSeekClient
from langchain_core.messages import SystemMessage, ToolMessage

llm = DeepSeekClient()

def input_node(state):
    return {
        "messages": [{"role": "user", "content": state["input"]}]
    }

def llm_node(state):
    response = llm.chat(state["messages"])
    
    return {
        "messages": state["messages"] + [
            {"role": "assistant", "content": response}
        ],
        "output": response
    }

# app/graph/nodes.py



def call_model(state, model, system):
    messages = state["messages"]

    if system:
        messages = [SystemMessage(content=system)] + messages

    response = model.invoke(messages)

    return {"messages": [response]}


def exists_action(state):
    last = state["messages"][-1]
    return len(getattr(last, "tool_calls", [])) > 0


def take_action(state, tools):
    tool_calls = state["messages"][-1].tool_calls
    results = []

    for t in tool_calls:
        if t["name"] not in tools:
            result = "bad tool name, retry"
        else:
            result = tools[t["name"]].invoke(t["args"])

        results.append(
            ToolMessage(
                tool_call_id=t["id"],
                name=t["name"],
                content=str(result),
            )
        )

    return {"messages": results}