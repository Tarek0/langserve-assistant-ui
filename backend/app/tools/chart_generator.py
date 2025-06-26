"""
Dynamic chart generation tools for any aggregated dataset.
Supports automatic data structure inference and multiple chart types.
"""

from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union
from langchain_core.tools import tool
import json


@tool
def generate_chart_data(
    data: Union[str, Dict, List], 
    chart_type: str = "auto",
    x_field: Optional[str] = None,
    y_field: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None
):
    """Generate chart data from any aggregated dataset with automatic structure inference.
    
    This tool can transform any structured data into chart-ready format with support for:
    - Line charts: Time series data with dates/timestamps
    - Bar charts: Categorical data with values
    - Pie charts: Data with categories and percentages/values
    - Multi-series charts: Data with multiple data series
    - Scatter plots: Data with x,y coordinates
    
    Args:
        data: Input data as JSON string, dictionary, or list of dictionaries
        chart_type: Chart type - "auto", "line", "bar", "pie", "scatter", "multi-line", "multi-bar"
        x_field: Field name for X-axis (auto-detected if not provided)
        y_field: Field name for Y-axis (auto-detected if not provided) 
        title: Chart title (auto-generated if not provided)
        description: Chart description (auto-generated if not provided)
        
    Returns:
        Dictionary containing chart configuration and processed data
    """
    
    # Parse input data if it's a JSON string
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON data provided"}
    
    if not data:
        return {"error": "No data provided"}
    
    # Convert single dict to list for consistent processing
    if isinstance(data, dict):
        data = [data]
    
    if not isinstance(data, list):
        return {"error": "Data must be a list of objects or a single object"}
    
    # Analyze data structure
    analysis = _analyze_data_structure(data)
    
    # Auto-detect chart type if not specified
    if chart_type == "auto":
        chart_type = _detect_optimal_chart_type(analysis)
    
    # Auto-detect fields if not specified
    if not x_field:
        x_field = analysis.get("suggested_x_field")
    if not y_field:
        y_field = analysis.get("suggested_y_field")
    
    # Generate chart configuration
    chart_config = _generate_chart_config(
        data, chart_type, x_field, y_field, analysis
    )
    
    # Auto-generate title and description if not provided
    if not title:
        title = _generate_title(chart_config, analysis)
    if not description:
        description = _generate_description(chart_config, analysis)
    
    return {
        "chart_type": chart_type,
        "title": title,
        "description": description,
        "config": chart_config,
        "data_analysis": analysis,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_data_points": len(data)
    }


def _analyze_data_structure(data: List[Dict]) -> Dict[str, Any]:
    """Analyze the structure of the input data to suggest optimal chart configuration."""
    
    if not data:
        return {}
    
    sample = data[0]
    fields = list(sample.keys()) if isinstance(sample, dict) else []
    
    analysis = {
        "total_records": len(data),
        "fields": fields,
        "field_types": {},
        "has_time_series": False,
        "has_categories": False,
        "has_percentages": False,
        "suggested_x_field": None,
        "suggested_y_field": None,
        "data_patterns": []
    }
    
    # Analyze each field
    for field in fields:
        values = [item.get(field) for item in data if item.get(field) is not None]
        if not values:
            continue
            
        field_analysis = _analyze_field(field, values)
        analysis["field_types"][field] = field_analysis
        
        # Check for time series patterns
        if field_analysis["type"] in ["date", "datetime"]:
            analysis["has_time_series"] = True
            if not analysis["suggested_x_field"]:
                analysis["suggested_x_field"] = field
                
        # Check for percentage patterns
        if field_analysis.get("is_percentage"):
            analysis["has_percentages"] = True
            
        # Check for categorical data
        if field_analysis["type"] == "categorical":
            analysis["has_categories"] = True
            
        # Suggest Y field for numeric data
        if field_analysis["type"] == "numeric" and not analysis["suggested_y_field"]:
            analysis["suggested_y_field"] = field
    
    # Determine data patterns
    if analysis["has_time_series"]:
        analysis["data_patterns"].append("time_series")
    if analysis["has_categories"] and analysis["has_percentages"]:
        analysis["data_patterns"].append("categorical_breakdown")
    if len([f for f in analysis["field_types"] if analysis["field_types"][f]["type"] == "numeric"]) > 2:
        analysis["data_patterns"].append("multi_metric")
    
    return analysis


def _analyze_field(field_name: str, values: List[Any]) -> Dict[str, Any]:
    """Analyze a specific field to determine its type and characteristics."""
    
    field_analysis = {
        "type": "unknown",
        "sample_values": values[:5],
        "unique_count": len(set(str(v) for v in values)),
        "is_percentage": False,
        "is_currency": False,
        "date_formats": []
    }
    
    # Check for numeric values
    numeric_values = []
    for val in values:
        try:
            if isinstance(val, (int, float)):
                numeric_values.append(float(val))
            elif isinstance(val, str):
                # Try to parse percentage
                if '%' in val:
                    numeric_values.append(float(val.replace('%', '')))
                    field_analysis["is_percentage"] = True
                # Try to parse currency
                elif any(symbol in val for symbol in ['$', '€', '£', '¥']):
                    clean_val = ''.join(c for c in val if c.isdigit() or c == '.')
                    if clean_val:
                        numeric_values.append(float(clean_val))
                        field_analysis["is_currency"] = True
                else:
                    numeric_values.append(float(val))
        except (ValueError, TypeError):
            pass
    
    if len(numeric_values) > len(values) * 0.8:  # 80% are numeric
        field_analysis["type"] = "numeric"
        field_analysis["range"] = [min(numeric_values), max(numeric_values)]
        field_analysis["average"] = sum(numeric_values) / len(numeric_values)
    
    # Check for date/time patterns
    date_patterns = [
        "%Y-%m-%d", "%Y-%m", "%m/%d/%Y", "%d/%m/%Y",
        "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"
    ]
    
    for pattern in date_patterns:
        try:
            parsed_dates = []
            for val in values[:10]:  # Test first 10 values
                if isinstance(val, str):
                    datetime.strptime(val, pattern)
                    parsed_dates.append(val)
            if len(parsed_dates) > len(values[:10]) * 0.8:
                field_analysis["type"] = "date" if "T" not in pattern and ":" not in pattern else "datetime"
                field_analysis["date_formats"].append(pattern)
                break
        except ValueError:
            continue
    
    # Check for categorical data
    if field_analysis["type"] == "unknown":
        if field_analysis["unique_count"] < len(values) * 0.5:  # Less than 50% unique
            field_analysis["type"] = "categorical"
        else:
            field_analysis["type"] = "text"
    
    return field_analysis


