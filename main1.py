from langgraph.graph import StateGraph, START, END
import os
# from google.colab import userdata

import requests
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition



from langchain.chains import create_sql_query_chain
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from langchain_community.utilities import SQLDatabase


import streamlit as st


from langchain_core.messages import AIMessage, ToolMessage

from langgraph.checkpoint.memory import InMemorySaver




from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from IPython.display import Image,display
from dotenv import load_dotenv

load_dotenv()
# os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

from langchain_google_genai import ChatGoogleGenerativeAI
llm=ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2,google_api_key=os.environ["GOOGLE_API_KEY"])

# checkpointer = InMemorySaver()
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



# db_user = "root"
# db_password = "12345"
# db_host = "localhost"
# db_name = "retail_sales_db" streamlit

# Create SQLAlchemy engine
from langchain_community.utilities import SQLDatabase

# engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}") streamlit

# db = SQLDatabase(engine, sample_rows_in_table_info=3)

# chain = create_sql_query_chain(llm, db)


# def execute_query(question :str)->str:
#     try:
#         # Generate SQL query from question
#         response = chain.invoke({"question": question})
#         cleaned_query = response.strip('```sql\n').strip('\n```')
#         result = db.run(cleaned_query)
       
                
#         # Return the query and the result
#         return result
#     except ProgrammingError as e:
#         # st.error(f"An error occurred: {e}")
#         return None
    
# execute_query_tool = Tool(
#     name="execute_query",
#     func=execute_query,
#     description= "Use this tool to answer natural language questions related to customer transactions, product categories, and sales data "
#         "stored in the 'sales_tb' table of the 'retail_sales_db' MySQL database.\n\n"
        
#         "The table contains the following columns:\n"
#         "- TransactionID\n"
#         "- Date\n"
#         "- CustomerID\n"
#         "- Gender\n"
#         "- Age\n"
#         "- ProductCategory\n"
#         "- Quantity\n"
#         "- PriceperUnit\n"
#         "- TotalAmount\n\n"
        
#         "This tool converts natural language to SQL and returns the executed result.\n\n"

#         "Example questions with corresponding queries and expected answers:\n"
#         "1. Question: 'How many customers are there?'\n"
#         "   SQL: SELECT COUNT(DISTINCT CustomerID) AS NumberOfCustomers FROM sales_tb;\n"
#         "   Answer: 29\n\n"

#         "2. Question: 'How many unique customers are there for each product category?'\n"
#         "   SQL: SELECT ProductCategory, COUNT(DISTINCT CustomerID) AS UniqueCustomers FROM sales_tb GROUP BY ProductCategory;\n"
#         "   Answer: [('Beauty', 8), ('Clothing', 13), ('Electronics', 8)]\n\n"

#         "3. Question: 'Calculate total sales amount per product category:'\n"
#         "   SQL: SELECT ProductCategory, SUM(TotalAmount) AS TotalSalesAmount FROM sales_tb GROUP BY ProductCategory ORDER BY TotalSalesAmount DESC;\n"
#         "   Answer: [('Clothing', 7940.0), ('Electronics', 5360.0), ('Beauty', 1760.0)]\n\n"

#         "4. Question: 'Which gender spent the most overall?'\n"
#         "   SQL: SELECT Gender, SUM(TotalAmount) AS TotalSpent FROM sales_tb GROUP BY Gender ORDER BY TotalSpent DESC;\n"
#         "   Answer: [('Male', 7925.0), ('Female', 5135.0)]\n\n"

#         "5. Question: 'Show total sales per month:'\n"
#         "   SQL: SELECT MONTH(Date) AS Month, SUM(TotalAmount) AS MonthlySales FROM sales_tb GROUP BY MONTH(Date) ORDER BY Month;\n"
#         "   Answer: [(1, 1680.0), (2, 2700.0), (3, 50.0), (4, 1280.0), (5, 600.0), (6, 0), (7, 0), (8, 1580.0), (9, 50.0), (10, 2500.0), (11, 1350.0), (12, 300.0)]"
# )

# execute_query_tool
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
# graph=graph_builder.compile(checkpointer=checkpointer)



# graph = graph_builder.compile()



















# if __name__ == "__main__":
#     while True:
#         try:
#             # user_input = input("User: ")
#             user_input=st.text_input("Enter your question:")

#             if user_input.lower() in ["quit", "exit", "q"]:
#                 print("Goodbye!")
#                 break

#             response = graph.invoke({"messages": [HumanMessage(content=user_input)]})
#             ai_message = response["messages"][-1].content
#             st.write(ai_message)
#             for m in response['messages']:
#                 m.pretty_print()
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             break

# if __name__ == "__main__":
    
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     st.subheader("Chat with AI (Tool-Augmented)")

#     for role, msg in st.session_state.chat_history:
#         with st.chat_message(role):
#             st.markdown(msg)

#     user_input = st.chat_input("Type your question here...", key="user_input")

#     if user_input:
#         # Append user message to history
#         st.session_state.chat_history.append(("user", user_input))
#         with st.chat_message("user"):
#                 st.markdown(user_input)

#         try:
#             config = {"configurable": {"thread_id": "1"}}
#             response = graph.invoke({"messages": [HumanMessage(content=user_input)]},config=config)
#             # ai_message = response["messages"]
#             ai_message = None
#             for message in reversed(response["messages"]):
#                 if isinstance(message, AIMessage) and message.content.strip():
#                     ai_message = message.content.strip()
#                     break
#                 elif isinstance(message, ToolMessage) and message.content.strip():
#                     ai_message = message.content.strip()
#                     break
                   

#             # Append AI response to history
#             st.session_state.chat_history.append(("assistant", ai_message))

#             # Show response
#             with st.chat_message("assistant"):
#                 st.markdown(ai_message)

#         except Exception as e:
#             st.error(f"An error occurred: {e}")

  

if __name__ == "__main__":

    # ✅ One-time init: store thread_id and memory in session state
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = "user-001"  # you can randomize if needed

    if "checkpointer" not in st.session_state:
        st.session_state.checkpointer = InMemorySaver()  # or SqliteSaver("memory.db")

    if "graph" not in st.session_state:
        st.session_state.graph = graph_builder.compile(checkpointer=st.session_state.checkpointer)

    graph = st.session_state.graph

  

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.subheader("Chat with AI (Tool-Augmented)")

    # Show prior messages
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    # Input box
    user_input = st.chat_input("Type your question here...", key="user_input")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # ✅ Use persistent config
        config = {
            "thread_id": st.session_state.thread_id,
            "checkpoint": st.session_state.checkpointer
        }

        try:
            response = graph.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=config
            )
            print(response)
            ai_message = None
            for message in reversed(response["messages"]):
                 if isinstance(message, (AIMessage, ToolMessage)) and message.content and message.content.strip():
                    ai_message = message.content.strip()
                    break
        
            # for message in reversed(response["messages"]):
            #     if isinstance(message, AIMessage) and message.content.strip():
            #         ai_message = message.content.strip()
            #         break
            #     elif isinstance(message, ToolMessage) and message.content.strip():
            #         ai_message = message.content.strip()
            #         break

            st.session_state.chat_history.append(("assistant", ai_message))

            with st.chat_message("assistant"):
                st.markdown(ai_message)

        except Exception as e:
            st.error(f"An error occurred: {e}")
