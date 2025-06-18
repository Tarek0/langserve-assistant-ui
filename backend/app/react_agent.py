import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from .tools import (
    get_weather,
    get_stock_price,
    get_nps_score,
    get_deep_detraction_rate,
    get_churn_rate,
    get_churn_reasons
)

load_dotenv()

llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2023-07-01-preview"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt35"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)



# Tools are now imported from the tools package

tools = [get_weather, get_stock_price, get_nps_score, get_deep_detraction_rate, get_churn_rate, get_churn_reasons]

SYSTEM_PROMPT = """You are a helpful assistant. 
You are able to call the following tools:
- get_weather: Get current weather information for a city, including temperature, conditions, humidity, wind, UV index, and air quality
- get_stock_price: Get current stock price and related information for a stock symbol. This is a mocked function and only supports 'AAPL'.
- get_nps_score: Get the Net Promoter Score (NPS) for Vodafone in a given country. This is a mocked function and supports country codes 'UK', 'DE', and 'PT'.
- get_deep_detraction_rate: Get the Deep Detraction Rate and a historical trend for Vodafone in a given country. This is a mocked function and supports country codes 'UK', 'DE', and 'PT'.
- get_churn_rate: Get the Churn Rate and a historical trend for Vodafone in a given country. This is a mocked function and supports country codes 'UK', 'DE', and 'PT'.
- get_churn_reasons: Get detailed reasons why customers are churning for Vodafone in a given country, including breakdown by percentage, severity, and trends. This is a mocked function and supports country codes 'UK', 'DE', and 'PT'.
"""

system_message = SystemMessage(content=SYSTEM_PROMPT)
agent_executor = create_react_agent(llm, tools, messages_modifier=system_message)

