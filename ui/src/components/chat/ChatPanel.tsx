'use client';

import React, { useRef, useEffect, useCallback } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { useStore } from '@/lib/store';
import { streamChat } from '@/lib/api/gemini';
import type { Message, ToolCall, Artifact } from '@/types';
import {
  Scale, Users, FileText, Clock, Brain,
  ArrowRight, Database, Zap, BookOpen
} from 'lucide-react';

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
    <div className="flex flex-col h-full relative">
      {/* Messages - Centered container matching input width, mobile-optimized padding */}
      <div className="flex-1 overflow-y-auto pb-28 sm:pb-32 flex justify-center">
        <div className="w-full max-w-3xl px-2 sm:px-4 md:px-6">
          {messages.length === 0 ? (
            <WelcomeScreen onSuggestionClick={handleSend} />
          ) : (
            <div className="space-y-3 sm:space-y-4 py-3 sm:py-4">
              {messages.map((message, index) => (
                <div
                  key={message.id}
                  className="animate-fade-in"
                  style={{ animationDelay: `${index * 30}ms` }}
                >
                  <ChatMessage message={message} />
                </div>
              ))}
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <ChatInput
        onSend={handleSend}
        onStop={handleStop}
        disabled={isGenerating}
      />
    </div>
  );
}

function WelcomeScreen({ onSuggestionClick }: { onSuggestionClick: (msg: string) => void }) {
  // Minimal welcome screen to show animation
  return (
    <div className="flex flex-col items-center justify-center min-h-full">
      {/* Empty space to reveal background brain animation */}
    </div>
  );
}
