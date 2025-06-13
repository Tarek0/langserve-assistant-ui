import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from datetime import datetime, timezone
import requests
from typing import Dict, Any

load_dotenv()

llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2023-07-01-preview"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt35"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)

def fetch_weather_data(location: str) -> Dict[str, Any]:
    """Fetch weather data from WeatherAPI.com."""
    api_key = os.environ.get("WEATHERAPI_KEY")
    if not api_key:
        raise ValueError("WEATHERAPI_KEY environment variable is not set")
    
    base_url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": location,
        "aqi": "yes"  # Include air quality data
    }
    
    response = requests.get(base_url, params=params)
    if not response.ok:
        raise ValueError(f"Failed to fetch weather data: {response.text}")
    
    return response.json()

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a specific location.
    
    Args:
        location: The city name to get weather for (e.g., "London", "New York", "Tokyo")
    
    Returns:
        A formatted string containing the current weather information
    """
    try:
        data = fetch_weather_data(location)
        current = data["current"]
        location_data = data["location"]
        
        # Extract relevant weather information
        weather_info = {
            "location": location_data["name"],
            "country": location_data["country"],
            "region": location_data["region"],
            "local_time": location_data["localtime"],
            "temperature": {
                "current": round(current["temp_c"]),
                "feels_like": round(current["feelslike_c"]),
                "unit": "°C"
            },
            "conditions": current["condition"]["text"],
            "humidity": current["humidity"],
            "wind": {
                "speed": round(current["wind_kph"]),
                "direction": current["wind_dir"],
                "unit": "km/h"
            },
            "uv_index": current["uv"],
            "air_quality": current.get("air_quality", {}).get("us-epa-index", "N/A")
        }
        
        # Format the weather information into a readable string
        weather_str = (
            f"Current weather in {weather_info['location']}, {weather_info['region']}, {weather_info['country']} "
            f"(Local time: {weather_info['local_time']}):\n"
            f"• Temperature: {weather_info['temperature']['current']}°C "
            f"(feels like {weather_info['temperature']['feels_like']}°C)\n"
            f"• Conditions: {weather_info['conditions']}\n"
            f"• Humidity: {weather_info['humidity']}%\n"
            f"• Wind: {weather_info['wind']['speed']} {weather_info['wind']['unit']} from {weather_info['wind']['direction']}\n"
            f"• UV Index: {weather_info['uv_index']}\n"
            f"• Air Quality Index (US EPA): {weather_info['air_quality']}"
        )
        
        return weather_str
    except Exception as e:
        return f"Sorry, I couldn't fetch the weather data for {location}. Error: {str(e)}"

@tool(return_direct=True)
def get_stock_price(stock_symbol: str):
    """Call to get the current stock price and related information for a given stock symbol."""
    # This is a mock implementation
    mock_stock_data = {
        "AAPL": {
            "symbol": "AAPL",
            "company_name": "Apple Inc.",
            "current_price": 173.50,
            "change": 2.35,
            "change_percent": 1.37,
            "volume": 52436789,
            "market_cap": "2.73T",
            "pe_ratio": 28.5,
            "fifty_two_week_high": 198.23,
            "fifty_two_week_low": 124.17,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        # Add more mock data for other symbols as needed
    }
    
    return mock_stock_data["AAPL"]

tools = [get_weather, get_stock_price]

SYSTEM_PROMPT = """You are a helpful assistant. 
You are able to call the following tools:
- get_weather: Get current weather information for a city, including temperature, conditions, humidity, wind, UV index, and air quality
- get_stock_price: Get current stock price and related information for a stock symbol
"""

system_message = SystemMessage(content=SYSTEM_PROMPT)
agent_executor = create_react_agent(llm, tools, messages_modifier=system_message)

