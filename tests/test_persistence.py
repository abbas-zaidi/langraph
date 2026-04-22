import pytest
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from app.agents.persistent_agent import Agent
from app.llm.deepseek_client import DeepSeekClient

@pytest.mark.skip(reason="This feature is not implemented yet")
def test_persistent_agent():
    tool = TavilySearchResults(max_results=4) #increased number of results
    prompt = """You are a smart research assistant. Use the search engine to look up information. \
        You are allowed to make multiple calls (either together or in sequence). \
        Only look up information when you are sure of what you want. \
        If you need to look up some information before asking a follow up question, you are allowed to do that!
        """
    
    with SqliteSaver.from_conn_string("checkpoints.sqlite") as memory:
        # Compile your graph with the checkpointer
        
        model = DeepSeekClient().get_model()
        abot = Agent(model, [tool], system=prompt,checkpointer=memory)
        messages = HumanMessage(content="Who won the super bowl in 2024? In what state is the winning team headquarters located? \
        What is the GDP of that state? Answer each question.")
    
        thread = {"configurable":{"thread_id":"1"}}
        abot.run(messages,thread)

@pytest.mark.asyncio
async def test_persistent_agent_async():
    tool = TavilySearchResults(max_results=4) #increased number of results
    prompt = """You are a smart research assistant. Use the search engine to look up information. \
        You are allowed to make multiple calls (either together or in sequence). \
        Only look up information when you are sure of what you want. \
        If you need to look up some information before asking a follow up question, you are allowed to do that!
        """
    
    async with AsyncSqliteSaver.from_conn_string("checkpoints.sqlite") as memory:
        # Compile your graph with the checkpointer
        
        model = DeepSeekClient().get_model()
        abot = Agent(model, [tool], system=prompt,checkpointer=memory)
        messages = HumanMessage(content="what is the weather in SFO")
    
        thread = {"configurable":{"thread_id":"1"}}
        await abot.run_async(messages,thread)