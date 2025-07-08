from langgraph.graph import StateGraph, START, END
import os
# from google.colab import userdata

import requests
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition


from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from IPython.display import Image,display
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

from langchain_google_genai import ChatGoogleGenerativeAI
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)


class State(TypedDict):
    messages: Annotated[list, add_messages]



from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool

search_tool = Tool(
    name="duckduckgo_search",
    func=DuckDuckGoSearchRun().run,
    description="Search the web using DuckDuckGo. Useful for questions about current events, weather, or general knowledge."
)

def multiply(a:int,b:int) -> int:
    """
    Multiply a and b
    """
    return a* b

def add(a:int,b:int) -> int:
    """
    Adds a and b
    """
    return a + b


tools=[search_tool, add, multiply]
llm_with_tools=llm.bind_tools(tools)
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}




graph_builder=StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tools",ToolNode(tools))
graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",tools_condition)
graph_builder.add_edge("tools","chatbot")
graph_builder.add_edge("chatbot",END)
graph=graph_builder.compile()






























if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            response = graph.invoke({"messages": [HumanMessage(content=user_input)]})
            for m in response['messages']:
                m.pretty_print()
        except Exception as e:
            print(f"An error occurred: {e}")
            break