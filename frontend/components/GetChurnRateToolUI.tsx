'use client';

import { makeAssistantToolUI } from '@assistant-ui/react';
import { DeepDetractionRateChart } from './charts/DeepDetractionRateChart';

type GetChurnRateToolArgs = {
  country_code: string;
};

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

type GetChurnRateToolResult = {
  company_name: string;
  churn_rate: number | string;  // Support both formats
  churn_rate_formatted?: string;
  status?: string;
  benchmark?: BenchmarkData;
  trend: TrendData[];
  trend_analysis?: TrendAnalysis;
  insights?: string[];
  timestamp: string;
  last_updated_formatted?: string;
};

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-6">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
  </div>
);

const StatusBadge = ({ status }: { status?: string }) => {
  if (!status) return null;
  
  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'improving':
        return { color: 'bg-green-100 text-green-800', icon: '↗️', text: 'improving' };
      case 'declining':
        return { color: 'bg-red-100 text-red-800', icon: '↘️', text: 'declining' };
      default:
        return { color: 'bg-yellow-100 text-yellow-800', icon: '→', text: 'stable' };
    }
  };

  const config = getStatusConfig(status);
  return (
    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${config.color} ml-2`}>
      <span className="mr-1">{config.icon}</span>
      {config.text}
    </span>
  );
};

const FollowUpQuestions = ({ result }: { result: GetChurnRateToolResult }) => {
  const questions = [];
  
  // Handle both old and new data formats for comparisons
  const currentRate = typeof result.churn_rate === 'number' 
    ? result.churn_rate 
    : parseFloat(result.churn_rate?.toString().replace('%', '') || '0');
  
  // Segmentation questions
  questions.push(`Do you want to split this churn rate by product or customer type?`);
  questions.push(`Would you like to see this broken down by customer segment (enterprise vs consumer)?`);
  questions.push(`Do you want to analyze this by subscription plan (prepaid vs postpaid)?`);
  
  // Comparative analysis based on performance
  if (result.benchmark) {
    if (currentRate > result.benchmark.industry_average) {
      questions.push(`How does ${result.company_name}'s churn rate compare to top-performing competitors?`);
    } else {
      questions.push(`How does this compare to other Vodafone markets?`);
    }
  }
  
  // Trend-based questions
  if (result.trend_analysis) {
    if (result.trend_analysis.direction === 'decreasing') {
      questions.push(`What retention initiatives are driving this churn rate improvement?`);
      questions.push(`What's the ROI impact of reaching the target retention rate?`);
    } else if (result.trend_analysis.direction === 'increasing') {
      questions.push(`What are the main drivers behind this churn rate increase?`);
      questions.push(`What immediate retention actions could reverse this trend?`);
    } else {
      questions.push(`What could drive breakthrough improvement in customer retention?`);
    }
  }
  
  // Time-based analysis
  questions.push(`Would you like to see quarterly trends or seasonal patterns?`);
  questions.push(`How does this compare to the same period last year?`);
  
  // Root cause and correlation
  questions.push(`How does this churn rate correlate with customer satisfaction scores?`);
  questions.push(`Would you like to see the impact of recent retention campaigns?`);
  
  // Action-oriented questions
  if (result.benchmark?.target) {
    const gapToTarget = Math.abs(currentRate - result.benchmark.target);
    questions.push(`What would be the business impact of closing the ${gapToTarget.toFixed(1)}% gap to target?`);
  }
  
  // Predictive questions
  questions.push(`Would you like to see forecasts for the next quarter?`);
  questions.push(`What's the projected impact if current trends continue?`);
  
  // Customer journey and touchpoint analysis
  questions.push(`Which customer touchpoints most influence churn decisions?`);
  questions.push(`Do you want to analyze this by customer tenure (new vs existing)?`);

  return (
    <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <h4 className="text-sm font-medium text-gray-700 mb-3">Explore further:</h4>
      <div className="space-y-2">
        {questions.slice(0, 6).map((question, index) => (
          <button
            key={index}
            className="w-full text-left p-3 text-sm text-blue-700 hover:text-blue-900 hover:bg-blue-50 rounded-md border border-blue-200 hover:border-blue-300 transition-colors"
            onClick={() => {
              // This would trigger a new query - for now just show the question
              console.log('Follow-up question:', question);
            }}
          >
            {question}
          </button>
        ))}
      </div>
      
      {questions.length > 6 && (
        <button className="mt-2 text-xs text-gray-500 hover:text-gray-700 underline">
          Show more analysis options...
        </button>
      )}
    </div>
  );
};

const ChurnRateDisplay = ({ result }: { result: GetChurnRateToolResult }) => {
  if (!result) return null;

  // Handle both old and new data formats
  const currentRate = typeof result.churn_rate === 'number' 
    ? result.churn_rate 
    : parseFloat(result.churn_rate?.toString().replace('%', '') || '0');
  
  const formattedRate = result.churn_rate_formatted || 
    (typeof result.churn_rate === 'string' ? result.churn_rate : `${currentRate}%`);

  // Calculate basic trend analysis if not provided
  const trendData = result.trend || [];
  const basicTrendAnalysis = trendData.length > 1 ? {
    direction: trendData[0].rate > trendData[trendData.length - 1].rate ? 'decreasing' : 'increasing',
    change_absolute: trendData[trendData.length - 1].rate - trendData[0].rate,
    change_percentage: ((trendData[trendData.length - 1].rate - trendData[0].rate) / trendData[0].rate) * 100,
    description: `The rate has ${trendData[0].rate > trendData[trendData.length - 1].rate ? 'decreased' : 'increased'} from ${trendData[0].rate}% to ${trendData[trendData.length - 1].rate}% over the period.`,
    projection: ''
  } : undefined;

  return (
    <div className="w-full max-w-3xl bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-900">{result.company_name}</h2>
            <p className="text-sm text-gray-600 mt-1">Churn Rate</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        {/* Current Rate */}
        <div className="text-center mb-6">
          <div className="inline-flex items-baseline">
            <span className="text-4xl font-bold text-gray-900">{formattedRate}</span>
            <StatusBadge status={result.status} />
          </div>
          {result.trend_analysis && (
            <p className="text-sm text-gray-600 mt-2">
              {result.trend_analysis.change_absolute > 0 ? '+' : ''}{result.trend_analysis.change_absolute}% 
              over 5 months
            </p>
          )}
        </div>

        {/* Chart */}
        {result.trend && result.trend.length > 0 && (
          <div className="mb-6">
            <DeepDetractionRateChart 
              trend={result.trend} 
              trendAnalysis={result.trend_analysis || basicTrendAnalysis}
            />
          </div>
        )}

        {/* Follow-up Questions */}
        <FollowUpQuestions result={result} />

        {/* Footer */}
        <div className="mt-6 pt-4 border-t border-gray-100">
          <p className="text-xs text-gray-400 text-center">
            Last updated: {result.last_updated_formatted || new Date(result.timestamp).toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  );
};

export const GetChurnRateToolUI = makeAssistantToolUI<GetChurnRateToolArgs, GetChurnRateToolResult>({
  toolName: 'get_churn_rate',
  render: ({ result }) => {
    if (!result) return <LoadingSpinner />;
    return <ChurnRateDisplay result={result} />;
  },
}); 