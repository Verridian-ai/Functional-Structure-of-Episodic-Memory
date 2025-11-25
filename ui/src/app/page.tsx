'use client';

import React, { useCallback, useEffect, useState } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { ChatPanel } from '@/components/chat/ChatPanel';
import { CanvasPanel } from '@/components/canvas/CanvasPanel';
import { AdminPanel } from '@/components/admin/AdminPanel';
import { VoicePanel } from '@/components/voice/VoicePanel';
import { useStore } from '@/lib/store';
import { X } from 'lucide-react';

export default function Home() {
  const {
    showCanvas,
    clearMessages,
    addConversation,
    setCurrentConversation,
    toggleCanvas
  } = useStore();

  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handleNewChat = useCallback(() => {
    const newConversation = {
      id: `conv_${Date.now()}`,
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    addConversation(newConversation);
    setCurrentConversation(newConversation.id);
    clearMessages();
  }, [addConversation, setCurrentConversation, clearMessages]);

  const handleVoiceTranscript = useCallback((text: string) => {
    // The voice transcript will be handled by the ChatInput component
    // through the store's voice state
    console.log('Voice transcript:', text);
  }, []);

  return (
    <MainLayout onNewChat={handleNewChat}>
      <div className="flex h-full relative">
        {/* Main Chat Area */}
        <div className={`flex-1 min-w-0 h-full ${showCanvas && !isMobile ? 'border-r border-cyan-500/20' : ''}`}>
          <ChatPanel />
        </div>

        {/* Canvas Panel */}
        {showCanvas && (
          <div 
            className={`
                ${isMobile ? 'fixed inset-0 z-50 bg-black/95 backdrop-blur-xl' : 'w-[500px] flex-shrink-0 relative'}
                transition-all duration-300 ease-in-out border-l border-cyan-500/20 shadow-2xl shadow-cyan-500/5
            `}
          >
            {isMobile && (
                <button 
                    onClick={toggleCanvas}
                    className="absolute top-4 right-4 p-2 bg-zinc-800 rounded-full z-50"
                >
                    <X className="w-5 h-5 text-zinc-400" />
                </button>
            )}
            <CanvasPanel />
          </div>
        )}
      </div>

      {/* Admin Panel (Modal) */}
      <AdminPanel />

      {/* Voice Panel */}
      <VoicePanel onTranscript={handleVoiceTranscript} />
    </MainLayout>
  );
}
