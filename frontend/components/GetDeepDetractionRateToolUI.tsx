'use client';

import { makeAssistantToolUI } from '@assistant-ui/react';
import { DeepDetractionRateChart } from './charts/DeepDetractionRateChart';

type GetDeepDetractionRateToolArgs = {
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

type GetDeepDetractionRateToolResult = {
  company_name: string;
  deep_detraction_rate: number | string;  // Support both formats
  deep_detraction_rate_formatted?: string;
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

const FollowUpQuestions = ({ result }: { result: GetDeepDetractionRateToolResult }) => {
  const questions = [];
  
  if (result.benchmark) {
    questions.push(`How does ${result.company_name}'s DDR compare to industry benchmarks?`);
  }
  
  if (result.insights && result.insights.length > 0) {
    questions.push(`What are the key insights about ${result.company_name}'s performance?`);
  }
  
  if (result.trend_analysis?.projection) {
    questions.push(`What's the projected DDR trend for ${result.company_name}?`);
  }
  
  // Always include some general follow-up questions
  questions.push(`What factors might be driving this DDR trend?`);
  questions.push(`How can ${result.company_name} improve their DDR further?`);

  return (
    <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <h4 className="text-sm font-medium text-gray-700 mb-3">Learn more:</h4>
      <div className="space-y-2">
        {questions.slice(0, 4).map((question, index) => (
          <button
            key={index}
            className="w-full text-left p-2 text-sm text-blue-700 hover:text-blue-900 hover:bg-blue-50 rounded border border-blue-200 hover:border-blue-300 transition-colors"
            onClick={() => {
              // This would trigger a new query - for now just show the question
              console.log('Follow-up question:', question);
            }}
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
};

const DdrDisplay = ({ result }: { result: GetDeepDetractionRateToolResult }) => {
  if (!result) return null;

  // Handle both old and new data formats
  const currentRate = typeof result.deep_detraction_rate === 'number' 
    ? result.deep_detraction_rate 
    : parseFloat(result.deep_detraction_rate?.toString().replace('%', '') || '0');
  
  const formattedRate = result.deep_detraction_rate_formatted || 
    (typeof result.deep_detraction_rate === 'string' ? result.deep_detraction_rate : `${currentRate}%`);

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
            <p className="text-sm text-gray-600 mt-1">Deep Detraction Rate</p>
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

export const GetDeepDetractionRateToolUI = makeAssistantToolUI<GetDeepDetractionRateToolArgs, GetDeepDetractionRateToolResult>({
  toolName: 'get_deep_detraction_rate',
  render: ({ result }) => {
    if (!result) return <LoadingSpinner />;
    return <DdrDisplay result={result} />;
  },
}); 