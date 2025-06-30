import { makeAssistantToolUI } from '@assistant-ui/react';

type GetNpsScoreToolArgs = {
  country_code: string;
};

type GetNpsScoreToolResult = {
  company_name: string;
  nps_score: number;
  timestamp: string;
};

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-4">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
  </div>
);

const NpsInfoItem = ({ label, value }: { label: string; value: string | number }) => (
  <div>
    <p className="text-gray-600">{label}</p>
    <p className="font-semibold">{value}</p>
  </div>
);

const NpsScoreDisplay = ({ result }: { result: GetNpsScoreToolResult }) => {
  if (!result) return null;

  return (
    <div className="p-4 border rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-4">{result.company_name}</h1>
      <div className="grid grid-cols-2 gap-4">
        <NpsInfoItem label="NPS Score" value={result.nps_score ?? 'N/A'} />
        <NpsInfoItem label="Last Updated" value={new Date(result.timestamp).toLocaleString()} />
      </div>
    </div>
  );
};

export const GetNpsScoreToolUI = makeAssistantToolUI<GetNpsScoreToolArgs, GetNpsScoreToolResult>({
  toolName: 'get_nps_score',
  render: ({ result }) => {
    if (!result) return <LoadingSpinner />;
    return <NpsScoreDisplay result={result} />;
  },
}); 