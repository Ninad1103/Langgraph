from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
#Using ChatOllama so that we can bind tools

#Annotated : Provides additional context without affecting the type
#BaseMessage : Base class for all message types
#ToolMessage : Passes data back to LLM after it calls a tool such as the content
#SystemMessage : System messages are used to set the instructions for the LLM
#Sequence : To automatically add messages to the state
#add_message : Reducer function
    #Rule that controls how updates from nodes are combined with existing state
    #Tells how to merge data into current state
    #Without reducer, updates would have replaced the existing value entirely

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool
def add_two_numbers(a: int, b: int) -> int:
    """
    Addition function that adds two numbers
    """
    return a + b

@tool
def multiply_two_numbers(a: int, b: int) -> int:
    """
    Multiplication function that multiplies two numbers
    """
    return a * b

tools = [add_two_numbers, multiply_two_numbers]

model = ChatOllama(model="llama3.2:3b").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are a helpful assistant who answers questions about math")
    response = model.invoke([system_prompt] + state['messages'])
    return {"messages": [response]}


def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "continue"
    else:
        return END

graph = StateGraph(AgentState)
graph.add_node("agent", model_call)
graph.add_edge(START, "agent")


tool_node = ToolNode(tools)
graph.add_node("tool_node", tool_node)

graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tool_node",
        END: END
    }
)

graph.add_edge("tool_node", "agent")

app = graph.compile()

inputs = {"messages": [("user", "What is 2 + 2? Multiply the answer by 7." )]}

response = app.invoke(inputs)

final_message = response['messages'][-1]
print(f"\nAI: {final_message.content}")
