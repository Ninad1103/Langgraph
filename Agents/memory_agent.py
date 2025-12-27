from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    messages : List[Union[HumanMessage, AIMessage, SystemMessage]]

llm = Ollama(model="llama3.2:3b")

#Add the AI response to the state as well
def process(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    state['messages'].append(SystemMessage(content="You are a helpful assistant."))
    state['messages'].append(AIMessage(content=response))
    print(f"\n AI: {response}")
    return state

#create workflow
graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
app = graph.compile()

conversation_history = []

while True:
    user_input = input("\n You: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break
    conversation_history.append(HumanMessage(content=user_input))
    result = app.invoke({"messages": conversation_history})
    conversation_history = result['messages']