'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import {
  MessageSquare, FileText, Settings, Menu, Plus,
  ChevronLeft, Trash2, Brain
} from 'lucide-react';
import { useStore } from '@/lib/store';
import { VerridianBrainUltimate } from '@/components/ui/VerridianBrainUltimate';

interface MainLayoutProps {
  children: React.ReactNode;
  onNewChat: () => void;
}

export function MainLayout({ children, onNewChat }: MainLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const {
    conversations,
    currentConversationId,
    setCurrentConversation,
    deleteConversation,
    toggleAdmin,
    toggleCanvas,
    showCanvas,
  } = useStore();

  // Touch handling for swipe gestures
  const [touchStart, setTouchStart] = useState<number | null>(null);

  const handleTouchStart = (e: React.TouchEvent) => {
    setTouchStart(e.targetTouches[0].clientX);
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (touchStart === null) return;
    
    const touchEnd = e.changedTouches[0].clientX;
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > 50;
    const isRightSwipe = distance < -50;

    if (isLeftSwipe && sidebarOpen) {
      setSidebarOpen(false);
    }
    
    if (isRightSwipe && !sidebarOpen && touchStart < 30) { // Only open if start from left edge
      setSidebarOpen(true);
    }
    
    setTouchStart(null);
  };

  // Mobile responsiveness: close sidebar by default on mobile
  useEffect(() => {
    const handleResize = () => {
        if (window.innerWidth < 768) {
            setSidebarOpen(false);
        } else {
            setSidebarOpen(true);
        }
    };
    
    // Initial check
    handleResize();

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);


  const filteredConversations = conversations.filter(c =>
    c.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div 
      className="flex h-screen bg-zinc-950 text-white overflow-hidden relative"
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      {/* 3D Brain Background */}
      <VerridianBrainUltimate />

      {/* Subtle gradient overlay */}
      <div className="fixed inset-0 gradient-mesh pointer-events-none z-[1]" />
      
      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div 
            className="fixed inset-0 bg-black/50 z-20 md:hidden backdrop-blur-sm"
            onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
            fixed md:relative z-30 h-full
            ${sidebarOpen ? 'translate-x-0 w-[280px] sm:w-[300px] md:w-80' : '-translate-x-full md:translate-x-0 md:w-0'}
            flex flex-col bg-zinc-950/80 backdrop-blur-3xl border-r border-white/5 transition-all duration-300 overflow-hidden shadow-2xl
        `}
      >
        {/* Sidebar Header Section */}
        <div className="flex-shrink-0 pt-4 sm:pt-6 md:pt-8 pb-4 sm:pb-6 border-b border-white/5" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
          <div className="flex justify-center mb-4 sm:mb-6 md:mb-8">
            <div className="relative w-24 h-24 sm:w-32 sm:h-32 md:w-40 md:h-40 flex items-center justify-center hover:scale-105 transition-transform duration-300">
              <Image
                src="/verridian_logo_new.png"
                alt="Verridian"
                fill
                className="object-contain drop-shadow-2xl"
                priority
              />
            </div>
          </div>

          {/* New Chat Button - Compact size */}
          <button
            id="new-project-button"
            onClick={() => {
                onNewChat();
                if (window.innerWidth < 768) setSidebarOpen(false);
            }}
            className="group flex items-center gap-2.5 px-3 h-10 bg-white/5 hover:bg-white/10 border border-white/10 text-white rounded-lg font-medium shadow-lg transition-all active:scale-[0.98]"
          >
            <div className="w-6 h-6 flex items-center justify-center bg-white/5 rounded-md group-hover:bg-white/10 transition-colors flex-shrink-0">
                <Plus className="w-3.5 h-3.5 text-white stroke-[2.5]" />
            </div>
            <span className="tracking-wide text-sm">New Project</span>
          </button>
        </div>

        {/* Search Section - Compact */}
        <div className="flex-shrink-0 py-3 border-b border-white/5 bg-white/[0.02]" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search projects..."
            className="h-9 px-3 bg-black/40 border border-zinc-800 rounded-lg text-sm text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:bg-black/60 focus:border-zinc-700 focus:ring-1 focus:ring-zinc-700 transition-all"
            style={{ width: '180px' }}
          />
        </div>

        {/* Recent Activity Label - Compact */}
        <div className="pt-3 pb-2 flex items-center justify-between border-b border-white/5 bg-white/[0.02]" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
            <span className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider">Recents</span>
            <span className="text-[10px] text-zinc-500 font-mono bg-white/5 px-1.5 py-0.5 rounded">{filteredConversations.length}</span>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto py-2 space-y-1 custom-scrollbar" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
          {filteredConversations.length === 0 ? (
            <div className="text-center py-8 px-3">
              <div className="w-10 h-10 mx-auto mb-2 rounded-lg bg-zinc-900/50 border border-dashed border-zinc-800 flex items-center justify-center">
                <MessageSquare className="w-4 h-4 text-zinc-700" />
              </div>
              <p className="text-xs text-zinc-600 font-medium">
                {searchQuery ? 'No matches found' : 'No history yet'}
              </p>
            </div>
          ) : (
            <div className="space-y-1 sm:space-y-1.5">
              {filteredConversations.map((conv, index) => (
                <div
                  key={conv.id}
                  className={`group relative flex items-center gap-2.5 sm:gap-3.5 p-2.5 sm:p-3.5 rounded-xl sm:rounded-2xl cursor-pointer transition-all duration-200 border touch-target ${
                    conv.id === currentConversationId
                      ? 'bg-white/10 border-white/10 shadow-md'
                      : 'hover:bg-white/5 border-transparent hover:border-white/5 active:bg-white/5'
                  }`}
                  onClick={() => {
                      setCurrentConversation(conv.id);
                      if (window.innerWidth < 768) setSidebarOpen(false);
                  }}
                >
                  <div className={`w-8 h-8 sm:w-10 sm:h-10 rounded-lg sm:rounded-xl flex items-center justify-center flex-shrink-0 transition-colors ${
                    conv.id === currentConversationId
                      ? 'bg-white/10 text-white'
                      : 'bg-zinc-900 text-zinc-600 group-hover:text-zinc-400 group-hover:bg-zinc-800'
                  }`}>
                    <MessageSquare className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                  </div>

                  <div className="flex-1 min-w-0 py-0.5">
                    <div className={`text-xs sm:text-sm font-medium truncate mb-0.5 ${
                      conv.id === currentConversationId ? 'text-white' : 'text-zinc-400 group-hover:text-zinc-200'
                    }`}>
                      {conv.title}
                    </div>
                    <div className="flex items-center gap-1.5 sm:gap-2 text-[10px] sm:text-xs text-zinc-600 group-hover:text-zinc-500">
                        <span className="hidden sm:inline">{new Date().toLocaleDateString()}</span>
                        <span className="sm:hidden">{new Date().toLocaleDateString('en', { month: 'short', day: 'numeric' })}</span>
                        <span className="w-0.5 h-0.5 rounded-full bg-zinc-600" />
                        <span>{conv.messages.length} msgs</span>
                    </div>
                  </div>

                  {/* Delete button - Always visible on mobile, hover on desktop */}
                  <div className="flex-shrink-0 opacity-100 sm:opacity-0 group-hover:opacity-100 transition-opacity flex items-center">
                    <button
                        onClick={(e) => {
                        e.stopPropagation();
                        deleteConversation(conv.id);
                        }}
                        className="p-2 sm:p-2 text-zinc-500 hover:text-red-400 active:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors touch-target"
                        title="Delete"
                    >
                        <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Sidebar Footer - Compact */}
        <div className="flex-shrink-0 py-3 border-t border-white/10 bg-black/20 safe-area-pb" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
            <div className="flex items-center gap-2">
                <button
                    id="canvas-toggle-button"
                    onClick={() => {
                        toggleCanvas();
                        if (window.innerWidth < 768) setSidebarOpen(false);
                    }}
                    className={`group flex items-center gap-2 px-3 h-9 rounded-lg text-sm font-medium transition-all ${
                    showCanvas
                        ? 'bg-white/10 text-white border border-white/10'
                        : 'hover:bg-white/5 text-zinc-400 hover:text-zinc-200 border border-transparent'
                    }`}
                >
                    <FileText className="w-4 h-4 stroke-[1.5] flex-shrink-0" />
                    <span>Canvas</span>
                </button>

                <button
                    onClick={toggleAdmin}
                    className="flex items-center gap-2 px-3 h-9 rounded-lg text-sm font-medium text-zinc-400 hover:text-zinc-200 hover:bg-white/5 border border-transparent transition-all"
                >
                    <Settings className="w-4 h-4 stroke-[1.5] flex-shrink-0" />
                    <span>Settings</span>
                </button>
            </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 relative z-[2]">
        {/* Top Bar - Responsive */}
        <header className="flex-shrink-0 flex items-center justify-between px-2 sm:px-4 py-2 sm:py-3 bg-zinc-950/60 backdrop-blur-xl border-b border-white/5">
          <div className="flex items-center gap-2 sm:gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 sm:p-2 hover:bg-white/5 active:bg-white/5 rounded-lg sm:rounded-xl transition-colors touch-target"
            >
              {sidebarOpen ? (
                <ChevronLeft className="w-5 h-5 text-zinc-400" />
              ) : (
                <Menu className="w-5 h-5 text-zinc-400" />
              )}
            </button>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            {/* Model Badge - Condensed on mobile */}
            <div className="flex items-center gap-1.5 sm:gap-2 px-2 sm:px-3 py-1 sm:py-1.5 bg-white/5 rounded-full border border-white/10">
              <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full status-online bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]" />
              <span className="text-[10px] sm:text-xs text-zinc-300 hidden xs:inline">Gemini 3 Pro</span>
              <span className="text-[10px] sm:text-xs text-zinc-300 xs:hidden">AI</span>
            </div>

            {/* Knowledge Base Badge - Hidden on mobile */}
            <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-white/5 rounded-full border border-white/10">
              <Brain className="w-3.5 h-3.5 text-zinc-300" />
              <span className="text-xs text-zinc-300">GSW Connected</span>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-hidden">
          {children}
        </div>
      </main>
    </div>
  );
}
