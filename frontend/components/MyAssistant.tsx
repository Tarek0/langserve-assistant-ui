'use client';

// import { useEdgeRuntime } from "@assistant-ui/react";
import { useChat } from 'ai/react';
import { Thread } from '@assistant-ui/react';
import { makeMarkdownText } from '@assistant-ui/react-markdown';
import { useVercelUseChatRuntime } from '@assistant-ui/react-ai-sdk';
import { GetStockPriceToolUI } from './GetStockPriceToolUI';
import { GetNpsScoreToolUI } from './GetNpsScoreToolUI';
import { GetDeepDetractionRateToolUI } from './GetDeepDetractionRateToolUI';
import { GetChurnRateToolUI } from './GetChurnRateToolUI';
import { ToolFallback } from './ToolFallBack';

const MarkdownText = makeMarkdownText();

export function MyAssistant() {
  // const runtime = useEdgeRuntime({ api: "/api/chat" });
  const chat = useChat({
    api: '/api/chat',
  });

  const runtime = useVercelUseChatRuntime(chat);

  return (
    <Thread
      runtime={runtime}
      assistantMessage={{ components: { Text: MarkdownText, ToolFallback } }}
      tools={[GetStockPriceToolUI, GetNpsScoreToolUI, GetDeepDetractionRateToolUI, GetChurnRateToolUI]}
    />
  );
}
