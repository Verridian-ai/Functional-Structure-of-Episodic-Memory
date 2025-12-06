'use client';

import React, { useCallback, useEffect, useState, lazy, Suspense } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { ChatPanel } from '@/components/chat/ChatPanel';
import { CanvasPanel } from '@/components/canvas/CanvasPanel';
import { useStore } from '@/lib/store';
import { X } from 'lucide-react';
import { ErrorBoundary } from '@/components/ui/ErrorBoundary';
import { ToastProvider } from '@/components/ui/Toast';
import { SynapseLoader } from '@/components/ui/SynapseLoader';
import {
  OnboardingProvider,
  OnboardingTooltip,
  OnboardingModal,
  HelpButton,
} from '@/components/onboarding';

// Lazy load less critical components
const AdminPanel = lazy(() => import('@/components/admin/AdminPanel').then(m => ({ default: m.AdminPanel })));
const VoicePanel = lazy(() => import('@/components/voice/VoicePanel').then(m => ({ default: m.VoicePanel })));

export default function Home() {
  const {
    showCanvas,
    clearMessages,
    addConversation,
    setCurrentConversation,
    toggleCanvas
  } = useStore();

  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);

  useEffect(() => {
    const checkViewport = () => {
      const width = window.innerWidth;
      setIsMobile(width < 768);
      setIsTablet(width >= 768 && width < 1024);
    };
    checkViewport();
    window.addEventListener('resize', checkViewport);
    return () => window.removeEventListener('resize', checkViewport);
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
    <ToastProvider position="bottom-center">
      <ErrorBoundary showDetails={process.env.NODE_ENV === 'development'}>
        <OnboardingProvider>
          {/* Onboarding components */}
          <OnboardingModal />
          <OnboardingTooltip />
          <HelpButton />

          <MainLayout onNewChat={handleNewChat}>
            <div className="flex h-full relative">
              {/* Main Chat Area */}
              <div className={`flex-1 min-w-0 h-full ${showCanvas && !isMobile ? 'border-r border-cyan-500/20' : ''}`}>
                <ErrorBoundary>
                  <ChatPanel />
                </ErrorBoundary>
              </div>

              {/* Canvas Panel */}
              {showCanvas && (
                <div
                  className={`
                      ${isMobile
                        ? 'fixed inset-0 z-50 bg-black/95 backdrop-blur-xl safe-area-inset'
                        : isTablet
                          ? 'w-full max-w-full md:w-[340px] flex-shrink-0 relative'
                          : 'w-full max-w-full md:w-[360px] lg:w-[440px] xl:w-[520px] flex-shrink-0 relative'}
                      transition-all duration-300 ease-in-out border-l border-cyan-500/20 shadow-2xl shadow-cyan-500/5
                  `}
                >
                  {isMobile && (
                      <button
                          onClick={toggleCanvas}
                          className="absolute top-4 right-4 p-2.5 sm:p-3 bg-zinc-800/80 hover:bg-zinc-700/80 rounded-full z-50 touch-target transition-colors"
                          aria-label="Close canvas"
                      >
                          <X className="w-5 h-5 sm:w-6 sm:h-6 text-zinc-300" />
                      </button>
                  )}
                  <ErrorBoundary>
                    <CanvasPanel />
                  </ErrorBoundary>
                </div>
              )}
            </div>

            {/* Admin Panel (Modal) - Lazy loaded */}
            <Suspense fallback={null}>
              <AdminPanel />
            </Suspense>

            {/* Voice Panel - Lazy loaded */}
            <Suspense fallback={null}>
              <VoicePanel onTranscript={handleVoiceTranscript} />
            </Suspense>
          </MainLayout>
        </OnboardingProvider>
      </ErrorBoundary>
    </ToastProvider>
  );
}
