'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff, Paperclip, Code, FileText, StopCircle, Sparkles } from 'lucide-react';
import { useStore } from '@/lib/store';

interface ChatInputProps {
  onSend: (message: string) => void;
  onStop?: () => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, onStop, disabled }: ChatInputProps) {
  const [input, setInput] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { isGenerating, voice, setVoice, settings } = useStore();

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px';
    }
  }, [input]);

  const handleSend = () => {
    if (input.trim() && !disabled && !isGenerating) {
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
      icon: Code,
      label: 'Code',
      action: () => setInput(input + '\n```python\n\n```'),
      color: 'text-green-400 hover:bg-green-500/10',
    },
    {
      icon: FileText,
      label: 'Draft Letter',
      action: () => setInput(input + '\nPlease draft a letter regarding '),
      color: 'text-blue-400 hover:bg-blue-500/10',
    },
  ];

  return (
    <div className="flex-shrink-0 fixed bottom-4 left-4 right-4 md:absolute md:bottom-6 md:left-1/2 md:-translate-x-1/2 md:w-full md:max-w-3xl z-20">
      <div className="w-full">
        {/* Input Container */}
        <div
          className={`relative flex items-end gap-2 p-2 rounded-[2rem] border transition-all duration-300 ${
            isFocused
              ? 'bg-black/60 border-cyan-500/50 shadow-[0_0_30px_rgba(6,182,212,0.2)] backdrop-blur-xl'
              : 'bg-black/40 border-white/10 hover:border-white/20 backdrop-blur-lg shadow-[0_0_20px_rgba(0,0,0,0.5)]'
          }`}
        >
          {/* Attachment Button */}
          <button
            className="flex-shrink-0 p-3 text-zinc-400 hover:text-white transition-colors hover:bg-white/10 rounded-full active:scale-90"
            title="Attach file"
          >
            <Paperclip className="w-5 h-5" />
          </button>

          {/* Textarea */}
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Message Verridian..."
            disabled={disabled}
            rows={3}
            className="flex-1 py-3 bg-transparent resize-none outline-none text-white placeholder:text-zinc-500 min-h-[72px] max-h-[200px] text-[16px]"
          />

          {/* Right Side Buttons */}
          <div className="flex items-center gap-1 pr-1 pb-1">
            {/* Voice Button */}
            {settings.voiceEnabled && (
              <button
                onClick={toggleVoice}
                className={`p-2 rounded-full transition-all ${
                  voice.isListening
                    ? 'bg-red-500/20 text-red-400 pulse-glow'
                    : 'text-zinc-400 hover:text-white hover:bg-white/10'
                }`}
                title={voice.isListening ? 'Stop listening' : 'Start voice input'}
              >
                {voice.isListening ? (
                  <MicOff className="w-5 h-5" />
                ) : (
                  <Mic className="w-5 h-5" />
                )}
              </button>
            )}

            {/* Send/Stop Button */}
            {isGenerating ? (
              <button
                onClick={onStop}
                className="p-2 rounded-full bg-white/10 text-white hover:bg-white/20 transition-all"
                title="Stop generating"
              >
                <div className="w-3 h-3 bg-white rounded-[2px]" />
              </button>
            ) : (
              <button
                onClick={handleSend}
                disabled={!input.trim() || disabled}
                className={`p-2 rounded-full transition-all transform hover:scale-110 active:scale-90 ${
                  input.trim()
                    ? 'bg-cyan-600 text-white shadow-lg hover:bg-cyan-500 shadow-cyan-500/30'
                    : 'bg-zinc-800/50 text-zinc-600 cursor-not-allowed'
                }`}
                title="Send message"
              >
                <Send className="w-4 h-4 ml-0.5" />
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
