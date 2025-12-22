from langgraph.graph import StateGraph, START, END
import random
from typing import TypedDict, Dict, List

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int

def greeting_node(state: AgentState) -> AgentState:
    """
    Greet the user
    """
    state['name'] = f"Hi there, {state['name']}"
    state['counter'] = 0 #reset counter
    return state    

def random_node(state: AgentState) -> AgentState:
    """
    Generate a random number from 0 to 10
    """
    state['number'].append(random.randint(1, 10))
    state['counter'] += 1
    return state

def should_countinue(state: AgentState) -> AgentState:
    """
    Decide whether to continue the loop
    """
    if state['counter'] < 5:
        print("Entering Loop", state['counter'])
        return "loop" #We return the name of the edge
    else:
        print("Exiting Loop", state['counter'])
        return "end" #We return the name of the edge

graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random")
graph.add_conditional_edges(
    "random", #source node
    should_countinue, #action
    {"loop": "random", "end": END}  #edges
    )


agent = graph.compile()

result = agent.invoke({"name": "Ninad", "number": [], "counter": -1})

print(result["number"])
