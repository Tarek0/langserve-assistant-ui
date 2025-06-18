'use client';

import { useState, useEffect } from 'react';

type TrendData = {
  date: string;
  percentage: number;
  month_name: string;
};

type ChurnReason = {
  reason: string;
  current_percentage: number;
  current_count: number;
  severity: 'high' | 'medium' | 'low';
  trend_direction: 'increasing' | 'decreasing' | 'stable';
  historical_trend: TrendData[];
};

type ChartType = 'bar' | 'line';

type ChurnReasonsChartProps = {
  reasons: ChurnReason[];
  chartType?: ChartType;
  selectedReason?: string;
  onChartTypeChange?: (type: ChartType) => void;
  onReasonSelect?: (reason: string) => void;
};

const LineChart = ({ trend, color = 'blue' }: { trend: TrendData[], color?: string }) => {
  const percentages = trend.map(d => d.percentage);
  const maxPercentage = Math.max(...percentages);
  const minPercentage = Math.min(...percentages);
  const padding = (maxPercentage - minPercentage) * 0.1 || 2;
  const chartMax = maxPercentage + padding;
  const chartMin = Math.max(0, minPercentage - padding);
  const range = chartMax - chartMin;

  const getY = (percentage: number) => {
    return 200 - ((percentage - chartMin) / range) * 160; // 160px is the usable height
  };

  const getX = (index: number) => {
    return 40 + (index * (300 / (trend.length - 1))); // 300px width, starting at 40px
  };

  // Generate SVG path for the line
  const pathData = trend.map((point, index) => {
    const x = getX(index);
    const y = getY(point.percentage);
    return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
  }).join(' ');

  // Color classes based on color prop
  const colorClasses = {
    blue: { stroke: 'stroke-blue-500', fill: 'fill-blue-500', bg: 'bg-blue-50' },
    red: { stroke: 'stroke-red-500', fill: 'fill-red-500', bg: 'bg-red-50' },
    green: { stroke: 'stroke-green-500', fill: 'fill-green-500', bg: 'bg-green-50' },
    orange: { stroke: 'stroke-orange-500', fill: 'fill-orange-500', bg: 'bg-orange-50' },
    purple: { stroke: 'stroke-purple-500', fill: 'fill-purple-500', bg: 'bg-purple-50' }
  };

  const currentColor = colorClasses[color as keyof typeof colorClasses] || colorClasses.blue;

  return (
    <div className="w-full">
      <div className="relative bg-white rounded-lg border border-gray-100 p-6 shadow-sm">
        <svg viewBox="0 0 380 240" className="w-full h-60">
          {/* Grid lines */}
          <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f3f4f6" strokeWidth="0.5"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
          
          {/* Y-axis labels */}
          <text x="10" y="25" className="text-xs fill-gray-400">{chartMax.toFixed(1)}%</text>
          <text x="10" y="125" className="text-xs fill-gray-400">{((chartMax + chartMin) / 2).toFixed(1)}%</text>
          <text x="10" y="205" className="text-xs fill-gray-400">{chartMin.toFixed(1)}%</text>
          
          {/* Line path */}
          <path 
            d={pathData}
            className={`${currentColor.stroke} fill-none`}
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          
          {/* Data points */}
          {trend.map((point, index) => {
            const x = getX(index);
            const y = getY(point.percentage);
            
            return (
              <g key={index}>
                {/* Data point circle */}
                <circle 
                  cx={x} 
                  cy={y} 
                  r="4" 
                  className={`${currentColor.fill} stroke-white`}
                  strokeWidth="2"
                />
                
                {/* Data point value */}
                <text 
                  x={x} 
                  y={y - 12} 
                  textAnchor="middle" 
                  className="text-xs font-semibold fill-gray-700"
                >
                  {point.percentage}%
                </text>
                
                {/* X-axis label */}
                <text 
                  x={x} 
                  y="230" 
                  textAnchor="middle" 
                  className="text-xs fill-gray-500"
                >
                  {point.date}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
};

const BarChart = ({ trend, color = 'blue' }: { trend: TrendData[], color?: string }) => {
  const percentages = trend.map(d => d.percentage);
  const maxPercentage = Math.max(...percentages);
  const minPercentage = Math.min(...percentages);
  const padding = (maxPercentage - minPercentage) * 0.15 || 1;
  const chartMax = maxPercentage + padding;
  const chartMin = Math.max(0, minPercentage - padding);
  const range = chartMax - chartMin;

  const getBarHeight = (percentage: number) => {
    return ((percentage - chartMin) / range) * 180 + 20;
  };

  const colorClasses = {
    blue: 'from-blue-500 to-blue-400',
    red: 'from-red-500 to-red-400',
    green: 'from-green-500 to-green-400',
    orange: 'from-orange-500 to-orange-400',
    purple: 'from-purple-500 to-purple-400'
  };

  const currentColor = colorClasses[color as keyof typeof colorClasses] || colorClasses.blue;

  return (
    <div className="w-full">
      <div className="relative bg-white rounded-lg border border-gray-100 p-6 shadow-sm">
        {/* Y-axis labels */}
        <div className="absolute left-0 top-6 bottom-16 flex flex-col justify-between text-xs text-gray-400">
          <span>{chartMax.toFixed(1)}%</span>
          <span>{chartMin.toFixed(1)}%</span>
        </div>
        
        {/* Chart area */}
        <div className="ml-8 h-48 flex items-end justify-between pb-12 relative">
          {trend.map((point, index) => {
            const height = getBarHeight(point.percentage);
            
            return (
              <div key={index} className="flex flex-col items-center relative group">
                {/* Data point value */}
                <div className="text-xs font-semibold text-gray-700 mb-2 bg-white px-2 py-1 rounded-md shadow-sm border">
                  {point.percentage}%
                </div>
                
                {/* Bar */}
                <div 
                  className={`bg-gradient-to-t ${currentColor} w-12 rounded-t shadow-sm hover:shadow-md transition-shadow cursor-pointer`}
                  style={{ height: `${height}px` }}
                  title={`${point.month_name}: ${point.percentage}%`}
                />
                
                {/* X-axis label */}
                <div className="text-xs text-gray-500 mt-3 text-center">
                  {point.date}
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

const ReasonsList = ({ 
  reasons, 
  selectedReason, 
  onReasonSelect 
}: { 
  reasons: ChurnReason[], 
  selectedReason?: string,
  onReasonSelect?: (reason: string) => void 
}) => {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'text-red-600 bg-red-50 border-red-200';
      case 'medium': return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'low': return 'text-green-600 bg-green-50 border-green-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'increasing': return '↗️';
      case 'decreasing': return '↘️';
      case 'stable': return '➡️';
      default: return '—';
    }
  };

  return (
    <div className="space-y-2">
      {reasons.map((reason, index) => (
        <div 
          key={index}
          className={`p-3 rounded-lg border cursor-pointer transition-colors ${
            selectedReason === reason.reason 
              ? 'bg-blue-50 border-blue-200' 
              : 'bg-white border-gray-200 hover:bg-gray-50'
          }`}
          onClick={() => onReasonSelect?.(reason.reason)}
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="font-medium text-gray-900 text-sm">
                {reason.reason}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {reason.current_count.toLocaleString()} customers
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-bold text-gray-700">
                {reason.current_percentage}%
              </span>
              <span className="text-sm">
                {getTrendIcon(reason.trend_direction)}
              </span>
              <span className={`px-2 py-1 rounded text-xs border ${getSeverityColor(reason.severity)}`}>
                {reason.severity}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export const ChurnReasonsChart = ({ 
  reasons, 
  chartType = 'bar',
  selectedReason,
  onChartTypeChange,
  onReasonSelect 
}: ChurnReasonsChartProps) => {
  const [isMounted, setIsMounted] = useState(false);
  const [currentReason, setCurrentReason] = useState(selectedReason || reasons[0]?.reason);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (selectedReason) {
      setCurrentReason(selectedReason);
    }
  }, [selectedReason]);

  if (!isMounted) {
    return <div className="p-4 text-gray-600">Loading chart...</div>;
  }

  if (!reasons || reasons.length === 0) {
    return <div className="p-4 text-red-600">No churn reasons data available</div>;
  }

  const selectedReasonData = reasons.find(r => r.reason === currentReason);
  const reasonColors = ['blue', 'red', 'green', 'orange', 'purple'];
  const currentReasonIndex = reasons.findIndex(r => r.reason === currentReason);
  const chartColor = reasonColors[currentReasonIndex] || 'blue';

  const handleReasonSelect = (reason: string) => {
    setCurrentReason(reason);
    onReasonSelect?.(reason);
  };

  return (
    <div className="space-y-6">
      {/* Chart Type Toggle */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">
          Churn Reasons Trend: {selectedReasonData?.reason}
        </h3>
        <div className="flex bg-gray-100 rounded-lg p-1">
          <button
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              chartType === 'bar' 
                ? 'bg-white text-gray-900 shadow-sm' 
                : 'text-gray-600 hover:text-gray-900'
            }`}
            onClick={() => onChartTypeChange?.('bar')}
          >
            📊 Bar Chart
          </button>
          <button
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              chartType === 'line' 
                ? 'bg-white text-gray-900 shadow-sm' 
                : 'text-gray-600 hover:text-gray-900'
            }`}
            onClick={() => onChartTypeChange?.('line')}
          >
            📈 Line Chart
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Reasons List */}
        <div className="lg:col-span-1">
          <h4 className="text-md font-medium text-gray-700 mb-3">Select Reason to View Trend</h4>
          <ReasonsList 
            reasons={reasons}
            selectedReason={currentReason}
            onReasonSelect={handleReasonSelect}
          />
        </div>

        {/* Chart Display */}
        <div className="lg:col-span-2">
          {selectedReasonData && (
            <>
              {chartType === 'line' ? (
                <LineChart trend={selectedReasonData.historical_trend} color={chartColor} />
              ) : (
                <BarChart trend={selectedReasonData.historical_trend} color={chartColor} />
              )}
              
              {/* Trend Summary */}
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Trend Direction:</span>
                  <span className={`font-medium ${
                    selectedReasonData.trend_direction === 'increasing' ? 'text-red-600' :
                    selectedReasonData.trend_direction === 'decreasing' ? 'text-green-600' :
                    'text-gray-600'
                  }`}>
                    {selectedReasonData.trend_direction === 'increasing' ? '↗️ Increasing' :
                     selectedReasonData.trend_direction === 'decreasing' ? '↘️ Decreasing' :
                     '➡️ Stable'}
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm mt-2">
                  <span className="text-gray-600">Current Impact:</span>
                  <span className="font-medium text-gray-900">
                    {selectedReasonData.current_percentage}% ({selectedReasonData.current_count.toLocaleString()} customers)
                  </span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}; 