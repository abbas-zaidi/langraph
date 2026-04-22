import asyncio
from langchain_core.messages import HumanMessage
from app.graph.builder import build_agent_graph
from typing import Optional


class Agent:
    def __init__(self, model, tools, system="",checkpointer=None):
        self.graph = build_agent_graph(model, tools, system,checkpointer)

    def run(self, user_input: HumanMessage, thread=None):
        for event in self.graph.stream({"messages":[user_input]},thread):
            for v in event.values():
                print(v['messages'])
    
    async def run_async(self, user_input: HumanMessage, thread: Optional[dict] = None):
        try:
            async with asyncio.timeout(30.0):  # Timeout wrapper for async block
                async for event in self.graph.astream_events(
                    {"messages": [user_input]}, 
                    thread, 
                    version="v1"
                ):
                    kind = event["event"]
                    if kind == "on_chat_model_stream":
                        content = event["data"]["chunk"].content
                        if content:
                            print(content, end="|")
        except asyncio.TimeoutError:
            print("\nStream timed out after 30 seconds")