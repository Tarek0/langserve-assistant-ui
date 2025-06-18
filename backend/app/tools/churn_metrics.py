"""
Churn metrics tools for Vodafone data.
Currently implements mocked data for demonstration purposes.

Supports churn rate metrics for UK, DE, and PT country codes:
- Churn Rate with historical trends and retention analysis
- Churn Reasons with detailed breakdown and insights
"""

from datetime import datetime, timezone
from langchain_core.tools import tool


@tool
def get_churn_rate(country_code: str):
    """Get the Churn Rate for Vodafone in a given country, including a historical trend. 
    
    This is a mocked function and supports country codes 'UK', 'DE', and 'PT'.
    
    Args:
        country_code: Country code (UK, DE, PT)
        
    Returns:
        Dictionary containing churn rate data with historical trends or error message
    """
    # This is a mock implementation
    mock_churn_data = {
        "UK": {
            "company_name": "Vodafone UK", 
            "churn_rate": 2.8,
            "churn_rate_formatted": "2.8%",
            "status": "improving",
            "benchmark": {
                "industry_average": 3.2,
                "target": 2.5,
                "status": "above_target"
            },
            "trend": [
                {"date": "2024-01", "rate": 3.5, "month_name": "January 2024"},
                {"date": "2024-02", "rate": 3.2, "month_name": "February 2024"},
                {"date": "2024-03", "rate": 3.0, "month_name": "March 2024"},
                {"date": "2024-04", "rate": 2.9, "month_name": "April 2024"},
                {"date": "2024-05", "rate": 2.8, "month_name": "May 2024"},
            ],
            "trend_analysis": {
                "direction": "decreasing",
                "change_absolute": -0.7,
                "change_percentage": -20.0,
                "description": "The churn rate has decreased from 3.5% to 2.8% over the period, showing strong customer retention improvement.",
                "projection": "If the current trend continues, the rate may reach 2.6% by next month."
            },
            "insights": [
                "Churn rate has improved by 0.7 percentage points over 5 months",
                "Currently 0.4 points below industry average of 3.2%",
                "Still 0.3 points above target of 2.5%",
                "Strong customer retention momentum building"
            ],
            "period": {
                "start_date": "2024-01",
                "end_date": "2024-05",
                "duration_months": 5
            }
        },
        "DE": {
            "company_name": "Vodafone Germany", 
            "churn_rate": 4.2,
            "churn_rate_formatted": "4.2%",
            "status": "stable",
            "benchmark": {
                "industry_average": 4.1,
                "target": 3.5,
                "status": "above_target"
            },
            "trend": [
                {"date": "2024-01", "rate": 4.3, "month_name": "January 2024"},
                {"date": "2024-02", "rate": 4.1, "month_name": "February 2024"},
                {"date": "2024-03", "rate": 4.2, "month_name": "March 2024"},
                {"date": "2024-04", "rate": 4.3, "month_name": "April 2024"},
                {"date": "2024-05", "rate": 4.2, "month_name": "May 2024"},
            ],
            "trend_analysis": {
                "direction": "stable",
                "change_absolute": -0.1,
                "change_percentage": -2.3,
                "description": "The churn rate has remained relatively stable around 4.2% with minor fluctuations.",
                "projection": "Rate expected to continue around 4.1-4.3% range in coming months."
            },
            "insights": [
                "Churn rate has been relatively stable over 5 months",
                "Slightly above industry average of 4.1%",
                "0.7 points above target of 3.5%",
                "Needs focused retention initiatives to improve"
            ],
            "period": {
                "start_date": "2024-01",
                "end_date": "2024-05",
                "duration_months": 5
            }
        },
        "PT": {
            "company_name": "Vodafone Portugal", 
            "churn_rate": 3.6,
            "churn_rate_formatted": "3.6%",
            "status": "declining",
            "benchmark": {
                "industry_average": 3.4,
                "target": 3.0,
                "status": "above_target"
            },
            "trend": [
                {"date": "2024-01", "rate": 3.1, "month_name": "January 2024"},
                {"date": "2024-02", "rate": 3.3, "month_name": "February 2024"},
                {"date": "2024-03", "rate": 3.4, "month_name": "March 2024"},
                {"date": "2024-04", "rate": 3.5, "month_name": "April 2024"},
                {"date": "2024-05", "rate": 3.6, "month_name": "May 2024"},
            ],
            "trend_analysis": {
                "direction": "increasing",
                "change_absolute": 0.5,
                "change_percentage": 16.1,
                "description": "The churn rate has increased from 3.1% to 3.6% over the period, indicating deteriorating customer retention.",
                "projection": "If the current trend continues, the rate may reach 3.8% by next month."
            },
            "insights": [
                "Churn rate has worsened by 0.5 percentage points over 5 months",
                "Now above industry average of 3.4%",
                "0.6 points above target of 3.0%",
                "Urgent attention needed to reverse retention trend"
            ],
            "period": {
                "start_date": "2024-01",
                "end_date": "2024-05",
                "duration_months": 5
            }
        },
    }

    code = country_code.upper()
    if code in mock_churn_data:
        response_data = mock_churn_data[code].copy()
        response_data["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        response_data["last_updated_formatted"] = datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        return response_data
        
    return {"error": f"Churn Rate for Vodafone in {country_code} not found. Supported country codes are UK, DE, PT."}


@tool
def get_churn_reasons(country_code: str):
    """Get the top 5 reasons for customer churn for Vodafone in a given country with percentage breakdown and historical trends.
    
    This is a mocked function and supports country codes 'UK', 'DE', and 'PT'.
    
    Args:
        country_code: Country code (UK, DE, PT)
        
    Returns:
        Dictionary containing churn reasons data with percentage breakdown and trend analysis or error message
    """
    # This is a mock implementation
    mock_churn_reasons_data = {
        "UK": {
            "company_name": "Vodafone UK",
            "total_churned_customers": 12500,
            "analysis_period": "May 2024",
            "top_5_reasons": [
                {
                    "reason": "High pricing/Better competitor offers",
                    "current_percentage": 34.5,
                    "current_count": 4313,
                    "severity": "high",
                    "trend_direction": "increasing",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 29.2, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 30.8, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 32.1, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 33.4, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 34.5, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Poor network coverage/Quality issues",
                    "current_percentage": 26.3,
                    "current_count": 3288,
                    "severity": "high", 
                    "trend_direction": "stable",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 26.8, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 26.1, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 26.5, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 26.0, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 26.3, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Customer service issues",
                    "current_percentage": 19.7,
                    "current_count": 2463,
                    "severity": "medium",
                    "trend_direction": "decreasing",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 22.4, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 21.8, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 20.9, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 20.2, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 19.7, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Billing/Contract disputes",
                    "current_percentage": 12.8,
                    "current_count": 1600,
                    "severity": "medium",
                    "trend_direction": "stable",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 13.1, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 12.6, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 12.9, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 13.2, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 12.8, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Relocation/Moving abroad",
                    "current_percentage": 6.7,
                    "current_count": 838,
                    "severity": "low",
                    "trend_direction": "stable",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 8.5, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 8.7, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 7.6, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 7.2, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 6.7, "month_name": "May 2024"}
                    ]
                }
            ],
            "insights": [
                "Price sensitivity is the primary driver - consider competitive pricing strategies",
                "Network quality issues affect 1 in 4 churned customers - infrastructure investment needed",
                "Customer service improvements are showing positive results (decreasing trend)",
                "Billing disputes remain consistent - process optimization opportunity"
            ],
            "recommendations": [
                "Launch targeted retention campaigns for price-sensitive segments",
                "Prioritize network coverage improvements in high-churn areas",
                "Continue customer service training initiatives", 
                "Implement proactive billing communication"
            ],
            "benchmarks": {
                "industry_avg_price_sensitivity": 28.5,
                "industry_avg_network_issues": 22.1,
                "performance_vs_industry": "slightly worse on pricing, similar on network"
            }
        },
        "DE": {
            "company_name": "Vodafone Germany",
            "total_churned_customers": 18750,
            "analysis_period": "May 2024",
            "top_5_reasons": [
                {
                    "reason": "Poor network coverage/Quality issues",
                    "current_percentage": 31.2,
                    "current_count": 5850,
                    "severity": "high",
                    "trend_direction": "increasing",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 27.3, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 28.1, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 29.6, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 30.4, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 31.2, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "High pricing/Better competitor offers",
                    "current_percentage": 28.4,
                    "current_count": 5325,
                    "severity": "high",
                    "trend_direction": "stable",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 28.9, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 28.1, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 28.7, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 28.2, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 28.4, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Customer service issues",
                    "current_percentage": 21.6,
                    "current_count": 4050,
                    "severity": "medium",
                    "trend_direction": "increasing",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 18.5, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 19.2, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 20.1, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 20.8, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 21.6, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Limited data allowances",
                    "current_percentage": 12.4,
                    "current_count": 2325,
                    "severity": "medium",
                    "trend_direction": "stable",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 13.2, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 12.8, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 12.1, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 12.7, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 12.4, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Billing/Contract disputes",
                    "current_percentage": 6.4,
                    "current_count": 1200,
                    "severity": "low",
                    "trend_direction": "decreasing",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 12.1, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 11.8, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 9.5, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 7.9, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 6.4, "month_name": "May 2024"}
                    ]
                }
            ],
            "insights": [
                "Network quality is the biggest concern - significant infrastructure gaps",
                "Strong competition on pricing from local operators",
                "Customer service satisfaction declining - resource constraint issue",
                "Data plan limitations becoming more important to customers"
            ],
            "recommendations": [
                "Urgent network infrastructure investment program",
                "Review and optimize data plan offerings",
                "Expand customer service team and improve training",
                "Competitive pricing analysis and adjustment"
            ],
            "benchmarks": {
                "industry_avg_price_sensitivity": 28.5,
                "industry_avg_network_issues": 22.1,
                "performance_vs_industry": "worse on network quality, competitive on pricing"
            }
        },
        "PT": {
            "company_name": "Vodafone Portugal",
            "total_churned_customers": 8900,
            "analysis_period": "May 2024",
            "top_5_reasons": [
                {
                    "reason": "High pricing/Better competitor offers",
                    "current_percentage": 37.8,
                    "current_count": 3364,
                    "severity": "high",
                    "trend_direction": "increasing",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 32.1, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 33.7, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 35.4, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 36.9, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 37.8, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Customer service issues",
                    "current_percentage": 24.3,
                    "current_count": 2163,
                    "severity": "high",
                    "trend_direction": "increasing",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 19.8, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 21.2, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 22.7, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 23.6, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 24.3, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Limited data allowances",
                    "current_percentage": 18.2,
                    "current_count": 1620,
                    "severity": "medium",
                    "trend_direction": "stable",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 17.9, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 18.5, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 17.8, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 18.4, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 18.2, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Poor network coverage/Quality issues",
                    "current_percentage": 12.9,
                    "current_count": 1148,
                    "severity": "medium",
                    "trend_direction": "decreasing",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 16.4, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 15.1, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 14.2, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 13.6, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 12.9, "month_name": "May 2024"}
                    ]
                },
                {
                    "reason": "Billing/Contract disputes",
                    "current_percentage": 6.8,
                    "current_count": 605,
                    "severity": "low",
                    "trend_direction": "stable",
                    "historical_trend": [
                        {"date": "2024-01", "percentage": 13.8, "month_name": "January 2024"},
                        {"date": "2024-02", "percentage": 11.5, "month_name": "February 2024"},
                        {"date": "2024-03", "percentage": 9.9, "month_name": "March 2024"},
                        {"date": "2024-04", "percentage": 7.5, "month_name": "April 2024"},
                        {"date": "2024-05", "percentage": 6.8, "month_name": "May 2024"}
                    ]
                }
            ],
            "insights": [
                "Price competition is most intense - aggressive competitor pricing",
                "Customer service quality declining significantly - major concern",
                "Data plans not competitive with market offerings",
                "Network quality better than other markets but still room for improvement"
            ],
            "recommendations": [
                "Immediate pricing strategy review and competitive response",
                "Customer service recovery program - quality and responsiveness focus",
                "Launch new data plan packages to match market demand",
                "Maintain network quality advantage through continued investment"
            ],
            "benchmarks": {
                "industry_avg_price_sensitivity": 28.5,
                "industry_avg_network_issues": 22.1,
                "performance_vs_industry": "significantly worse on pricing, better on network"
            }
        }
    }

    code = country_code.upper()
    if code in mock_churn_reasons_data:
        response_data = mock_churn_reasons_data[code].copy()
        response_data["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        response_data["last_updated_formatted"] = datetime.now(timezone.utc).strftime("%d/%m/%Y, %H:%M:%S")
        return response_data
        
    return {"error": f"Churn reasons for Vodafone in {country_code} not found. Supported country codes are UK, DE, PT."} 