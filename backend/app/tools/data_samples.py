"""
Sample data generation tools for testing chart functionality.
Provides various types of sample datasets for demonstration purposes.
"""

from datetime import datetime, timezone, timedelta
from langchain_core.tools import tool
import random


@tool
def get_sample_sales_data(period_months: int = 6):
    """Generate sample sales data for chart testing.
    
    Args:
        period_months: Number of months of data to generate (default: 6)
        
    Returns:
        Dictionary containing sample sales data with monthly breakdown
    """
    
    base_date = datetime.now() - timedelta(days=30 * period_months)
    sales_data = []
    
    base_sales = 10000
    
    for i in range(period_months):
        current_date = base_date + timedelta(days=30 * i)
        month_name = current_date.strftime("%B %Y")
        month_code = current_date.strftime("%Y-%m")
        
        # Add some realistic variation
        seasonal_factor = 1 + 0.2 * random.sin(i * 0.5)  # Seasonal variation
        growth_factor = 1 + (i * 0.05)  # Growth trend
        random_factor = 1 + random.uniform(-0.15, 0.15)  # Random variation
        
        sales = int(base_sales * seasonal_factor * growth_factor * random_factor)
        
        sales_data.append({
            "month": month_code,
            "month_name": month_name,
            "sales": sales,
            "sales_formatted": f"${sales:,}"
        })
    
    return {
        "dataset_name": "Sample Sales Data",
        "description": f"Monthly sales data over {period_months} months showing growth trend with seasonal variation",
        "data": sales_data,
        "metadata": {
            "total_records": len(sales_data),
            "date_range": f"{sales_data[0]['month']} to {sales_data[-1]['month']}",
            "data_types": {
                "month": "date",
                "month_name": "text", 
                "sales": "numeric",
                "sales_formatted": "text"
            }
        },
        "suggested_charts": ["line", "bar"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }


@tool  
def get_sample_market_share_data():
    """Generate sample market share data for pie chart testing.
    
    Returns:
        Dictionary containing sample market share data for different companies
    """
    
    companies = [
        {"name": "Company A", "share": 35.2},
        {"name": "Company B", "share": 28.7},
        {"name": "Company C", "share": 18.4},
        {"name": "Company D", "share": 12.1},
        {"name": "Others", "share": 5.6}
    ]
    
    return {
        "dataset_name": "Sample Market Share Data",
        "description": "Market share distribution among top companies in the industry",
        "data": companies,
        "metadata": {
            "total_records": len(companies),
            "total_share": sum(c["share"] for c in companies),
            "data_types": {
                "name": "categorical",
                "share": "numeric"
            }
        },
        "suggested_charts": ["pie", "bar"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }


@tool
def get_sample_performance_metrics():
    """Generate sample performance metrics data for multi-metric analysis.
    
    Returns:
        Dictionary containing sample performance data with multiple metrics
    """
    
    departments = ["Sales", "Marketing", "Engineering", "Support", "HR"]
    metrics_data = []
    
    for dept in departments:
        # Generate realistic but varied metrics
        efficiency = random.uniform(75, 95)
        satisfaction = random.uniform(80, 98)
        productivity = random.uniform(70, 90)
        
        metrics_data.append({
            "department": dept,
            "efficiency": round(efficiency, 1),
            "satisfaction": round(satisfaction, 1), 
            "productivity": round(productivity, 1),
            "efficiency_formatted": f"{efficiency:.1f}%",
            "satisfaction_formatted": f"{satisfaction:.1f}%",
            "productivity_formatted": f"{productivity:.1f}%"
        })
    
    return {
        "dataset_name": "Sample Performance Metrics",
        "description": "Department performance metrics including efficiency, satisfaction, and productivity scores",
        "data": metrics_data,
        "metadata": {
            "total_records": len(metrics_data),
            "metrics": ["efficiency", "satisfaction", "productivity"],
            "data_types": {
                "department": "categorical",
                "efficiency": "numeric",
                "satisfaction": "numeric", 
                "productivity": "numeric"
            }
        },
        "suggested_charts": ["multi-bar", "scatter", "bar"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }


@tool
def get_sample_time_series_data(metric_name: str = "Revenue", days: int = 30):
    """Generate sample time series data for line chart testing.
    
    Args:
        metric_name: Name of the metric to generate data for
        days: Number of days of data to generate
        
    Returns:
        Dictionary containing daily time series data
    """
    
    base_date = datetime.now() - timedelta(days=days)
    time_series_data = []
    
    base_value = 1000
    trend = random.uniform(-0.5, 1.5)  # Random trend
    
    for i in range(days):
        current_date = base_date + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        date_formatted = current_date.strftime("%m/%d")
        
        # Generate realistic daily variation
        trend_value = base_value + (i * trend)
        seasonal_factor = 1 + 0.1 * random.sin(i * 0.2)
        daily_noise = random.uniform(-50, 50)
        
        value = max(0, int(trend_value * seasonal_factor + daily_noise))
        
        time_series_data.append({
            "date": date_str,
            "date_formatted": date_formatted,
            "value": value,
            "metric_name": metric_name
        })
    
    return {
        "dataset_name": f"Sample {metric_name} Time Series",
        "description": f"Daily {metric_name.lower()} data over {days} days showing trend and variation",
        "data": time_series_data,
        "metadata": {
            "total_records": len(time_series_data),
            "date_range": f"{time_series_data[0]['date']} to {time_series_data[-1]['date']}",
            "metric": metric_name,
            "data_types": {
                "date": "date",
                "date_formatted": "text",
                "value": "numeric",
                "metric_name": "text"
            }
        },
        "suggested_charts": ["line"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }


@tool
def get_sample_scatter_data(records: int = 50):
    """Generate sample scatter plot data for correlation analysis.
    
    Args:
        records: Number of data points to generate
        
    Returns:
        Dictionary containing sample data for scatter plot
    """
    
    scatter_data = []
    
    for i in range(records):
        # Create some correlation between x and y with noise
        x = random.uniform(10, 100)
        y = 2 * x + random.uniform(-20, 20) + random.uniform(0, 30)  # Some correlation + noise
        
        scatter_data.append({
            "x_value": round(x, 1),
            "y_value": round(y, 1),
            "point_id": f"Point_{i+1}"
        })
    
    return {
        "dataset_name": "Sample Scatter Data",
        "description": f"Sample scatter plot data with {records} points showing correlation between X and Y variables",
        "data": scatter_data,
        "metadata": {
            "total_records": len(scatter_data),
            "correlation": "positive_moderate",
            "data_types": {
                "x_value": "numeric",
                "y_value": "numeric",
                "point_id": "text"
            }
        },
        "suggested_charts": ["scatter"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    } 