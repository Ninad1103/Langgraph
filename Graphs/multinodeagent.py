from typing import Dict, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict): #state schema
    name : str
    age: int
    skills: str
    result: str

def first_node(state: AgentState) -> AgentState:
    """
    A simple node that returns a greeting message.
    """    
    state['result'] = state['name'] + ", welcome!"
    return state

def second_node(state: AgentState) -> AgentState:
    """
    Appends age to result
    """    
    state['result'] = state['result'] + ", you are " + str(state['age']) + " years old!"
    return state

def third_node(state: AgentState) -> AgentState:
    """
    Appends skills to result
    """    
    state['result'] = state['result'] + ", your skills are " + state['skills']
    return state

graph = StateGraph(AgentState)
graph.add_node("first", first_node)
graph.add_edge("first", "second")
graph.add_node("second", second_node)
graph.add_edge("second", "third")
graph.add_node("third", third_node)
graph.set_entry_point("first")
graph.set_finish_point("third")

agent = graph.compile()

result = agent.invoke({"name": "Ninad", "age": 25, "skills": "Python, Langgraph"})

print(result["result"])
