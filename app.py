from langchain_openai import ChatOpenAI
import requests
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage

load_dotenv()
polygon_key = os.getenv("POLYGON_KEY")
openai_key = os.getenv("OPENAPI_KEY")
openweather_key = os.getenv("OPENWEATHER_KEY")

llm = ChatOpenAI(temperature=0.0)

@tool
def get_weather(city: str, country_code: str) -> str:
    """
    Fetches the weather information for a given city and country code.

    Args:
        city (str): The name of the city.
        country_code (str): The country code of the city.

    Returns:
        str: A string containing the weather description and temperature.

    """

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={openweather_key}&units=metric",
        timeout=5,
    )

    data = response.json()
    return f"The weather in {city}, {country_code} is {data['weather'][0]['description']} with a temperature of {data['main']['temp']} C."


@tool
def get_stock_price(stock_ticker: str) -> float:
    """
    Retrieves the previous closing price of a stock using the Polygon API.

    Args:
        stock_ticker (str): The ticker symbol of the stock.

    Returns:
        float: The previous closing price of the stock.
    """
    response = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{stock_ticker}/prev?adjusted=true&apiKey={polygon_key}",
        timeout=5,
    )

    data = response.json()
    return data["results"][0]["c"]


# langchain.debug = True
tools = [get_stock_price, get_weather]
llm_with_tools = llm.bind_tools(tools)


import streamlit as st

st.title("AI Chatbot for Weather and Stock Queries")

prompt_template = """
You are a chatbot. You are designed to answer questions about the weather and stock prices.
If a user asks question about anything other than the weather or stock prices, you should \
respond with a message indicating that you are unable to answer the question. \
"""
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(prompt_template)]
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if query := st.chat_input("Ask me about the weather or stock prices!"):
    # Display user message in chat message container

    # print(st.session_state.messages)

    with st.chat_message("user"):
        st.markdown(query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})


    st.session_state.chat_history.append(HumanMessage(query))
    ai_msg = llm_with_tools.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(ai_msg)
    for tool_call in ai_msg.tool_calls:
        selected_tool = {
            "get_stock_price": get_stock_price,
            "get_weather": get_weather,
        }[tool_call["name"].lower()]
        tool_output = selected_tool.invoke(tool_call["args"])
        st.session_state.chat_history.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

    response = llm_with_tools.invoke(st.session_state.chat_history)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.content)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    st.session_state.chat_history.append(response)
    
