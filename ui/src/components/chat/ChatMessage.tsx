'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { User, Sparkles, Code, FileText, Loader2, CheckCircle2, AlertCircle, Clock, ExternalLink, Copy, BrainCircuit } from 'lucide-react';
import type { Message, Artifact, ToolCall } from '@/types';
import { useStore } from '@/lib/store';
import { SynapseLoader } from '../ui/SynapseLoader';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const { addArtifact, setActiveArtifact, toggleCanvas } = useStore();
  const isUser = message.role === 'user';

  const handleArtifactClick = (artifact: Artifact) => {
    addArtifact(artifact);
    setActiveArtifact(artifact.id);
    toggleCanvas();
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className={`group px-4 py-6 transition-colors ${
      isUser 
        ? 'bg-transparent' 
        : 'mx-4 md:mx-auto max-w-4xl rounded-2xl bg-zinc-900/40 backdrop-blur-md border border-white/5 shadow-sm'
    }`}>
      <div className="max-w-4xl mx-auto flex gap-4">
        {/* Avatar */}
        <div className="flex-shrink-0">
          <div className={`w-9 h-9 rounded-xl flex items-center justify-center shadow-lg ${
            isUser
              ? 'bg-zinc-800 text-zinc-400'
              : 'bg-emerald-600 text-white'
          }`}>
            {isUser ? (
              <User className="w-5 h-5" />
            ) : (
              <BrainCircuit className="w-5 h-5" />
            )}
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0 space-y-3">
          {/* Header */}
          <div className="flex items-center gap-2">
            <span className="font-medium text-sm text-zinc-200">
              {isUser ? 'You' : 'Legal AI Assistant'}
            </span>
            <span className="text-xs text-zinc-500">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>

          {/* Tool Calls */}
          {message.toolCalls && message.toolCalls.length > 0 && (
            <div className="space-y-2">
              {message.toolCalls.map((tc) => (
                <ToolCallDisplay key={tc.id} toolCall={tc} />
              ))}
            </div>
          )}

          {/* Message Content */}
          <div className="prose prose-invert prose-sm max-w-none">
            {message.isStreaming && !message.content ? (
              <div className="flex items-center gap-3 text-zinc-400 py-2">
                <SynapseLoader size="sm" />
                <span className="text-sm animate-pulse">Neural Processing...</span>
              </div>
            ) : (
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({ className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '');
                    const isInline = !match;
                    const codeContent = String(children).replace(/\n$/, '');

                    if (isInline) {
                      return (
                        <code className="bg-zinc-800/50 px-1.5 py-0.5 rounded-md text-emerald-400 text-[13px]" {...props}>
                          {children}
                        </code>
                      );
                    }

                    return (
                      <div className="relative group/code my-4">
                        {/* Header */}
                        <div className="flex items-center justify-between px-4 py-2 bg-zinc-900 border border-white/10 border-b-0 rounded-t-xl">
                          <span className="text-xs text-zinc-400 font-medium">{match[1]}</span>
                          <div className="flex items-center gap-1 opacity-0 group-hover/code:opacity-100 transition-opacity">
                            <button
                              onClick={() => copyToClipboard(codeContent)}
                              className="p-1.5 hover:bg-white/5 rounded-lg transition-colors"
                              title="Copy code"
                            >
                              <Copy className="w-3.5 h-3.5 text-zinc-400" />
                            </button>
                            <button
                              onClick={() => handleArtifactClick({
                                id: `artifact_${Date.now()}`,
                                type: 'code',
                                title: `Code (${match[1]})`,
                                content: codeContent,
                                language: match[1],
                                createdAt: new Date(),
                                updatedAt: new Date(),
                              })}
                              className="p-1.5 hover:bg-white/5 rounded-lg transition-colors"
                              title="Open in Canvas"
                            >
                              <ExternalLink className="w-3.5 h-3.5 text-zinc-400" />
                            </button>
                          </div>
                        </div>
                        {/* Code */}
                        <pre className="bg-zinc-950/80 p-4 rounded-b-xl border border-white/10 border-t-0 overflow-x-auto">
                          <code className={`${className} text-[13px]`} {...props}>
                            {children}
                          </code>
                        </pre>
                      </div>
                    );
                  },
                  p({ children }) {
                    return <p className="mb-3 last:mb-0 leading-relaxed text-zinc-300">{children}</p>;
                  },
                  ul({ children }) {
                    return <ul className="mb-3 pl-4 space-y-1 list-disc marker:text-emerald-500">{children}</ul>;
                  },
                  ol({ children }) {
                    return <ol className="mb-3 pl-4 space-y-1 list-decimal marker:text-emerald-500">{children}</ol>;
                  },
                  li({ children }) {
                    return <li className="text-zinc-300">{children}</li>;
                  },
                  h1({ children }) {
                    return <h1 className="text-xl font-bold text-white mb-3 mt-4 first:mt-0">{children}</h1>;
                  },
                  h2({ children }) {
                    return <h2 className="text-lg font-semibold text-white mb-2 mt-4 first:mt-0">{children}</h2>;
                  },
                  h3({ children }) {
                    return <h3 className="text-base font-semibold text-white mb-2 mt-3 first:mt-0">{children}</h3>;
                  },
                  blockquote({ children }) {
                    return (
                      <blockquote className="border-l-2 border-emerald-500/50 pl-4 my-3 text-zinc-400 italic">
                        {children}
                      </blockquote>
                    );
                  },
                  a({ children, href }) {
                    return (
                      <a
                        href={href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-emerald-400 hover:text-emerald-300 underline underline-offset-2"
                      >
                        {children}
                      </a>
                    );
                  },
                }}
              >
                {message.content}
              </ReactMarkdown>
            )}
          </div>

          {/* Artifacts */}
          {message.artifacts && message.artifacts.length > 0 && (
            <div className="flex flex-wrap gap-2 pt-2">
              {message.artifacts.map((artifact) => (
                <button
                  key={artifact.id}
                  onClick={() => handleArtifactClick(artifact)}
                  className="flex items-center gap-2 px-4 py-2.5 bg-zinc-900/50 rounded-xl border border-white/10 hover:border-emerald-500/30 transition-all group/artifact"
                >
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                    artifact.type === 'code'
                      ? 'bg-emerald-900/20'
                      : 'bg-zinc-800'
                  }`}>
                    {artifact.type === 'code' ? (
                      <Code className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <FileText className="w-4 h-4 text-zinc-400 group-hover/artifact:text-emerald-400 transition-colors" />
                    )}
                  </div>
                  <div className="text-left">
                    <div className="text-sm font-medium text-zinc-200 group-hover/artifact:text-emerald-300 transition-colors">
                      {artifact.title}
                    </div>
                    <div className="text-xs text-zinc-500">{artifact.type}</div>
                  </div>
                  <ExternalLink className="w-4 h-4 text-zinc-600 group-hover/artifact:text-emerald-400 ml-2 transition-colors" />
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function ToolCallDisplay({ toolCall }: { toolCall: ToolCall }) {
  const [expanded, setExpanded] = React.useState(false);

  const getStatusIcon = () => {
    switch (toolCall.status) {
      case 'running':
        return <Loader2 className="w-4 h-4 text-emerald-400 animate-spin" />;
      case 'completed':
        return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      default:
        return <Clock className="w-4 h-4 text-zinc-500" />;
    }
  };

  const getStatusColor = () => {
    switch (toolCall.status) {
      case 'running':
        return 'border-emerald-500/30 bg-emerald-500/5';
      case 'completed':
        return 'border-emerald-500/30 bg-emerald-500/5';
      case 'error':
        return 'border-red-500/30 bg-red-500/5';
      default:
        return 'border-zinc-700/50 bg-zinc-800/30';
    }
  };

  return (
    <div className="space-y-2">
      <button
        onClick={() => toolCall.result && setExpanded(!expanded)}
        className={`inline-flex items-center gap-2 px-3 py-2 rounded-xl border text-sm ${getStatusColor()} ${toolCall.result ? 'cursor-pointer hover:bg-white/5' : ''}`}
      >
        {getStatusIcon()}
        <span className="text-emerald-400 font-medium">{toolCall.name}</span>
        {toolCall.arguments && Object.keys(toolCall.arguments).length > 0 && (
          <span className="text-zinc-500 text-xs">
            ({Object.entries(toolCall.arguments).slice(0, 2).map(([k, v]) =>
              `${k}: ${String(v).slice(0, 20)}${String(v).length > 20 ? '...' : ''}`
            ).join(', ')})
          </span>
        )}
        {toolCall.result && (
          <span className="text-zinc-500 text-xs ml-1">
            {expanded ? '▼' : '▶'}
          </span>
        )}
      </button>
      {expanded && toolCall.result && (
        <div className="ml-4 p-3 bg-black/40 rounded-lg border border-white/10 text-sm text-zinc-300 whitespace-pre-wrap font-mono max-h-48 overflow-auto">
          {toolCall.result}
        </div>
      )}
    </div>
  );
}
