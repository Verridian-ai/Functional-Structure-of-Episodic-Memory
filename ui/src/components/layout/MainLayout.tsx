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
    <div className="flex h-screen bg-zinc-950 text-white overflow-hidden relative">
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
            ${sidebarOpen ? 'translate-x-0 w-72' : '-translate-x-full md:translate-x-0 md:w-0'}
            flex flex-col bg-blue-950/40 backdrop-blur-2xl border-r border-cyan-500/20 transition-all duration-300 overflow-hidden
        `}
      >
        {/* Sidebar Header */}
        <div className="flex-shrink-0 p-4 border-b border-cyan-500/20">
          <div className="flex items-center gap-3 mb-4">
            <div className="relative w-10 h-10">
              <Image 
                src="/verridian_logo.png"
                alt="Verridian"
                fill
                className="object-contain"
              />
            </div>
            <div className="flex-1 min-w-0">
              <h1 className="font-bold text-white text-lg tracking-tight">LAW OS</h1>
            </div>
          </div>

          {/* New Chat Button */}
          <button
            onClick={() => {
                onNewChat();
                if (window.innerWidth < 768) setSidebarOpen(false);
            }}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white rounded-xl font-medium shadow-lg shadow-cyan-500/20 transition-all transform hover:scale-[1.02] active:scale-[0.98]"
          >
            <Plus className="w-5 h-5" />
            New Conversation
          </button>
        </div>

        {/* Search */}
        <div className="flex-shrink-0 p-3">
          <div className="relative group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cyan-300/50 group-focus-within:text-cyan-400 transition-colors" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search conversations..."
              className="w-full pl-10 pr-4 py-2.5 bg-blue-950/40 border border-cyan-500/20 rounded-xl text-sm text-white placeholder:text-cyan-300/30 focus:outline-none focus:border-cyan-500/50 focus:bg-blue-900/40 focus:shadow-[0_0_15px_rgba(6,182,212,0.1)] transition-all"
            />
          </div>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto px-3 pb-3">
          {filteredConversations.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-12 h-12 mx-auto mb-3 rounded-xl bg-blue-900/20 flex items-center justify-center">
                <MessageSquare className="w-6 h-6 text-cyan-400" />
              </div>
              <p className="text-sm text-cyan-300/70">
                {searchQuery ? 'No matching conversations' : 'No conversations yet'}
              </p>
              <p className="text-xs text-cyan-300/50 mt-1">Start a new chat to begin</p>
            </div>
          ) : (
            <div className="space-y-1">
              {filteredConversations.map((conv, index) => (
                <div
                  key={conv.id}
                  className={`group flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all duration-200 animate-fade-in hover:translate-x-1 ${
                    conv.id === currentConversationId
                      ? 'bg-cyan-600/20 border border-cyan-500/30 shadow-lg shadow-cyan-500/10'
                      : 'hover:bg-blue-900/20 border border-transparent'
                  }`}
                  style={{ animationDelay: `${index * 50}ms` }}
                  onClick={() => {
                      setCurrentConversation(conv.id);
                      if (window.innerWidth < 768) setSidebarOpen(false);
                  }}
                >
                  <div className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 ${
                    conv.id === currentConversationId
                      ? 'bg-cyan-500/20'
                      : 'bg-blue-900/30'
                  }`}>
                    <MessageSquare className={`w-4 h-4 ${
                      conv.id === currentConversationId ? 'text-cyan-400' : 'text-cyan-300/50'
                    }`} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className={`text-sm font-medium truncate ${
                      conv.id === currentConversationId ? 'text-white' : 'text-zinc-300'
                    }`}>
                      {conv.title}
                    </div>
                    <div className="text-xs text-cyan-300/50 truncate">
                      {conv.messages.length} messages
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteConversation(conv.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-500/20 rounded-lg transition-all"
                  >
                    <Trash2 className="w-4 h-4 text-red-400" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Sidebar Footer */}
        <div className="flex-shrink-0 p-3 border-t border-cyan-500/20 space-y-1">
          <button
            onClick={() => {
                toggleCanvas();
                if (window.innerWidth < 768) setSidebarOpen(false);
            }}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all hover:bg-blue-900/20 active:scale-95 ${
              showCanvas
                ? 'bg-cyan-600/20 text-cyan-300 border border-cyan-500/30'
                : 'hover:bg-blue-900/20 text-zinc-400 border border-transparent'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span className="flex-1 text-left">Canvas</span>
            {showCanvas && <div className="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_10px_rgba(6,182,212,0.5)]" />}
          </button>
          <button
            onClick={toggleAdmin}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-zinc-400 hover:bg-blue-900/20 active:scale-95 transition-all border border-transparent"
          >
            <Settings className="w-4 h-4" />
            <span className="flex-1 text-left">Settings</span>
          </button>
        </div>

        {/* Stats - Badges Removed */}
        <div className="flex-shrink-0 p-3 border-t border-cyan-500/20">
           {/* Empty container to maintain layout structure if needed, or can be removed entirely */}
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
