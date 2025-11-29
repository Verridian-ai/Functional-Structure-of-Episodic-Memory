'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Mic, FileText, AudioLines, PlusCircle, ArrowUp, ScrollText, Gavel, BookOpen, X } from 'lucide-react';
import { useStore } from '@/lib/store';
import { useSound } from '@/hooks/useSound';

interface AttachedFile {
  file: File;
  preview?: string;
}

interface ChatInputProps {
  onSend: (message: string, files?: File[]) => void;
  onStop?: () => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, onStop, disabled }: ChatInputProps) {
  const [input, setInput] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { isGenerating, voice, setVoice, settings, messages } = useStore();
  const { play } = useSound();
  const prevListening = useRef(voice.isListening);
  // Track the input state *before* the current voice session started
  const inputBeforeListening = useRef('');
  // Ref to hold handleSend for use in effects
  const handleSendRef = useRef<() => void>(() => {});

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px';
    }
  }, [input]);

  // Sync voice transcript to input (Append Logic)
  useEffect(() => {
    if (voice.isListening) {
      // While listening, show base input + current transcript
      // If there was previous text, add a space
      const separator = inputBeforeListening.current && voice.transcript ? ' ' : '';
      setInput(inputBeforeListening.current + separator + voice.transcript);
    }
    // If not listening, we don't force update input from transcript here,
    // we let the cleanup logic handle the final commit.
  }, [voice.transcript, voice.isListening]);

  // Handle listening state changes (Start/Stop)
  useEffect(() => {
    // STARTED LISTENING
    if (!prevListening.current && voice.isListening) {
      // Save current input as base
      inputBeforeListening.current = input;
      play('click'); // Optional: feedback for start
    }

    // STOPPED LISTENING
    if (prevListening.current && !voice.isListening) {
      // Voice stopped. The current 'input' state already contains the full transcript 
      // because of the sync effect above.
      // We just need to check auto-send.
      
      if (settings.voiceAutoSend && input.trim()) {
        handleSendRef.current();
      }
      
      // Reset base input for next time? 
      // Actually, we should update inputBeforeListening to the current input 
      // so if they start again, it appends to this new state.
      inputBeforeListening.current = input;
    }

    prevListening.current = voice.isListening;
  }, [voice.isListening, settings.voiceAutoSend]); // removed 'input' dependency to avoid loop issues

  // Global Spacebar Handler for Push-to-Talk
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      // Only activate if Space is pressed, NOT in an input/textarea (unless it's ours but we want PTT behavior?)
      // User requirement: "hit the spacebar... and hold it in... activates mic"
      // If the user is typing in the box, Space should type a space.
      // So only activate if NOT focused on the textarea, OR if focused but maybe with a modifier?
      // Standard PTT usually works when not focused on a text input.
      
      if (e.code === 'Space' && !e.repeat) {
        // Check if focused element is an input/textarea
        const activeElement = document.activeElement;
        const activeTag = activeElement?.tagName.toLowerCase();
        const isContentEditable = activeElement instanceof HTMLElement && activeElement.isContentEditable;
        const isInputActive = activeTag === 'input' || activeTag === 'textarea' || isContentEditable;

        if (!isInputActive && !voice.isListening && !isGenerating && !disabled) {
          e.preventDefault(); // Prevent scrolling
          setVoice({ isListening: true, transcript: '' });
        }
      }
    };

    const handleGlobalKeyUp = (e: KeyboardEvent) => {
      if (e.code === 'Space') {
        // If we were listening (and it was likely triggered by spacebar PTT), stop.
        // Note: This might stop it even if clicked via button, if they happen to press Space.
        // That's acceptable behavior for a "Hold to Talk" feature.
        if (voice.isListening) {
          e.preventDefault();
          setVoice({ isListening: false });
        }
      }
    };

    window.addEventListener('keydown', handleGlobalKeyDown);
    window.addEventListener('keyup', handleGlobalKeyUp);

    return () => {
      window.removeEventListener('keydown', handleGlobalKeyDown);
      window.removeEventListener('keyup', handleGlobalKeyUp);
    };
  }, [voice.isListening, isGenerating, disabled, setVoice]);


  const handleSend = React.useCallback(() => {
    if ((input.trim() || attachedFiles.length > 0) && !disabled && !isGenerating) {
      play('send');
      const files = attachedFiles.map(af => af.file);
      onSend(input.trim(), files.length > 0 ? files : undefined);
      setInput('');
      setAttachedFiles([]);
    }
  }, [input, attachedFiles, disabled, isGenerating, play, onSend]);

  // Keep ref updated for use in effects
  useEffect(() => {
    handleSendRef.current = handleSend;
  }, [handleSend]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    const newFiles: AttachedFile[] = [];
    Array.from(files).forEach(file => {
      const preview = file.type.startsWith('image/')
        ? URL.createObjectURL(file)
        : undefined;
      newFiles.push({ file, preview });
    });

    setAttachedFiles(prev => [...prev, ...newFiles]);
    play('click');

    // Reset input so same file can be selected again
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeFile = (index: number) => {
    setAttachedFiles(prev => {
      const newFiles = [...prev];
      // Revoke object URL if it exists
      if (newFiles[index].preview) {
        URL.revokeObjectURL(newFiles[index].preview!);
      }
      newFiles.splice(index, 1);
      return newFiles;
    });
    play('click');
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
    play('click');
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
      label: 'Find Precedents',
      action: () => setInput('Find case law regarding '),
    },
    {
      icon: ScrollText,
      label: 'Review Contract',
      action: () => setInput('Review this contract clause for risk: '),
    },
    {
      icon: FileText,
      label: 'Draft Letter',
      action: () => setInput('Draft a formal Letter of Demand for '),
    },
    {
        icon: BookOpen,
        label: 'Explain Statute',
        action: () => setInput('Explain Section 60CC of the Family Law Act in relation to '),
    }
  ];

  return (
    <div className="flex-shrink-0 fixed bottom-0 left-0 right-0 p-4 md:absolute md:bottom-6 md:left-1/2 md:-translate-x-1/2 md:w-full md:max-w-3xl z-20 safe-area-pb">
      <div className="w-full">
        {/* Starter Prompts - Floating above input, scrollable on mobile */}
        {messages.length === 0 && !input && (
            <div className="flex items-center justify-start md:justify-center gap-2 mb-4 animate-fade-in-up overflow-x-auto pb-2 -mx-4 px-4 md:mx-0 md:px-0 scrollbar-hide">
                {quickActions.map((action, i) => (
                    <button
                        key={i}
                        onClick={() => {
                            play('click');
                            action.action();
                            textareaRef.current?.focus();
                        }}
                        className="flex items-center gap-2 px-3 md:px-4 py-2 bg-black/40 backdrop-blur-md border border-white/10 rounded-full text-xs md:text-sm text-zinc-300 hover:bg-white/10 hover:text-white hover:border-emerald-500/30 transition-all active:scale-95 shadow-lg whitespace-nowrap flex-shrink-0"
                    >
                        <action.icon className="w-3 h-3 md:w-3.5 md:h-3.5 text-emerald-400" />
                        <span className="hidden sm:inline">{action.label}</span>
                        <span className="sm:hidden">{action.label.split(' ')[0]}</span>
                    </button>
                ))}
            </div>
        )}

        {/* Attached Files Preview */}
        {attachedFiles.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3 px-2 animate-fade-in">
            {attachedFiles.map((af, index) => (
              <div
                key={index}
                className="relative group flex items-center gap-2 px-3 py-2 bg-black/50 backdrop-blur-md border border-white/10 rounded-xl"
              >
                {af.preview ? (
                  <img
                    src={af.preview}
                    alt={af.file.name}
                    className="w-8 h-8 object-cover rounded"
                  />
                ) : (
                  <FileText className="w-5 h-5 text-emerald-400" />
                )}
                <span className="text-sm text-zinc-300 max-w-[120px] truncate">
                  {af.file.name}
                </span>
                <button
                  onClick={() => removeFile(index)}
                  className="ml-1 p-1 text-zinc-500 hover:text-red-400 hover:bg-red-500/10 rounded-full transition-colors"
                  title="Remove file"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}

          {/* Input Container */}
        <div
          className={`relative flex items-end gap-2 p-2 rounded-[2rem] border transition-all duration-300 ${
            isFocused
              ? 'bg-black/60 border-emerald-500/50 shadow-[0_0_30px_rgba(16,185,129,0.2)] backdrop-blur-xl'
              : 'bg-black/40 border-white/10 hover:border-white/20 backdrop-blur-lg shadow-[0_0_20px_rgba(0,0,0,0.5)]'
          }`}
        >
          {/* Hidden File Input */}
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg,.gif,.webp"
            onChange={handleFileSelect}
            className="hidden"
          />

          {/* Attachment Button - Uniform 44px Target */}
          <button
            onClick={triggerFileInput}
            className="flex-shrink-0 w-11 h-11 flex items-center justify-center text-zinc-400 hover:text-emerald-400 transition-colors hover:bg-emerald-500/10 rounded-full active:scale-95 group"
            title="Attach file"
          >
            <div className="relative">
                <PlusCircle className="w-6 h-6 group-hover:rotate-90 transition-transform duration-300 stroke-[1.5]" />
                {attachedFiles.length > 0 && (
                  <span className="absolute -top-1 -right-1 w-4 h-4 bg-emerald-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                    {attachedFiles.length}
                  </span>
                )}
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
                    : 'text-zinc-400 hover:text-emerald-400 hover:bg-emerald-500/10'
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
                disabled={(!input.trim() && attachedFiles.length === 0) || disabled}
                className={`w-11 h-11 flex items-center justify-center rounded-full transition-all transform active:scale-95 ${
                  input.trim() || attachedFiles.length > 0
                    ? 'bg-emerald-600 text-white shadow-lg hover:bg-emerald-500 shadow-emerald-500/30'
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
