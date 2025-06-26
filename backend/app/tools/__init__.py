"""
Tools package for the React Agent.

This package contains all tool functions organized by domain:
- demo: Demo tools including weather (WeatherAPI) and stock price data (mocked)
- nps_metrics: NPS and Deep Detraction Rate tools for Vodafone
- churn_metrics: Churn Rate tools for Vodafone
- chart_generator: Universal chart generation tools for any dataset
- data_samples: Sample data generation tools for testing chart functionality
"""

from .demo import get_weather, get_stock_price
from .nps_metrics import get_nps_score, get_deep_detraction_rate
from .churn_metrics import get_churn_rate, get_churn_reasons
from .chart_generator import generate_chart_data, create_custom_dataset
from .data_samples import (
    get_sample_sales_data,
    get_sample_market_share_data,
    get_sample_performance_metrics,
    get_sample_time_series_data,
    get_sample_scatter_data
)

__all__ = [
    "get_weather",
    "get_stock_price", 
    "get_nps_score",
    "get_deep_detraction_rate",
    "get_churn_rate",
    "get_churn_reasons",
    "generate_chart_data",
    "create_custom_dataset",
    "get_sample_sales_data",
    "get_sample_market_share_data",
    "get_sample_performance_metrics",
    "get_sample_time_series_data",
    "get_sample_scatter_data"
] 