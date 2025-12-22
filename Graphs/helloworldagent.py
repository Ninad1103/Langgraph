from typing import Dict, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict): #state schema
    message : str

def greeting_node(state: AgentState) -> AgentState:
    """
    A simple node that returns a greeting message.
    """    
    state['message'] = state['message'] + ", good job learning LangGraph!"
    return state
    
graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.set_entry_point("greeting")

agent = graph.compile()

result = agent.invoke({"message": "Ninad"})

print(result["message"])