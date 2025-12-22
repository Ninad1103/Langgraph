from typing import Dict, TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict): #state schema
    number1 : int
    operation : str
    number2: int
    result: int

def addition_node(state: AgentState) -> AgentState:
    """
    Addition node
    """    
    state['result'] = state['number1'] + state['number2']
    return state

def subtraction_node(state: AgentState) -> AgentState:
    """
    Subtraction node
    """    
    state['result'] = state['number1'] - state['number2']
    return state

def decide_next_node(state: AgentState) -> AgentState:
    """
    Acts as a router
    """    
    if state['operation'] == "+":
        return "additionoperation" #this is the name of the edge
    elif state['operation'] == "-":
        return "subtractionoperation"


graph = StateGraph(AgentState)
graph.add_node("addition", addition_node)
graph.add_node("subtraction", subtraction_node)
graph.add_node("router", lambda state:state) #pass through function

graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router",
    decide_next_node, # {edge -> node}
    {"additionoperation": "addition", "subtractionoperation": "subtraction"}
)
graph.add_edge("addition", END)
graph.add_edge("subtraction", END)

agent = graph.compile()

result = agent.invoke({"number1": 1, "operation": "-", "number2": 2})

print(result["result"])