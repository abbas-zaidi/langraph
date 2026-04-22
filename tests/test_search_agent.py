from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from app.agents.react_agent import Agent
from app.llm.deepseek_client import DeepSeekClient

def test_react_agent():
    tool = TavilySearchResults(max_results=4) #increased number of results
    prompt = """You are a smart research assistant. Use the search engine to look up information. \
        You are allowed to make multiple calls (either together or in sequence). \
        Only look up information when you are sure of what you want. \
        If you need to look up some information before asking a follow up question, you are allowed to do that!
        """
    
    model = DeepSeekClient().get_model()
    abot = Agent(model, [tool], system=prompt)
    messages = HumanMessage(content="Who won the super bowl in 2024? In what state is the winning team headquarters located? \
        What is the GDP of that state? Answer each question.")
    

    result = abot.run(messages)
    print(result)