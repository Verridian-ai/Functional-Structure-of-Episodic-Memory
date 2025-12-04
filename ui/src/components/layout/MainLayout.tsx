'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import {
  MessageSquare, FileText, Settings, Menu, Plus,
  ChevronLeft, Trash2, Brain, Sun, Moon, Home
} from 'lucide-react';
import { useStore } from '@/lib/store';

interface MainLayoutProps {
  children: React.ReactNode;
  onNewChat: () => void;
}

export function MainLayout({ children, onNewChat }: MainLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  // Theme toggle effect
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'dark' | 'light' | null;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.setAttribute('data-theme', savedTheme);
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };
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
        const width = window.innerWidth;
        // Close sidebar on mobile (< 768px), open on tablet+ (>= 768px)
        if (width < 768) {
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
      className="flex min-h-[100dvh] md:h-screen bg-zinc-950 text-white overflow-hidden relative"
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      {/* Subtle gradient background for LAW OS */}
      <div className="fixed inset-0 bg-gradient-to-br from-zinc-950 via-zinc-900 to-zinc-950 pointer-events-none z-[0]" />
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
            ${sidebarOpen ? 'translate-x-0 w-[280px] sm:w-[300px] md:w-[320px] lg:w-80' : '-translate-x-full md:translate-x-0 md:w-0'}
            flex flex-col bg-zinc-950/95 backdrop-blur-3xl border-r border-white/5 transition-all duration-300 ease-in-out overflow-hidden shadow-2xl
        `}
      >
        {/* Sidebar Header Section - Logo */}
        <div className="flex-shrink-0 pt-4 sm:pt-5 md:pt-6 pb-4" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
          {/* Logo - Switch based on theme */}
          <div className="flex items-center gap-2.5 sm:gap-3">
            <div className="relative w-32 h-12 sm:w-36 sm:h-14 md:w-40 md:h-16 flex items-center justify-center flex-shrink-0">
              <Image
                src={theme === 'dark' ? '/Law_OS_Dark_Mode_Logo.png' : '/Law_OS_Light_Mode_Logo.png'}
                alt="LAW OS logo"
                width={160}
                height={64}
                className="object-contain drop-shadow-lg"
                priority
              />
            </div>
          </div>
        </div>

        {/* New Chat Button */}
        <div className="flex-shrink-0 mb-6" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
          <button
            id="new-project-button"
            onClick={() => {
                onNewChat();
                if (window.innerWidth < 768) setSidebarOpen(false);
            }}
            className="group w-full flex items-center justify-center gap-2.5 px-4 h-11 sm:h-12 bg-white/[0.08] hover:bg-white/[0.12] border border-white/10 hover:border-white/20 text-white rounded-xl sm:rounded-2xl font-semibold transition-all duration-200 active:scale-[0.98] touch-target shadow-sm"
          >
            <Plus className="w-5 h-5 text-white stroke-[2]" />
            <span className="tracking-wide text-sm sm:text-base">New Chat</span>
          </button>
        </div>

        {/* Search Section */}
        <div className="flex-shrink-0 mb-6" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search projects..."
            className="h-10 w-full px-3 bg-black/40 border border-zinc-800 rounded-xl text-sm text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:bg-black/60 focus:border-zinc-700 focus:ring-1 focus:ring-emerald-500/40 transition-all"
          />
        </div>

        {/* Recent Activity Label */}
        <div className="mb-3 flex items-center justify-between border-b border-white/5 pb-3" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
            <span className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider">Recents</span>
            <span className="text-[10px] text-zinc-500 font-mono bg-white/5 px-1.5 py-0.5 rounded">{filteredConversations.length}</span>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto py-2 space-y-1 custom-scrollbar" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
          {filteredConversations.length === 0 ? (
            <div className="empty-state-container flex flex-col items-center justify-center py-12 sm:py-16 px-4 text-center rounded-2xl mt-4">
              <div className="w-16 h-16 sm:w-20 sm:h-20 mx-auto mb-4 sm:mb-5 rounded-xl sm:rounded-2xl bg-zinc-800/50 border border-dashed border-zinc-600/50 flex items-center justify-center">
                <MessageSquare className="w-8 h-8 sm:w-10 sm:h-10 text-zinc-500" />
              </div>
              <p className="text-sm sm:text-base text-zinc-400 font-medium mb-1">
                {searchQuery ? 'No matches found' : 'No conversations yet'}
              </p>
              {!searchQuery && (
                <p className="text-xs sm:text-sm text-zinc-500">
                  Start a new chat to begin
                </p>
              )}
            </div>
          ) : (
            <div className="space-y-1 sm:space-y-1.5">
              {filteredConversations.map((conv, index) => (
                <div
                  key={conv.id}
                  className={`group relative flex items-center gap-2.5 sm:gap-3.5 p-3 sm:p-3.5 rounded-xl sm:rounded-2xl cursor-pointer transition-all duration-200 border touch-target ${
                    conv.id === currentConversationId
                      ? 'bg-white/10 border-white/10 shadow-md shadow-emerald-500/10'
                      : 'bg-white/[0.02] border-white/5 hover:bg-white/8 hover:border-white/10 active:bg-white/10'
                  }`}
                  onClick={() => {
                      setCurrentConversation(conv.id);
                      if (window.innerWidth < 768) setSidebarOpen(false);
                  }}
                >
                  <div className={`w-9 h-9 sm:w-10 sm:h-10 rounded-lg sm:rounded-xl flex items-center justify-center flex-shrink-0 transition-colors ${
                    conv.id === currentConversationId
                      ? 'bg-emerald-500/20 text-white border border-emerald-500/30'
                      : 'bg-zinc-900/70 text-zinc-500 group-hover:text-zinc-300 group-hover:bg-zinc-800/80 border border-transparent group-hover:border-zinc-700/60'
                  }`}>
                    <MessageSquare className="w-4 h-4 sm:w-5 sm:h-5" />
                  </div>

                  <div className="flex-1 min-w-0 py-0.5">
                    <div className={`text-xs sm:text-sm font-semibold truncate mb-0.5 ${
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

        {/* Sidebar Footer */}
        <div className="flex-shrink-0 py-3 border-t border-white/10 safe-area-pb" style={{ paddingLeft: '16px', paddingRight: '16px' }}>
            {/* Dashboard Button */}
            <button
                className="w-full flex items-center gap-3 px-3 py-2.5 mb-3 rounded-lg text-sm font-medium text-zinc-300 hover:text-white hover:bg-white/[0.05] transition-all"
            >
                <Home className="w-4 h-4" />
                <span>Dashboard</span>
            </button>

            {/* Theme Toggle */}
            <div className="flex items-center justify-between">
                <span className="text-sm text-zinc-400">Theme</span>
                <button
                    onClick={toggleTheme}
                    className="w-9 h-9 flex items-center justify-center rounded-full bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/30 transition-all"
                    aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
                >
                    {theme === 'dark' ? (
                        <Moon className="w-4 h-4 text-amber-400" />
                    ) : (
                        <Sun className="w-4 h-4 text-amber-500" />
                    )}
                </button>
            </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 relative z-[2]">
        {/* Top Bar - Responsive */}
        <header className="flex-shrink-0 flex items-center justify-between px-3 sm:px-4 md:px-6 py-2.5 sm:py-3 md:py-4 bg-zinc-950/60 backdrop-blur-xl border-b border-white/5 safe-area-pt">
          <div className="flex items-center gap-2 sm:gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 sm:p-2.5 hover:bg-white/5 active:bg-white/10 rounded-lg sm:rounded-xl transition-colors touch-target"
              aria-label={sidebarOpen ? 'Close sidebar' : 'Open sidebar'}
            >
              {sidebarOpen ? (
                <ChevronLeft className="w-5 h-5 sm:w-6 sm:h-6 text-zinc-400" />
              ) : (
                <Menu className="w-5 h-5 sm:w-6 sm:h-6 text-zinc-400" />
              )}
            </button>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            {/* Model Badge - Condensed on mobile */}
            <div className="flex items-center gap-1.5 sm:gap-2 px-2.5 sm:px-3 py-1.5 sm:py-2 bg-white/5 rounded-full border border-white/10">
              <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full status-online bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]" />
              <span className="text-[10px] sm:text-xs text-zinc-300 hidden min-[375px]:inline">Gemini 3 Pro</span>
              <span className="text-[10px] sm:text-xs text-zinc-300 min-[375px]:hidden">AI</span>
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
