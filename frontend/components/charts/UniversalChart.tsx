'use client';

import { useState, useEffect } from 'react';

type ChartData = {
  [key: string]: any;
};

type ChartConfig = {
  type: string;
  data: ChartData[];
  x_field: string;
  y_field: string;
  options: any;
};

type UniversalChartProps = {
  chartType: string;
  title: string;
  description: string;
  config: ChartConfig;
  data: ChartData[];
  className?: string;
};

// Utility function to get color palette
const getColorPalette = (index: number = 0) => {
  const colors = [
    'rgb(59, 130, 246)',   // blue-500
    'rgb(239, 68, 68)',    // red-500
    'rgb(34, 197, 94)',    // green-500
    'rgb(245, 158, 11)',   // yellow-500
    'rgb(168, 85, 247)',   // purple-500
    'rgb(236, 72, 153)',   // pink-500
    'rgb(14, 165, 233)',   // sky-500
    'rgb(249, 115, 22)',   // orange-500
  ];
  return colors[index % colors.length];
};

const LineChart = ({ data, xField, yField, title, options }: { 
  data: ChartData[], 
  xField: string, 
  yField: string,
  title: string,
  options?: any 
}) => {
  if (!data || data.length === 0) {
    return <div className="text-center text-gray-500 p-8">No data available</div>;
  }

  const values = data.map(d => parseFloat(d[yField]) || 0);
  const maxValue = Math.max(...values);
  const minValue = Math.min(...values);
  const padding = (maxValue - minValue) * 0.1 || 2;
  const chartMax = maxValue + padding;
  const chartMin = Math.max(0, minValue - padding);
  const range = chartMax - chartMin;

  const getY = (value: number) => {
    return 200 - ((value - chartMin) / range) * 160;
  };

  const getX = (index: number) => {
    return 40 + (index * (300 / Math.max(data.length - 1, 1)));
  };

  const pathData = data.map((point, index) => {
    const x = getX(index);
    const y = getY(parseFloat(point[yField]) || 0);
    return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
  }).join(' ');

  return (
    <div className="w-full bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      </div>
      <svg viewBox="0 0 380 240" className="w-full h-60">
        {/* Grid lines */}
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f3f4f6" strokeWidth="0.5"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
        
        {/* Y-axis labels */}
        <text x="10" y="25" className="text-xs fill-gray-400">{chartMax.toFixed(1)}</text>
        <text x="10" y="125" className="text-xs fill-gray-400">{((chartMax + chartMin) / 2).toFixed(1)}</text>
        <text x="10" y="205" className="text-xs fill-gray-400">{chartMin.toFixed(1)}</text>
        
        {/* Line path */}
        <path 
          d={pathData}
          stroke={getColorPalette(0)}
          fill="none"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        
        {/* Data points */}
        {data.map((point, index) => {
          const x = getX(index);
          const y = getY(parseFloat(point[yField]) || 0);
          
          return (
            <g key={index}>
              <circle 
                cx={x} 
                cy={y} 
                r="4" 
                fill={getColorPalette(0)}
                stroke="white"
                strokeWidth="2"
              />
              <text 
                x={x} 
                y={y - 12} 
                textAnchor="middle" 
                className="text-xs font-semibold fill-gray-700"
              >
                {point[yField]}
              </text>
              <text 
                x={x} 
                y="230" 
                textAnchor="middle" 
                className="text-xs fill-gray-500"
              >
                {point[xField]}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

const BarChart = ({ data, xField, yField, title, options }: { 
  data: ChartData[], 
  xField: string, 
  yField: string,
  title: string,
  options?: any 
}) => {
  if (!data || data.length === 0) {
    return <div className="text-center text-gray-500 p-8">No data available</div>;
  }

  const values = data.map(d => parseFloat(d[yField]) || 0);
  const maxValue = Math.max(...values);
  const minValue = Math.min(...values);
  const padding = (maxValue - minValue) * 0.15 || 1;
  const chartMax = maxValue + padding;
  const chartMin = Math.max(0, minValue - padding);
  const range = chartMax - chartMin;

  const getBarHeight = (value: number) => {
    return ((value - chartMin) / range) * 180 + 20;
  };

  return (
    <div className="w-full bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      </div>
      <div className="relative">
        {/* Y-axis labels */}
        <div className="absolute left-0 top-6 bottom-16 flex flex-col justify-between text-xs text-gray-400">
          <span>{chartMax.toFixed(1)}</span>
          <span>{chartMin.toFixed(1)}</span>
        </div>
        
        {/* Chart area */}
        <div className="ml-8 h-48 flex items-end justify-between pb-12 relative">
          {data.map((point, index) => {
            const height = getBarHeight(parseFloat(point[yField]) || 0);
            
            return (
              <div key={index} className="flex flex-col items-center relative group">
                <div className="text-xs font-semibold text-gray-700 mb-2 bg-white px-2 py-1 rounded-md shadow-sm border">
                  {point[yField]}
                </div>
                <div 
                  className="w-12 rounded-t shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                  style={{ 
                    height: `${height}px`, 
                    backgroundColor: getColorPalette(index),
                    background: `linear-gradient(to top, ${getColorPalette(index)}, ${getColorPalette(index)}dd)`
                  }}
                  title={`${point[xField]}: ${point[yField]}`}
                />
                <div className="text-xs text-gray-500 mt-3 text-center max-w-16 truncate">
                  {point[xField]}
                </div>
              </div>
            );
          })}
        </div>
        
        {/* Grid lines */}
        <div className="absolute left-8 right-4 top-6 bottom-16 pointer-events-none">
          <div className="absolute w-full border-t border-gray-50" style={{ top: '0%' }} />
          <div className="absolute w-full border-t border-gray-50" style={{ top: '50%' }} />
          <div className="absolute w-full border-t border-gray-50" style={{ top: '100%' }} />
        </div>
      </div>
    </div>
  );
};

const PieChart = ({ data, xField, yField, title, options }: { 
  data: ChartData[], 
  xField: string, 
  yField: string,
  title: string,
  options?: any 
}) => {
  if (!data || data.length === 0) {
    return <div className="text-center text-gray-500 p-8">No data available</div>;
  }

  const total = data.reduce((sum, item) => sum + (parseFloat(item[yField]) || 0), 0);
  let currentAngle = -90; // Start from top

  const createPath = (centerX: number, centerY: number, radius: number, startAngle: number, endAngle: number) => {
    const start = polarToCartesian(centerX, centerY, radius, endAngle);
    const end = polarToCartesian(centerX, centerY, radius, startAngle);
    const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
    return [
      "M", centerX, centerY, 
      "L", start.x, start.y, 
      "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y, 
      "Z"
    ].join(" ");
  };

  const polarToCartesian = (centerX: number, centerY: number, radius: number, angleInDegrees: number) => {
    const angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
    return {
      x: centerX + (radius * Math.cos(angleInRadians)),
      y: centerY + (radius * Math.sin(angleInRadians))
    };
  };

  return (
    <div className="w-full bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      </div>
      <div className="flex items-center justify-center">
        <div className="relative">
          <svg width="300" height="300" className="drop-shadow-sm">
            {data.map((item, index) => {
              const value = parseFloat(item[yField]) || 0;
              const percentage = (value / total) * 100;
              const angle = (value / total) * 360;
              const path = createPath(150, 150, 120, currentAngle, currentAngle + angle);
              currentAngle += angle;
              
              return (
                <path
                  key={index}
                  d={path}
                  fill={getColorPalette(index)}
                  stroke="white"
                  strokeWidth="2"
                  className="hover:opacity-80 transition-opacity cursor-pointer"
                  title={`${item[xField]}: ${percentage.toFixed(1)}%`}
                />
              );
            })}
          </svg>
        </div>
        
        {/* Legend */}
        <div className="ml-6 space-y-2">
          {data.map((item, index) => {
            const value = parseFloat(item[yField]) || 0;
            const percentage = ((value / total) * 100).toFixed(1);
            
            return (
              <div key={index} className="flex items-center space-x-2 text-sm">
                <div 
                  className="w-4 h-4 rounded-sm" 
                  style={{ backgroundColor: getColorPalette(index) }}
                />
                <span className="text-gray-700">
                  {item[xField]}: {percentage}%
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

const ScatterPlot = ({ data, xField, yField, title, options }: { 
  data: ChartData[], 
  xField: string, 
  yField: string,
  title: string,
  options?: any 
}) => {
  if (!data || data.length === 0) {
    return <div className="text-center text-gray-500 p-8">No data available</div>;
  }

  const xValues = data.map(d => parseFloat(d[xField]) || 0);
  const yValues = data.map(d => parseFloat(d[yField]) || 0);
  
  const xMax = Math.max(...xValues);
  const xMin = Math.min(...xValues);
  const yMax = Math.max(...yValues);
  const yMin = Math.min(...yValues);
  
  const xRange = xMax - xMin || 1;
  const yRange = yMax - yMin || 1;
  
  const getX = (value: number) => 40 + ((value - xMin) / xRange) * 300;
  const getY = (value: number) => 200 - ((value - yMin) / yRange) * 160;

  return (
    <div className="w-full bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      </div>
      <svg viewBox="0 0 380 240" className="w-full h-60">
        {/* Grid */}
        <defs>
          <pattern id="scatterGrid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f3f4f6" strokeWidth="0.5"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#scatterGrid)" />
        
        {/* Axes labels */}
        <text x="10" y="25" className="text-xs fill-gray-400">{yMax.toFixed(1)}</text>
        <text x="10" y="205" className="text-xs fill-gray-400">{yMin.toFixed(1)}</text>
        <text x="40" y="230" className="text-xs fill-gray-400">{xMin.toFixed(1)}</text>
        <text x="340" y="230" className="text-xs fill-gray-400">{xMax.toFixed(1)}</text>
        
        {/* Data points */}
        {data.map((point, index) => {
          const x = getX(parseFloat(point[xField]) || 0);
          const y = getY(parseFloat(point[yField]) || 0);
          
          return (
            <circle
              key={index}
              cx={x}
              cy={y}
              r="5"
              fill={getColorPalette(0)}
              stroke="white"
              strokeWidth="2"
              className="hover:r-6 transition-all cursor-pointer"
              title={`${xField}: ${point[xField]}, ${yField}: ${point[yField]}`}
            />
          );
        })}
      </svg>
    </div>
  );
};

export const UniversalChart = ({ 
  chartType, 
  title, 
  description, 
  config, 
  data,
  className = "" 
}: UniversalChartProps) => {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Validate required data
    if (!data || !Array.isArray(data) || data.length === 0) {
      setError("No data provided for chart");
      return;
    }

    if (!config?.x_field || !config?.y_field) {
      setError("Missing required field configuration");
      return;
    }

    setError(null);
  }, [data, config]);

  if (error) {
    return (
      <div className={`bg-red-50 border border-red-200 rounded-lg p-6 ${className}`}>
        <div className="text-red-800 font-medium">Chart Error</div>
        <div className="text-red-600 text-sm mt-1">{error}</div>
      </div>
    );
  }

  const renderChart = () => {
    const chartProps = {
      data: data || config.data,
      xField: config.x_field,
      yField: config.y_field,
      title,
      options: config.options
    };

    switch (chartType.toLowerCase()) {
      case 'line':
      case 'multi-line':
        return <LineChart {...chartProps} />;
      
      case 'bar':
      case 'multi-bar':
        return <BarChart {...chartProps} />;
      
      case 'pie':
        return <PieChart {...chartProps} />;
      
      case 'scatter':
        return <ScatterPlot {...chartProps} />;
      
      default:
        return <BarChart {...chartProps} />; // Default fallback
    }
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {description && (
        <div className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3">
          {description}
        </div>
      )}
      {renderChart()}
      <div className="text-xs text-gray-400 flex justify-between">
        <span>Chart Type: {chartType}</span>
        <span>Data Points: {data?.length || 0}</span>
      </div>
    </div>
  );
};

export default UniversalChart; 