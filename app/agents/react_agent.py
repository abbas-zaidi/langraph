from langchain_core.messages import HumanMessage
from app.graph.builder import build_agent_graph


class Agent:
    def __init__(self, model, tools, system=""):
        self.graph = build_agent_graph(model, tools, system)

    def run(self, user_input: HumanMessage):
        result = self.graph.invoke({
            "messages": [user_input]
        })
        return result["messages"][-1].content