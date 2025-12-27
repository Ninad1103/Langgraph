from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_community.llms import Ollama
from typing import TypedDict, List

class AgentState(TypedDict):
    messages : List[HumanMessage]

llm = Ollama(model="llama3.2:3b")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    print(f"\n AI: {response}")
    return state

#create the flow
graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
app = graph.compile()

#run the app
while True:
    user_input = input("\n You: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break
    app.invoke({"messages": [HumanMessage(content=user_input)]})    
    

