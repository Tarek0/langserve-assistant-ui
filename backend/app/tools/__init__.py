"""
Tools package for the React Agent.

This package contains all tool functions organized by domain:
- demo: Demo tools including weather (WeatherAPI) and stock price data (mocked)
- nps_metrics: NPS and Deep Detraction Rate tools for Vodafone
- churn_metrics: Churn Rate tools for Vodafone
"""

from .demo import get_weather, get_stock_price
from .nps_metrics import get_nps_score, get_deep_detraction_rate
from .churn_metrics import get_churn_rate, get_churn_reasons

__all__ = [
    "get_weather",
    "get_stock_price", 
    "get_nps_score",
    "get_deep_detraction_rate",
    "get_churn_rate",
    "get_churn_reasons"
] 