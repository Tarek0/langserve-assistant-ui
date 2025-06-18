"""
NPS (Net Promoter Score) related metrics tools for Vodafone data.
Currently implements mocked data for demonstration purposes.

Supports metrics for UK, DE, and PT country codes:
- NPS Score (Net Promoter Score) 
- Deep Detraction Rate with historical trends and analysis
"""

from datetime import datetime, timezone
from langchain_core.tools import tool


@tool
def get_nps_score(country_code: str):
    """Get the Net Promoter Score (NPS) for Vodafone in a given country. 
    
    This is a mocked function and supports country codes 'UK', 'DE', and 'PT'.
    
    Args:
        country_code: Country code (UK, DE, PT)
        
    Returns:
        Dictionary containing NPS data or error message
    """
    # This is a mock implementation
    mock_nps_data = {
        "UK": {"company_name": "Vodafone UK", "nps_score": 45},
        "DE": {"company_name": "Vodafone Germany", "nps_score": 42},
        "PT": {"company_name": "Vodafone Portugal", "nps_score": 48},
    }

    code = country_code.upper()
    if code in mock_nps_data:
        response_data = mock_nps_data[code].copy()
        response_data["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return response_data
        
    return {"error": f"NPS score for Vodafone in {country_code} not found. Supported country codes are UK, DE, PT."}


@tool
def get_deep_detraction_rate(country_code: str):
    """Get the Deep Detraction Rate for Vodafone in a given country, including a historical trend. 
    
    This is a mocked function and supports country codes 'UK', 'DE', and 'PT'.
    
    Args:
        country_code: Country code (UK, DE, PT)
        
    Returns:
        Dictionary containing DDR data with historical trends or error message
    """
    # This is a mock implementation
    mock_ddr_data = {
        "UK": {
            "company_name": "Vodafone UK", 
            "deep_detraction_rate": 10.0,  # Changed to numeric for easier processing
            "deep_detraction_rate_formatted": "10%",
            "status": "improving",  # Added status indicator
            "benchmark": {
                "industry_average": 12.5,
                "target": 8.0,
                "status": "above_target"
            },
            "trend": [
                {"date": "2024-01", "rate": 12.0, "month_name": "January 2024"},
                {"date": "2024-02", "rate": 11.5, "month_name": "February 2024"},
                {"date": "2024-03", "rate": 11.0, "month_name": "March 2024"},
                {"date": "2024-04", "rate": 10.5, "month_name": "April 2024"},
                {"date": "2024-05", "rate": 10.0, "month_name": "May 2024"},
            ],
            "trend_analysis": {
                "direction": "decreasing",
                "change_absolute": -2.0,
                "change_percentage": -16.7,
                "description": "The rate has decreased from 12% to 10% over the period, showing consistent improvement.",
                "projection": "If the current trend continues, the rate may reach 9% by next month."
            },
            "insights": [
                "DDR has improved by 2 percentage points over 5 months",
                "Currently 2.5 points below industry average",
                "Still 2 points above target of 8%",
                "Consistent month-over-month improvement trend"
            ],
            "period": {
                "start_date": "2024-01",
                "end_date": "2024-05",
                "duration_months": 5
            }
        },
        "DE": {
            "company_name": "Vodafone Germany", 
            "deep_detraction_rate": 15.0,
            "deep_detraction_rate_formatted": "15%",
            "status": "improving",
            "benchmark": {
                "industry_average": 14.2,
                "target": 12.0,
                "status": "above_target"
            },
            "trend": [
                {"date": "2024-01", "rate": 18.0, "month_name": "January 2024"},
                {"date": "2024-02", "rate": 17.0, "month_name": "February 2024"},
                {"date": "2024-03", "rate": 16.0, "month_name": "March 2024"},
                {"date": "2024-04", "rate": 15.5, "month_name": "April 2024"},
                {"date": "2024-05", "rate": 15.0, "month_name": "May 2024"},
            ],
            "trend_analysis": {
                "direction": "decreasing",
                "change_absolute": -3.0,
                "change_percentage": -16.7,
                "description": "The rate has decreased from 18% to 15% over the period, showing significant improvement.",
                "projection": "If the current trend continues, the rate may reach 14% by next month."
            },
            "insights": [
                "DDR has improved by 3 percentage points over 5 months",
                "Now slightly above industry average of 14.2%",
                "Still 3 points above target of 12%",
                "Strong improvement trajectory"
            ],
            "period": {
                "start_date": "2024-01",
                "end_date": "2024-05",
                "duration_months": 5
            }
        },
        "PT": {
            "company_name": "Vodafone Portugal", 
            "deep_detraction_rate": 11.0,
            "deep_detraction_rate_formatted": "11%",
            "status": "declining",  # This one is getting worse
            "benchmark": {
                "industry_average": 10.5,
                "target": 9.0,
                "status": "above_target"
            },
            "trend": [
                {"date": "2024-01", "rate": 10.0, "month_name": "January 2024"},
                {"date": "2024-02", "rate": 10.2, "month_name": "February 2024"},
                {"date": "2024-03", "rate": 10.5, "month_name": "March 2024"},
                {"date": "2024-04", "rate": 10.8, "month_name": "April 2024"},
                {"date": "2024-05", "rate": 11.0, "month_name": "May 2024"},
            ],
            "trend_analysis": {
                "direction": "increasing",
                "change_absolute": 1.0,
                "change_percentage": 10.0,
                "description": "The rate has increased from 10% to 11% over the period, indicating deteriorating performance.",
                "projection": "If the current trend continues, the rate may reach 11.5% by next month."
            },
            "insights": [
                "DDR has worsened by 1 percentage point over 5 months",
                "Now above industry average of 10.5%",
                "2 points above target of 9%",
                "Requires immediate attention to reverse trend"
            ],
            "period": {
                "start_date": "2024-01",
                "end_date": "2024-05",
                "duration_months": 5
            }
        },
    }

    code = country_code.upper()
    if code in mock_ddr_data:
        response_data = mock_ddr_data[code].copy()
        response_data["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        response_data["last_updated_formatted"] = datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        return response_data
        
    return {"error": f"Deep Detraction Rate for Vodafone in {country_code} not found. Supported country codes are UK, DE, PT."} 