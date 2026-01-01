'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { ArrowLeft, Sun, Moon, Home } from 'lucide-react';

interface FeaturePageLayoutProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  color: 'cyan' | 'purple' | 'emerald' | 'amber' | 'red';
  children: React.ReactNode;
}

const colorClasses = {
  cyan: {
    bg: 'bg-cyan-500/10',
    border: 'border-cyan-500/30',
    text: 'text-cyan-400',
    gradient: 'from-cyan-500/20',
  },
  purple: {
    bg: 'bg-purple-500/10',
    border: 'border-purple-500/30',
    text: 'text-purple-400',
    gradient: 'from-purple-500/20',
  },
  emerald: {
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-500/30',
    text: 'text-emerald-400',
    gradient: 'from-emerald-500/20',
  },
  amber: {
    bg: 'bg-amber-500/10',
    border: 'border-amber-500/30',
    text: 'text-amber-400',
    gradient: 'from-amber-500/20',
  },
  red: {
    bg: 'bg-red-500/10',
    border: 'border-red-500/30',
    text: 'text-red-400',
    gradient: 'from-red-500/20',
  },
};

export function FeaturePageLayout({
  title,
  description,
  icon,
  color,
  children,
}: FeaturePageLayoutProps) {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

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

  const colors = colorClasses[color];

  return (
    <div className="min-h-screen bg-zinc-950 text-white safe-area-inset">
      {/* Background */}
      <div className="fixed inset-0 bg-gradient-to-br from-zinc-950 via-zinc-900 to-zinc-950 pointer-events-none" />
      <div className="fixed inset-0 gradient-mesh pointer-events-none opacity-50" />

      {/* Header - Mobile First */}
      <header className="sticky top-0 z-50 flex items-center justify-between px-3 sm:px-4 md:px-6 lg:px-8 py-3 sm:py-4 border-b border-white/5 bg-zinc-950/80 backdrop-blur-xl safe-area-pt">
        <div className="flex items-center gap-2 sm:gap-3">
          <Link
            href="/dashboard"
            className="p-2 sm:p-2.5 hover:bg-white/5 active:bg-white/10 rounded-xl transition-colors touch-target"
            aria-label="Back to Dashboard"
          >
            <ArrowLeft className="w-5 h-5 text-zinc-400" />
          </Link>
          <div className="hidden sm:block">
            <Image
              src={theme === 'dark' ? '/Law_OS_Dark_Mode_Logo.png' : '/Law_OS_Light_Mode_Logo.png'}
              alt="LAW OS"
              width={80}
              height={32}
              className="object-contain h-6 sm:h-7 w-auto"
            />
          </div>
        </div>

        {/* Mobile Title */}
        <h1 className="sm:hidden text-sm font-semibold text-white truncate max-w-[140px]">
          {title}
        </h1>

        <div className="flex items-center gap-1.5 sm:gap-2">
          <Link
            href="/dashboard"
            className="p-2 sm:p-2.5 hover:bg-white/5 active:bg-white/10 rounded-xl transition-colors touch-target"
            aria-label="Dashboard"
          >
            <Home className="w-5 h-5 text-zinc-400" />
          </Link>
          <button
            onClick={toggleTheme}
            className="p-2 sm:p-2.5 hover:bg-white/5 active:bg-white/10 rounded-xl transition-colors touch-target"
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {theme === 'dark' ? (
              <Moon className="w-5 h-5 text-amber-400" />
            ) : (
              <Sun className="w-5 h-5 text-amber-500" />
            )}
          </button>
        </div>
      </header>

      {/* Hero Section - Mobile Optimized */}
      <div className={`relative bg-gradient-to-r ${colors.gradient} to-transparent border-b border-white/5`}>
        <div className="px-3 sm:px-4 md:px-6 lg:px-8 py-4 sm:py-6 md:py-8 max-w-7xl mx-auto">
          <div className="flex items-start sm:items-center gap-3 sm:gap-4">
            <div className={`w-10 h-10 sm:w-12 sm:h-12 md:w-14 md:h-14 rounded-xl sm:rounded-2xl ${colors.bg} border ${colors.border} flex items-center justify-center flex-shrink-0`}>
              <span className={colors.text}>{icon}</span>
            </div>
            <div className="min-w-0 flex-1">
              <h1 className="text-lg sm:text-xl md:text-2xl lg:text-3xl font-bold text-white truncate sm:whitespace-normal">
                {title}
              </h1>
              <p className="text-xs sm:text-sm md:text-base text-zinc-400 mt-0.5 sm:mt-1 line-clamp-2 sm:line-clamp-none">
                {description}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="relative z-10 px-3 sm:px-4 md:px-6 lg:px-8 py-4 sm:py-6 md:py-8 max-w-7xl mx-auto">
        {children}
      </main>

      {/* Footer - Mobile First */}
      <footer className="relative z-10 px-3 sm:px-4 md:px-6 lg:px-8 py-4 sm:py-6 border-t border-white/5 mt-6 sm:mt-8 safe-area-pb">
        <div className="max-w-7xl mx-auto text-center sm:text-left">
          <p className="text-[10px] sm:text-xs text-zinc-500">
            LAW OS by Verridian AI - Brain-inspired Legal Intelligence
          </p>
        </div>
      </footer>
    </div>
  );
}

export default FeaturePageLayout;
