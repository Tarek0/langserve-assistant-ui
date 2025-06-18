'use client';

import { useState, useEffect } from 'react';

type TrendData = {
  date: string;
  rate: number;
  month_name?: string;
};

type BenchmarkData = {
  industry_average: number;
  target: number;
  status: string;
};

type TrendAnalysis = {
  direction: string;
  change_absolute: number;
  change_percentage: number;
  description: string;
  projection: string;
};

type DeepDetractionRateChartProps = {
  trend: TrendData[];
  benchmark?: BenchmarkData;
  trendAnalysis?: TrendAnalysis;
};

const TrendChart = ({ trend, trendAnalysis }: { 
  trend: TrendData[], 
  trendAnalysis?: TrendAnalysis
}) => {
  const rates = trend.map(d => d.rate);
  const maxRate = Math.max(...rates);
  const minRate = Math.min(...rates);
  const padding = (maxRate - minRate) * 0.15 || 1;
  const chartMax = maxRate + padding;
  const chartMin = Math.max(0, minRate - padding);
  const range = chartMax - chartMin;

  const getBarHeight = (rate: number) => {
    return ((rate - chartMin) / range) * 180 + 20;
  };

  const getBarColor = (rate: number, index: number) => {
    // Use predefined Tailwind classes based on position in trend
    if (trendAnalysis?.direction === 'decreasing') {
      // For improving trends, make bars greener towards the end
      const colors = [
        'from-blue-500 to-blue-400',      // First bar - more blue
        'from-blue-400 to-blue-300',      // Second bar
        'from-blue-300 to-green-300',     // Third bar - transitioning
        'from-green-400 to-green-300',    // Fourth bar - more green
        'from-green-500 to-green-400'     // Last bar - most green
      ];
      return colors[index] || 'from-blue-500 to-blue-400';
    } else if (trendAnalysis?.direction === 'increasing') {
      // For declining trends, make bars redder towards the end
      const colors = [
        'from-blue-500 to-blue-400',      // First bar - blue
        'from-blue-400 to-yellow-300',    // Second bar
        'from-yellow-400 to-yellow-300',  // Third bar - yellow warning
        'from-orange-400 to-orange-300',  // Fourth bar - orange
        'from-red-500 to-red-400'         // Last bar - red alert
      ];
      return colors[index] || 'from-blue-500 to-blue-400';
    }
    // Default blue for all bars if no trend analysis
    return 'from-blue-500 to-blue-400';
  };

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
            const height = getBarHeight(point.rate);
            
            return (
              <div key={index} className="flex flex-col items-center relative group">
                {/* Data point value - always visible */}
                <div className="text-xs font-semibold text-gray-700 mb-2 bg-white px-2 py-1 rounded-md shadow-sm border">
                  {point.rate}%
                </div>
                
                {/* Bar */}
                <div 
                  className={`bg-gradient-to-t ${getBarColor(point.rate, index)} w-12 rounded-t shadow-sm hover:shadow-md transition-shadow cursor-pointer`}
                  style={{ height: `${height}px` }}
                  title={`${point.month_name || point.date}: ${point.rate}%`}
                />
                
                {/* X-axis label */}
                <div className="text-xs text-gray-500 mt-3 text-center">
                  {point.date}
                </div>
              </div>
            );
          })}
        </div>
        
        {/* Simple grid lines */}
        <div className="absolute left-8 right-4 top-6 bottom-16 pointer-events-none">
          <div className="absolute w-full border-t border-gray-50" style={{ top: '0%' }} />
          <div className="absolute w-full border-t border-gray-50" style={{ top: '50%' }} />
          <div className="absolute w-full border-t border-gray-50" style={{ top: '100%' }} />
        </div>
      </div>
    </div>
  );
};

export const DeepDetractionRateChart = ({ trend, trendAnalysis }: DeepDetractionRateChartProps) => {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return <div className="p-4 text-gray-600">Loading chart...</div>;
  }

  if (!trend || trend.length === 0) {
    return <div className="p-4 text-red-600">No trend data available</div>;
  }

  return <TrendChart trend={trend} trendAnalysis={trendAnalysis} />;
}; 