def _detect_optimal_chart_type(analysis: Dict[str, Any]) -> str:
    """Detect the optimal chart type based on data analysis."""
    
    patterns = analysis.get("data_patterns", [])
    
    if "time_series" in patterns:
        return "line"
    elif "categorical_breakdown" in patterns:
        return "pie" if analysis.get("has_percentages") else "bar"
    elif "multi_metric" in patterns:
        return "multi-bar"
    elif analysis.get("has_categories"):
        return "bar"
    else:
        return "line"  # Default fallback


def _generate_chart_config(
    data: List[Dict], 
    chart_type: str, 
    x_field: Optional[str], 
    y_field: Optional[str],
    analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate chart configuration based on data and chart type."""
    
    config = {
        "type": chart_type,
        "data": data,
        "x_field": x_field,
        "y_field": y_field,
        "options": {}
    }
    
    # Add type-specific configurations
    if chart_type == "line":
        config["options"] = {
            "responsive": True,
            "interaction": {"intersect": False},
            "scales": {
                "x": {"display": True, "title": {"display": True, "text": x_field or "X-Axis"}},
                "y": {"display": True, "title": {"display": True, "text": y_field or "Y-Axis"}}
            }
        }
    elif chart_type == "bar":
        config["options"] = {
            "responsive": True,
            "plugins": {"legend": {"position": "top"}},
            "scales": {
                "x": {"title": {"display": True, "text": x_field or "Categories"}},
                "y": {"title": {"display": True, "text": y_field or "Values"}}
            }
        }
    elif chart_type == "pie":
        config["options"] = {
            "responsive": True,
            "plugins": {
                "legend": {"position": "right"},
                "tooltip": {"callbacks": {"label": "function(context) { return context.label + ': ' + context.parsed + '%'; }"}}
            }
        }
    
    return config


def _generate_title(chart_config: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    """Auto-generate a chart title based on the data analysis."""
    
    chart_type = chart_config.get("type", "Chart")
    x_field = chart_config.get("x_field", "")
    y_field = chart_config.get("y_field", "")
    
    if chart_type == "line" and "time_series" in analysis.get("data_patterns", []):
        return f"{y_field.replace('_', ' ').title()} Over Time"
    elif chart_type == "bar":
        return f"{y_field.replace('_', ' ').title()} by {x_field.replace('_', ' ').title()}"
    elif chart_type == "pie":
        return f"{y_field.replace('_', ' ').title()} Distribution"
    else:
        return f"{chart_type.title()} Chart"


def _generate_description(chart_config: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    """Auto-generate a chart description based on the data analysis."""
    
    total_records = analysis.get("total_records", 0)
    patterns = analysis.get("data_patterns", [])
    
    desc_parts = [f"Chart showing {total_records} data points"]
    
    if "time_series" in patterns:
        desc_parts.append("with time series analysis")
    if "categorical_breakdown" in patterns:
        desc_parts.append("with categorical breakdown")
    if "multi_metric" in patterns:
        desc_parts.append("with multiple metrics")
        
    return ". ".join(desc_parts) + "."


@tool
def create_custom_dataset(
    dataset_name: str,
    dataset_description: str,
    data_points: List[Dict[str, Any]]
):
    """Create a custom dataset that can be used for charting.
    
    This tool allows you to create structured datasets on the fly that can then be
    visualized using the generate_chart_data tool.
    
    Args:
        dataset_name: Name for the dataset
        dataset_description: Description of what the dataset represents
        data_points: List of dictionaries containing the data points
        
    Returns:
        Dictionary containing the created dataset with metadata
    """
    
    if not data_points:
        return {"error": "No data points provided"}
    
    # Validate data structure
    if not all(isinstance(point, dict) for point in data_points):
        return {"error": "All data points must be dictionaries"}
    
    # Get field information
    all_fields = set()
    for point in data_points:
        all_fields.update(point.keys())
    
    dataset = {
        "name": dataset_name,
        "description": dataset_description,
        "data": data_points,
        "metadata": {
            "total_records": len(data_points),
            "fields": list(all_fields),
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "data_types": {}
        }
    }
    
    # Analyze field types
    for field in all_fields:
        values = [point.get(field) for point in data_points if field in point]
        if values:
            field_analysis = _analyze_field(field, values)
            dataset["metadata"]["data_types"][field] = field_analysis["type"]
    
    return dataset 