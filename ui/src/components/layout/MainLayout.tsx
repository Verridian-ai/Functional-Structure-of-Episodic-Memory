'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import {
  MessageSquare, FileText, Settings, Menu, Plus,
  ChevronLeft, Trash2, Search, Brain, Database
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
            ${sidebarOpen ? 'translate-x-0 w-80' : '-translate-x-full md:translate-x-0 md:w-0'}
            flex flex-col bg-blue-950/60 backdrop-blur-3xl border-r border-cyan-500/10 transition-all duration-300 overflow-hidden shadow-2xl
        `}
      >
        {/* Sidebar Header Section */}
        <div className="flex-shrink-0 px-6 pt-8 pb-6 border-b border-white/5">
          <div className="flex items-center gap-4 mb-8">
            <div className="relative w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500/20 to-blue-600/20 border border-white/10 flex items-center justify-center shadow-lg">
              <Image 
                src="/verridian_logo.png"
                alt="Verridian"
                width={28}
                height={28}
                className="object-contain drop-shadow-md"
              />
            </div>
            <div className="flex-1 min-w-0">
              <h1 className="font-semibold text-white text-xl tracking-tight leading-none">LAW OS</h1>
              <p className="text-xs text-zinc-400 font-medium tracking-wider mt-1.5">VERRIDIAN AI</p>
            </div>
          </div>

          {/* New Chat Button - Standard 52px Height */}
          <button
            onClick={() => {
                onNewChat();
                if (window.innerWidth < 768) setSidebarOpen(false);
            }}
            className="group w-full flex items-center gap-4 px-4 h-[52px] bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl font-medium shadow-lg shadow-cyan-900/20 transition-all active:scale-[0.98]"
          >
            <div className="w-8 h-8 flex items-center justify-center bg-white/10 rounded-lg group-hover:bg-white/20 transition-colors">
                <Plus className="w-5 h-5 text-white stroke-[2.5]" />
            </div>
            <span className="tracking-wide text-[15px]">New Project</span>
          </button>
        </div>

        {/* Search Section - Spacious & Distinct */}
        <div className="flex-shrink-0 px-6 py-6 border-b border-white/5 bg-white/[0.02]">
          <div className="relative group flex items-center">
            <Search className="absolute left-4 w-5 h-5 text-zinc-500 group-focus-within:text-cyan-400 transition-colors stroke-[2] pointer-events-none" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search"
              className="w-full h-12 pl-14 pr-4 bg-black/40 border border-zinc-800 rounded-xl text-[15px] text-zinc-200 placeholder:text-zinc-500 focus:outline-none focus:bg-black/60 focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all"
            />
          </div>
        </div>

        {/* Recent Activity Label - Increased Spacing */}
        <div className="px-6 pt-6 pb-4 flex items-center justify-between border-b border-white/5 bg-white/[0.02] mt-2">
            <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Recents</span>
            <span className="text-[10px] text-zinc-500 font-mono bg-white/5 px-2 py-0.5 rounded-md">{filteredConversations.length}</span>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto px-4 pb-4 space-y-2 custom-scrollbar">
          {filteredConversations.length === 0 ? (
            <div className="text-center py-16 px-4">
              <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-zinc-900/50 border border-dashed border-zinc-800 flex items-center justify-center">
                <MessageSquare className="w-6 h-6 text-zinc-600" />
              </div>
              <p className="text-sm text-zinc-500 font-medium">
                {searchQuery ? 'No matches found' : 'No history yet'}
              </p>
            </div>
          ) : (
            <div className="space-y-1.5">
              {filteredConversations.map((conv, index) => (
                <div
                  key={conv.id}
                  className={`group relative flex items-center gap-3.5 p-3.5 rounded-2xl cursor-pointer transition-all duration-200 border ${
                    conv.id === currentConversationId
                      ? 'bg-blue-900/20 border-cyan-500/30 shadow-md shadow-cyan-900/10'
                      : 'hover:bg-white/5 border-transparent hover:border-white/5'
                  }`}
                  onClick={() => {
                      setCurrentConversation(conv.id);
                      if (window.innerWidth < 768) setSidebarOpen(false);
                  }}
                >
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 transition-colors ${
                    conv.id === currentConversationId
                      ? 'bg-gradient-to-br from-cyan-500/20 to-blue-600/20 text-cyan-400'
                      : 'bg-zinc-900 text-zinc-500 group-hover:text-zinc-300 group-hover:bg-zinc-800'
                  }`}>
                    <MessageSquare className="w-4.5 h-4.5" />
                  </div>
                  
                  <div className="flex-1 min-w-0 py-0.5">
                    <div className={`text-sm font-medium truncate mb-0.5 ${
                      conv.id === currentConversationId ? 'text-cyan-100' : 'text-zinc-400 group-hover:text-zinc-200'
                    }`}>
                      {conv.title}
                    </div>
                    <div className="flex items-center gap-2 text-xs text-zinc-600 group-hover:text-zinc-500">
                        <span>{new Date().toLocaleDateString()}</span>
                        <span className="w-0.5 h-0.5 rounded-full bg-zinc-600" />
                        <span>{conv.messages.length} msgs</span>
                    </div>
                  </div>

                  {/* Hover Actions */}
                  <div className="absolute right-2 opacity-0 group-hover:opacity-100 transition-opacity flex items-center bg-zinc-950/80 rounded-lg shadow-sm backdrop-blur-sm">
                    <button
                        onClick={(e) => {
                        e.stopPropagation();
                        deleteConversation(conv.id);
                        }}
                        className="p-2 text-zinc-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
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

        {/* Sidebar Footer - Separated */}
        <div className="flex-shrink-0 p-6 border-t border-white/10 bg-[#0B101B]">
            <div className="space-y-2">
                <button
                    onClick={() => {
                        toggleCanvas();
                        if (window.innerWidth < 768) setSidebarOpen(false);
                    }}
                    className={`group w-full flex items-center gap-4 px-4 h-14 rounded-2xl text-[15px] font-medium transition-all ${
                    showCanvas
                        ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'
                        : 'hover:bg-white/5 text-zinc-400 hover:text-zinc-200 border border-transparent'
                    }`}
                >
                    <FileText className="w-6 h-6 stroke-[1.5]" />
                    <span className="flex-1 text-left">Canvas</span>
                    <div className={`w-2 h-2 rounded-full transition-colors ${showCanvas ? 'bg-cyan-400 shadow-[0_0_8px_rgba(6,182,212,0.8)]' : 'bg-zinc-800 group-hover:bg-zinc-700'}`} />
                </button>
                
                <button
                    onClick={toggleAdmin}
                    className="w-full flex items-center gap-4 px-4 h-14 rounded-2xl text-[15px] font-medium text-zinc-400 hover:text-zinc-200 hover:bg-white/5 border border-transparent transition-all"
                >
                    <Settings className="w-6 h-6 stroke-[1.5]" />
                    <span className="flex-1 text-left">Settings</span>
                </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 relative z-[2]">
        {/* Top Bar */}
        <header className="flex-shrink-0 flex items-center justify-between px-4 py-3 bg-blue-950/40 backdrop-blur-xl border-b border-cyan-500/20">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-blue-900/30 rounded-xl transition-colors"
            >
              {sidebarOpen ? (
                <ChevronLeft className="w-5 h-5 text-cyan-300/70" />
              ) : (
                <Menu className="w-5 h-5 text-cyan-300/70" />
              )}
            </button>
          </div>

          <div className="flex items-center gap-3">
            {/* Model Badge */}
            <div className="flex items-center gap-2 px-3 py-1.5 bg-blue-900/20 rounded-full border border-cyan-500/20">
              <div className="w-2 h-2 rounded-full status-online bg-cyan-400 shadow-[0_0_8px_rgba(6,182,212,0.8)]" />
              <span className="text-xs text-cyan-200">Gemini 3 Pro</span>
            </div>

            {/* Knowledge Base Badge */}
            <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-cyan-600/20 rounded-full border border-cyan-500/30">
              <Brain className="w-3.5 h-3.5 text-cyan-300" />
              <span className="text-xs text-cyan-200">GSW Connected</span>
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
