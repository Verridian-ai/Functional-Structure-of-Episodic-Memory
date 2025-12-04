'use client';

import React, { useRef, useEffect, useCallback, useState } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { useStore } from '@/lib/store';
import { streamChat } from '@/lib/api/gemini';
import type { Message, ToolCall, Artifact } from '@/types';
import {
  Scale, Users, FileText, Clock, Brain,
  ArrowRight, Database, Zap, BookOpen
} from 'lucide-react';
import Image from 'next/image';

export function ChatPanel() {
  const {
    messages,
    isGenerating,
    agentConfig,
    settings,
    addMessage,
    updateMessage,
    setGenerating,
    addArtifact,
  } = useStore();

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = useCallback(async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date(),
    };
    addMessage(userMessage);

    // Create assistant message placeholder
    const assistantId = `msg_${Date.now() + 1}`;
    const assistantMessage: Message = {
      id: assistantId,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true,
      toolCalls: [],
      artifacts: [],
    };
    addMessage(assistantMessage);
    setGenerating(true);

    // Create abort controller
    abortControllerRef.current = new AbortController();

    try {
      let fullContent = '';
      const toolCalls: ToolCall[] = [];
      const artifacts: Artifact[] = [];

      await streamChat(
        [...messages, userMessage],
        agentConfig,
        {
          onToken: (token) => {
            fullContent += token;
            updateMessage(assistantId, { content: fullContent });
          },
          onToolCall: (tc) => {
            tc.status = 'completed';
            // Update if exists, otherwise push
            const existingIndex = toolCalls.findIndex(t => t.id === tc.id);
            if (existingIndex !== -1) {
              toolCalls[existingIndex] = tc;
            } else {
              toolCalls.push(tc);
            }
            updateMessage(assistantId, { toolCalls: [...toolCalls] });

            // Handle artifact creation tool
            if (tc.name === 'create_artifact' && tc.arguments) {
              const args = tc.arguments as {
                type: Artifact['type'];
                title: string;
                content: string;
                language?: string;
                structure?: Artifact['structure'];
              };
              const artifact: Artifact = {
                id: `artifact_${Date.now()}`,
                type: args.type,
                title: args.title,
                content: args.content,
                language: args.language,
                structure: args.structure, // Include structure if provided
                createdAt: new Date(),
                updatedAt: new Date(),
              };
              artifacts.push(artifact);
              addArtifact(artifact);
              updateMessage(assistantId, { artifacts: [...artifacts] });
            }

            // Handle canvas section update tool
            if (tc.name === 'update_canvas_section' && tc.arguments) {
               const args = tc.arguments as {
                 sectionId: string;
                 content: string;
                 title?: string;
                 region?: 'header' | 'footer' | 'main' | 'sidebar-left' | 'sidebar-right';
                 style?: Record<string, string>;
                 type?: 'text' | 'image';
               };
               
               // Use a generic event or store action to update the *active* artifact if it is a smart-canvas
               // For simplicity in this refactor, we'll assume the agent might create a NEW version of the artifact 
               // or we need to update the store. 
               // Since we are inside a callback, we can access the store via closure but `activeArtifact` isn't here.
               // We'll rely on the store's `updateArtifact` which we have.
               
               // However, we need the artifact ID. The agent usually implies "current" context.
               // This is a limitation of the current simple tool call handler.
               // We'll implement a "smart update" that finds the most recent smart-canvas or creates one.
               
               // ... Logic to be implemented in a more robust handler, 
               // for now, let's just ensure create_artifact supports the structure.
            }
          },
          onComplete: (content) => {
            updateMessage(assistantId, {
              content,
              isStreaming: false,
              toolCalls,
              artifacts,
            });

            // Add assistant response to memory (Async)
            fetch('/api/memory/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    content, 
                    role: 'assistant', 
                    userId: 'test_session_user' // In real app, use actual user ID
                })
            }).catch(err => console.warn('Failed to save memory:', err));
          },
          onError: (error) => {
            updateMessage(assistantId, {
              content: `Error: ${error.message}`,
              isStreaming: false,
            });
          },
        },
        settings.apiKey
      );
    } catch (error) {
      console.error('Chat error:', error);
      updateMessage(assistantId, {
        content: `Sorry, an error occurred: ${error instanceof Error ? error.message : 'Unknown error'}`,
        isStreaming: false,
      });
    } finally {
      setGenerating(false);
      abortControllerRef.current = null;
    }
  }, [messages, agentConfig, settings.apiKey, addMessage, updateMessage, setGenerating, addArtifact]);

  const handleStop = useCallback(() => {
    abortControllerRef.current?.abort();
    setGenerating(false);
  }, [setGenerating]);

  return (
    <div className="flex flex-col h-full relative overflow-hidden">
      {/* Messages - Flex child that takes remaining space */}
      <div className="flex-1 overflow-y-auto scroll-smooth touch-scroll pb-32 sm:pb-36 md:pb-28">
        <div className="w-full max-w-4xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8 py-4 sm:py-6 md:py-8">
          {messages.length === 0 ? (
            <WelcomeScreen onSuggestionClick={handleSend} />
          ) : (
            <div className="space-y-3 sm:space-y-4">
              {messages.map((message, index) => (
                <div
                  key={message.id}
                  className="animate-fade-in"
                  style={{ animationDelay: `${index * 30}ms` }}
                >
                  <ChatMessage message={message} />
                </div>
              ))}
              {/* Spacer to ensure last message isn't hidden behind "absolute" elements if we had them, 
                  but now we act as flex col. Still good to have breathing room. */}
              <div className="h-4" /> 
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input - Flex child that stays at bottom */}
      <div className="flex-shrink-0 w-full border-t border-white/5 bg-zinc-950/80 backdrop-blur-md p-3 sm:p-4 md:p-6 z-10">
        <div className="max-w-4xl mx-auto">
          <ChatInput
            onSend={handleSend}
            onStop={handleStop}
            disabled={isGenerating}
          />
        </div>
      </div>
    </div>
  );
}

