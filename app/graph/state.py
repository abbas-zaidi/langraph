from typing import TypedDict, List, Annotated
from langchain_core.messages import AnyMessage
import operator

class GraphState(TypedDict):
    input: str
    messages: Annotated[List[AnyMessage],operator.add]
    output: str

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage],operator.add]