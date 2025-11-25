'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff, Paperclip, Code, FileText, StopCircle, Sparkles, AudioLines, PlusCircle, ArrowUp, Scale, ScrollText, Gavel, BookOpen } from 'lucide-react';
import { useStore } from '@/lib/store';
import { useSound } from '@/hooks/useSound';

interface ChatInputProps {
  onSend: (message: string) => void;
  onStop?: () => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, onStop, disabled }: ChatInputProps) {
  const [input, setInput] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { isGenerating, voice, setVoice, settings, messages } = useStore();
  const { play } = useSound();

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px';
    }
  }, [input]);

  const handleSend = () => {
    if (input.trim() && !disabled && !isGenerating) {
      play('send');
      onSend(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const toggleVoice = async () => {
    if (voice.isListening) {
      setVoice({ isListening: false });
    } else {
      setVoice({ isListening: true, transcript: '' });
    }
  };

  const quickActions = [
    {
      icon: Gavel,
      label: 'Case Law Research',
      action: () => setInput('Find recent HCA precedents regarding '),
    },
    {
      icon: ScrollText,
      label: 'Contract Review',
      action: () => setInput('Review this clause for ambiguity and risk: '),
    },
    {
      icon: FileText,
      label: 'Legal Drafting',
      action: () => setInput('Draft a formal Letter of Demand for '),
    },
    {
        icon: BookOpen,
        label: 'Statutory Analysis',
        action: () => setInput('Explain s 60CC of the Family Law Act regarding '),
    }
  ];

  return (
    <div className="flex-shrink-0 fixed bottom-4 left-4 right-4 md:absolute md:bottom-6 md:left-1/2 md:-translate-x-1/2 md:w-full md:max-w-3xl z-20">
      <div className="w-full">
        {/* Starter Prompts - Floating above input */}
        {messages.length === 0 && !input && (
            <div className="flex items-center justify-center gap-2 mb-4 animate-fade-in-up">
                {quickActions.map((action, i) => (
                    <button
                        key={i}
                        onClick={() => {
                            play('click');
                            action.action();
                            textareaRef.current?.focus();
                        }}
                        className="flex items-center gap-2 px-4 py-2 bg-black/40 backdrop-blur-md border border-white/10 rounded-full text-sm text-zinc-300 hover:bg-white/10 hover:text-white hover:border-cyan-500/30 transition-all active:scale-95 shadow-lg"
                    >
                        <action.icon className="w-3.5 h-3.5 text-cyan-400" />
                        <span>{action.label}</span>
                    </button>
                ))}
            </div>
        )}

        {/* Input Container */}
        <div
          className={`relative flex items-end gap-2 p-2 rounded-[2rem] border transition-all duration-300 ${
            isFocused
              ? 'bg-black/60 border-cyan-500/50 shadow-[0_0_30px_rgba(6,182,212,0.2)] backdrop-blur-xl'
              : 'bg-black/40 border-white/10 hover:border-white/20 backdrop-blur-lg shadow-[0_0_20px_rgba(0,0,0,0.5)]'
          }`}
        >
          {/* Attachment Button - Uniform 44px Target */}
          <button
            className="flex-shrink-0 w-11 h-11 flex items-center justify-center text-zinc-400 hover:text-cyan-400 transition-colors hover:bg-cyan-500/10 rounded-full active:scale-95 group"
            title="Attach file"
          >
            <div className="relative">
                <PlusCircle className="w-6 h-6 group-hover:rotate-90 transition-transform duration-300 stroke-[1.5]" />
            </div>
          </button>

          {/* Textarea - Clean */}
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Message Verridian..."
            disabled={disabled}
            rows={1}
            className="flex-1 py-3 bg-transparent resize-none outline-none text-white placeholder:text-zinc-500 min-h-[44px] max-h-[200px] text-[16px] leading-relaxed"
          />

          {/* Right Side Buttons */}
          <div className="flex items-center gap-2 pr-1">
            {/* Voice Button - Uniform 44px Target */}
            {settings.voiceEnabled && (
              <button
                onClick={() => {
                  play('click');
                  toggleVoice();
                }}
                className={`w-11 h-11 flex items-center justify-center rounded-full transition-all duration-300 ${
                  voice.isListening
                    ? 'bg-red-500 text-white shadow-lg shadow-red-500/40 animate-pulse'
                    : 'text-zinc-400 hover:text-cyan-400 hover:bg-cyan-500/10'
                }`}
                title={voice.isListening ? 'Stop listening' : 'Start voice input'}
              >
                {voice.isListening ? (
                  <AudioLines className="w-6 h-6 animate-wave stroke-[1.5]" />
                ) : (
                  <Mic className="w-6 h-6 stroke-[1.5]" />
                )}
              </button>
            )}

            {/* Send/Stop Button - Uniform 44px Target */}
            {isGenerating ? (
              <button
                onClick={() => {
                  play('click');
                  onStop?.();
                }}
                className="w-11 h-11 flex items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20 transition-all"
                title="Stop generating"
              >
                <div className="w-3 h-3 bg-white rounded-[2px]" />
              </button>
            ) : (
              <button
                onClick={handleSend}
                disabled={!input.trim() || disabled}
                className={`w-11 h-11 flex items-center justify-center rounded-full transition-all transform active:scale-95 ${
                  input.trim()
                    ? 'bg-cyan-600 text-white shadow-lg hover:bg-cyan-500 shadow-cyan-500/30'
                    : 'bg-zinc-800/50 text-zinc-600 cursor-not-allowed'
                }`}
                title="Send message"
              >
                <ArrowUp className="w-6 h-6 stroke-[2]" />
              </button>
            )}
          </div>
        </div>
        
        {/* Centered Helper Text */}
        {/* Helper Text removed as per user request */}
      </div>
    </div>
  );
}
