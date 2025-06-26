# Universal Chart Generation Guide

This system now supports **universal chart generation** from any aggregated dataset! You can create charts on-the-fly from any structured data.

## 🚀 Key Features

### Automatic Data Analysis
- **Smart field detection**: Automatically detects X/Y axis fields
- **Chart type suggestions**: Recommends optimal chart types based on data patterns
- **Data type inference**: Recognizes dates, percentages, categories, and numeric data
- **Pattern recognition**: Identifies time series, categorical breakdowns, and multi-metric datasets

### Supported Chart Types
- **Line Charts**: Perfect for time series data and trends
- **Bar Charts**: Great for categorical comparisons
- **Pie Charts**: Ideal for percentage distributions
- **Scatter Plots**: Excellent for correlation analysis
- **Multi-series Charts**: Handles multiple data series

## 🛠️ How to Use

### 1. Basic Chart Generation
Simply provide your data and let the system choose the best chart type:

```
"Chart this data: [{'month': 'Jan', 'sales': 1000}, {'month': 'Feb', 'sales': 1200}, {'month': 'Mar', 'sales': 1400}]"
```

### 2. Specific Chart Types
Request a specific chart type:

```
"Create a pie chart from this market share data: [{'company': 'A', 'share': 35}, {'company': 'B', 'share': 28}]"
```

### 3. Sample Data Generation
Generate sample datasets for testing:

```
"Generate sample sales data and create a chart"
"Show me a scatter plot with sample correlation data"
"Create sample market share data and make a pie chart"
```

## 📊 Available Sample Data Tools

### Sales Data
- `get_sample_sales_data(period_months=6)`: Monthly sales with trends
- Perfect for line and bar charts

### Market Share Data
- `get_sample_market_share_data()`: Company market share percentages
- Ideal for pie charts

### Performance Metrics
- `get_sample_performance_metrics()`: Multi-metric department data
- Great for multi-bar charts and comparisons

### Time Series Data
- `get_sample_time_series_data(metric_name="Revenue", days=30)`: Daily time series
- Perfect for line charts and trend analysis

### Scatter Data
- `get_sample_scatter_data(records=50)`: Correlation data points
- Ideal for scatter plots and correlation analysis

## 🎯 Example Workflows

### Quick Demo
```
"Show me what chart types you can create"
→ System generates sample data for each chart type
```

### Data Analysis
```
"Analyze this dataset and suggest the best visualization: [your_data_here]"
→ System analyzes structure and recommends optimal chart type
```

### Custom Visualization
```
"Create a custom dataset with sales by region and chart it as a bar chart"
→ System creates dataset and generates specified chart type
```

## 🔧 Technical Details

### Backend Tools
- **`generate_chart_data`**: Main chart generation engine
- **`create_custom_dataset`**: Custom dataset creation
- **Sample data generators**: Various realistic dataset generators

### Frontend Component
- **`UniversalChart`**: Dynamic chart renderer supporting all chart types
- Automatic styling and responsive design
- Interactive tooltips and legends

### Data Format Support
- JSON strings
- JavaScript objects
- Lists of dictionaries
- Automatic parsing and validation

## 💡 Best Practices

1. **Let the system auto-detect**: Use `chart_type="auto"` for best results
2. **Provide clear field names**: Better field names = better auto-generated titles
3. **Use sample data for demos**: Great for showing capabilities
4. **Combine tools**: Generate sample data + create charts in one workflow
5. **Specify requirements**: Mention chart type preferences if you have them

## 🚦 Getting Started

Try these example commands:

```bash
# Basic chart generation
"Chart this data: [{'category': 'A', 'value': 100}, {'category': 'B', 'value': 150}]"

# Sample data generation
"Generate 12 months of sample sales data and create a line chart"

# Specific chart type
"Create a pie chart showing market share distribution using sample data"

# Data analysis
"What's the best way to visualize department performance metrics?"
```

The system will automatically:
1. Generate or analyze your data
2. Determine the optimal chart type
3. Create chart configuration
4. Return visualization-ready data

Ready to start creating charts from any dataset! 🎉 