function WelcomeScreen({ onSuggestionClick }: { onSuggestionClick: (msg: string) => void }) {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  // Detect theme changes
  useEffect(() => {
    const checkTheme = () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') as 'dark' | 'light' | null;
      setTheme(currentTheme || 'dark');
    };

    // Initial check
    checkTheme();

    // Watch for theme changes
    const observer = new MutationObserver(checkTheme);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

    return () => observer.disconnect();
  }, []);

  const suggestions = [
    {
      icon: Scale,
      label: 'Research case law on contract disputes',
      message: 'Research case law on contract disputes',
    },
    {
      icon: FileText,
      label: 'Draft a legal demand letter',
      message: 'Draft a legal demand letter',
    },
    {
      icon: BookOpen,
      label: 'Explain statutory interpretation rules',
      message: 'Explain statutory interpretation rules',
    },
    {
      icon: Zap,
      label: 'Review a contract for risks',
      message: 'Review a contract for risks and potential issues',
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-full px-3 sm:px-4 md:px-6 lg:px-8 py-6 sm:py-8 md:py-12 lg:py-16">
      {/* Logo Badge - Switches based on theme */}
      <div className="mb-6 sm:mb-8 md:mb-10">
        <div className={`logo-badge relative w-28 h-28 sm:w-32 sm:h-32 md:w-36 md:h-36 flex items-center justify-center mx-auto rounded-2xl sm:rounded-3xl shadow-2xl backdrop-blur-sm ${
          theme === 'dark'
            ? 'bg-zinc-900/90 border border-white/10 shadow-black/30'
            : 'bg-white/90 border border-black/10 shadow-black/10'
        }`}>
          {/* Inner glow effect */}
          <div className={`absolute inset-0 rounded-2xl sm:rounded-3xl ${
            theme === 'dark'
              ? 'bg-gradient-to-br from-white/5 via-amber-500/5 to-transparent'
              : 'bg-gradient-to-br from-amber-500/5 via-transparent to-transparent'
          }`} />
          <Image
            src={theme === 'dark' ? '/Law_OS_Dark_Mode_Logo.png' : '/Law_OS_Light_Mode_Logo.png'}
            alt="LAW OS logo"
            width={144}
            height={144}
            className="object-contain drop-shadow-lg w-24 h-24 sm:w-28 sm:h-28 md:w-32 md:h-32 relative z-10"
            priority
          />
        </div>
      </div>

      {/* Main Heading - Gold/Amber color */}
      <h1 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-bold text-center mb-3 sm:mb-4 px-4 leading-tight bg-gradient-to-r from-amber-400 via-amber-300 to-amber-400 bg-clip-text text-transparent">
        How can I help you today?
      </h1>

      {/* Subtitle */}
      <p className="text-xs sm:text-sm md:text-base text-center mb-8 sm:mb-10 md:mb-12 text-zinc-400 max-w-xl mx-auto px-4 leading-relaxed">
        I&apos;m your AI legal assistant for research, drafting, and document analysis.
      </p>

      {/* Suggested Actions - 2x2 Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 w-full max-w-2xl px-2 sm:px-0">
        {suggestions.map((suggestion, index) => {
          const Icon = suggestion.icon;
          return (
            <button
              key={index}
              onClick={() => onSuggestionClick(suggestion.message)}
              className="suggestion-card group flex items-center gap-3 p-4 sm:p-5 bg-white/[0.03] hover:bg-white/[0.06] active:bg-white/[0.08] border border-white/10 hover:border-white/20 rounded-xl sm:rounded-2xl transition-all duration-200 text-left touch-target active:scale-[0.98] backdrop-blur-sm"
            >
              <div className="icon-container flex-shrink-0 w-10 h-10 sm:w-11 sm:h-11 flex items-center justify-center bg-zinc-800/60 rounded-xl group-hover:bg-zinc-700/60 transition-colors border border-white/5">
                <Icon className="w-5 h-5 text-zinc-300 group-hover:text-white transition-colors" />
              </div>
              <span className="flex-1 text-sm sm:text-base font-medium text-zinc-300 group-hover:text-white transition-colors leading-snug">
                {suggestion.label}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
