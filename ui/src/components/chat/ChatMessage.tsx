'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { User, Sparkles, Code, FileText, Loader2, CheckCircle2, AlertCircle, Clock, ExternalLink, Copy } from 'lucide-react';
import type { Message, Artifact, ToolCall } from '@/types';
import { useStore } from '@/lib/store';

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
        : 'mx-4 md:mx-auto max-w-4xl rounded-2xl bg-blue-900/20 backdrop-blur-md border border-blue-500/10 shadow-lg'
    }`}>
      <div className="max-w-4xl mx-auto flex gap-4">
        {/* Avatar */}
        <div className="flex-shrink-0">
          <div className={`w-9 h-9 rounded-xl flex items-center justify-center shadow-lg ${
            isUser
              ? 'bg-gradient-to-br from-cyan-500 to-blue-600'
              : 'bg-gradient-to-br from-cyan-500 via-blue-600 to-purple-600'
          }`}>
            {isUser ? (
              <User className="w-5 h-5 text-white" />
            ) : (
              <Sparkles className="w-5 h-5 text-white" />
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
            <span className="text-xs text-zinc-600">
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
                <div className="flex gap-1">
                  <div className="w-2 h-2 rounded-full bg-cyan-500 typing-dot" />
                  <div className="w-2 h-2 rounded-full bg-blue-500 typing-dot" />
                  <div className="w-2 h-2 rounded-full bg-purple-500 typing-dot" />
                </div>
                <span className="text-sm">Thinking...</span>
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
                        <code className="bg-blue-900/30 px-1.5 py-0.5 rounded-md text-cyan-400 text-[13px]" {...props}>
                          {children}
                        </code>
                      );
                    }

                    return (
                      <div className="relative group/code my-4">
                        {/* Header */}
                        <div className="flex items-center justify-between px-4 py-2 bg-blue-950/40 border border-blue-500/20 border-b-0 rounded-t-xl">
                          <span className="text-xs text-cyan-400 font-medium">{match[1]}</span>
                          <div className="flex items-center gap-1 opacity-0 group-hover/code:opacity-100 transition-opacity">
                            <button
                              onClick={() => copyToClipboard(codeContent)}
                              className="p-1.5 hover:bg-blue-900/50 rounded-lg transition-colors"
                              title="Copy code"
                            >
                              <Copy className="w-3.5 h-3.5 text-cyan-400" />
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
                              className="p-1.5 hover:bg-blue-900/50 rounded-lg transition-colors"
                              title="Open in Canvas"
                            >
                              <ExternalLink className="w-3.5 h-3.5 text-cyan-400" />
                            </button>
                          </div>
                        </div>
                        {/* Code */}
                        <pre className="bg-black/40 p-4 rounded-b-xl border border-blue-500/20 border-t-0 overflow-x-auto">
                          <code className={`${className} text-[13px]`} {...props}>
                            {children}
                          </code>
                        </pre>
                      </div>
                    );
                  },
                  p({ children }) {
                    return <p className="mb-3 last:mb-0 leading-relaxed text-zinc-200">{children}</p>;
                  },
                  ul({ children }) {
                    return <ul className="mb-3 pl-4 space-y-1 list-disc marker:text-cyan-500">{children}</ul>;
                  },
                  ol({ children }) {
                    return <ol className="mb-3 pl-4 space-y-1 list-decimal marker:text-cyan-500">{children}</ol>;
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
                      <blockquote className="border-l-2 border-cyan-500/50 pl-4 my-3 text-cyan-300/80 italic">
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
                        className="text-cyan-400 hover:text-cyan-300 underline underline-offset-2"
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
                  className="flex items-center gap-2 px-4 py-2.5 glass rounded-xl border border-cyan-500/20 hover:border-cyan-500/50 transition-all group/artifact"
                >
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                    artifact.type === 'code'
                      ? 'bg-cyan-500/20'
                      : 'bg-blue-500/20'
                  }`}>
                    {artifact.type === 'code' ? (
                      <Code className="w-4 h-4 text-cyan-400" />
                    ) : (
                      <FileText className="w-4 h-4 text-blue-400" />
                    )}
                  </div>
                  <div className="text-left">
                    <div className="text-sm font-medium text-zinc-200 group-hover/artifact:text-cyan-300 transition-colors">
                      {artifact.title}
                    </div>
                    <div className="text-xs text-cyan-500/70">{artifact.type}</div>
                  </div>
                  <ExternalLink className="w-4 h-4 text-zinc-600 group-hover/artifact:text-cyan-400 ml-2 transition-colors" />
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
        return <Loader2 className="w-4 h-4 text-cyan-400 animate-spin" />;
      case 'completed':
        return <CheckCircle2 className="w-4 h-4 text-blue-400" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      default:
        return <Clock className="w-4 h-4 text-zinc-500" />;
    }
  };

  const getStatusColor = () => {
    switch (toolCall.status) {
      case 'running':
        return 'border-cyan-500/30 bg-cyan-500/5';
      case 'completed':
        return 'border-blue-500/30 bg-blue-500/5';
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
        className={`inline-flex items-center gap-2 px-3 py-2 rounded-xl border text-sm ${getStatusColor()} ${toolCall.result ? 'cursor-pointer hover:bg-blue-900/20' : ''}`}
      >
        {getStatusIcon()}
        <span className="text-cyan-400 font-medium">{toolCall.name}</span>
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
        <div className="ml-4 p-3 bg-black/40 rounded-lg border border-blue-500/20 text-sm text-cyan-100 whitespace-pre-wrap font-mono max-h-48 overflow-auto">
          {toolCall.result}
        </div>
      )}
    </div>
  );
}
