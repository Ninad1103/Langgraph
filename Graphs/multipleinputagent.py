from typing import Dict, TypedDict
from langgraph.graph import StateGraph
from math import prod

class AgentState(TypedDict): #state schema
    name : str
    values: list
    operation : str
    result : str


def operation_node(state: AgentState) -> AgentState:
    """
    A simple node that processes multiple inputs
    """    
    if state['operation'] == "+":
        state['result'] = f"Hi {state['name']}, your answer is {sum(state['values'])}"
    elif state['operation'] == "*":
        state['result'] = f"Hi {state['name']}, your answer is {prod(state['values'])}"
    return state    

graph = StateGraph(AgentState)
graph.add_node("operation", operation_node)
graph.set_entry_point("operation")
graph.set_finish_point("operation")

agent = graph.compile()

result = agent.invoke({"name": "Ninad", "values": [1, 2, 3, 4], "operation": "*"})

print(result["result"])