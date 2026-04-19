from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.graph.builder import build_graph
from app.agents.react_agent import Agent
from app.config import settings

from langchain_community.tools.tavily_search import TavilySearchResults

# def test_graph():
#     app = build_graph()

#     result = app.invoke({
#         "input": "What is AI?"
#     })
#     print(result["output"])
#     assert "AI" in result["output"]

def test_react_agent():
    tool = TavilySearchResults(max_results=4) #increased number of results
    prompt = """You are a smart research assistant. Use the search engine to look up information. \
        You are allowed to make multiple calls (either together or in sequence). \
        Only look up information when you are sure of what you want. \
        If you need to look up some information before asking a follow up question, you are allowed to do that!
        """
    
    model = ChatOpenAI(
        model="deepseek-chat",  # or "deepseek-reasoner"
        openai_api_key= settings.DEEPSEEK_API_KEY,  # or set DEEPSEEK_API_KEY env var
        openai_api_base="https://api.deepseek.com/v1",  # DeepSeek's OpenAI-compatible endpoint
        temperature=0.7,
        max_tokens=1000,
    )
    abot = Agent(model, [tool], system=prompt)
    messages = HumanMessage(content="Who won the super bowl in 2024? In what state is the winning team headquarters located? \
        What is the GDP of that state? Answer each question.")
    

    result = abot.run(messages)
    print(result)
