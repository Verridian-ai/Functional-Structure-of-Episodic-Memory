'use client';

import React, { useState } from 'react';
import { HelpCircle, BookOpen, RotateCcw, Keyboard, X } from 'lucide-react';
import { useOnboarding } from './OnboardingProvider';

export function HelpButton() {
  const { resetOnboarding, openWelcomeModal, isOnboardingActive } = useOnboarding();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Don't show during onboarding
  if (isOnboardingActive) {
    return null;
  }

  return (
    <div className="fixed bottom-6 right-6 z-[100]">
      {/* Menu popup */}
      {isMenuOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-[99]"
            onClick={() => setIsMenuOpen(false)}
          />

          {/* Menu */}
          <div
            className="absolute bottom-16 right-0 w-64 mb-2 rounded-2xl overflow-hidden animate-scale-in"
            style={{
              background:
                'linear-gradient(135deg, rgba(9, 9, 11, 0.98), rgba(24, 24, 27, 0.95))',
              backdropFilter: 'blur(20px)',
              WebkitBackdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              boxShadow: `
                0 20px 40px rgba(0, 0, 0, 0.5),
                0 0 0 1px rgba(255, 255, 255, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.1)
              `,
            }}
          >
            {/* Header */}
            <div className="px-4 py-3 border-b border-white/5">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-white">Help & Tips</h3>
                <button
                  onClick={() => setIsMenuOpen(false)}
                  className="p-1 rounded-lg text-zinc-500 hover:text-zinc-300 hover:bg-white/5 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Menu items */}
            <div className="p-2">
              <button
                onClick={() => {
                  setIsMenuOpen(false);
                  resetOnboarding();
                }}
                className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left text-zinc-300 hover:text-white hover:bg-white/5 transition-all group"
              >
                <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center group-hover:bg-emerald-500/20 transition-colors">
                  <RotateCcw className="w-4 h-4 text-emerald-400" />
                </div>
                <div>
                  <div className="text-sm font-medium">Restart Tour</div>
                  <div className="text-xs text-zinc-500">
                    View the guided walkthrough again
                  </div>
                </div>
              </button>

              <button
                onClick={() => {
                  setIsMenuOpen(false);
                  openWelcomeModal();
                }}
                className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left text-zinc-300 hover:text-white hover:bg-white/5 transition-all group"
              >
                <div className="w-8 h-8 rounded-lg bg-cyan-500/10 flex items-center justify-center group-hover:bg-cyan-500/20 transition-colors">
                  <BookOpen className="w-4 h-4 text-cyan-400" />
                </div>
                <div>
                  <div className="text-sm font-medium">Welcome Screen</div>
                  <div className="text-xs text-zinc-500">
                    See the feature overview
                  </div>
                </div>
              </button>

              <div className="my-2 border-t border-white/5" />

              {/* Keyboard shortcuts */}
              <div className="px-3 py-2">
                <div className="flex items-center gap-2 text-xs text-zinc-500 mb-2">
                  <Keyboard className="w-3.5 h-3.5" />
                  <span className="font-medium">Keyboard Shortcuts</span>
                </div>
                <div className="space-y-1.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-zinc-400">Voice input</span>
                    <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-zinc-500 font-mono">
                      Space
                    </kbd>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-zinc-400">Send message</span>
                    <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-zinc-500 font-mono">
                      Enter
                    </kbd>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-zinc-400">New line</span>
                    <div className="flex items-center gap-0.5">
                      <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-zinc-500 font-mono">
                        Shift
                      </kbd>
                      <span className="text-zinc-600">+</span>
                      <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-zinc-500 font-mono">
                        Enter
                      </kbd>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Main button */}
      <button
        onClick={() => setIsMenuOpen(!isMenuOpen)}
        className={`
          group w-12 h-12 rounded-full flex items-center justify-center
          transition-all duration-300 ease-out
          ${
            isMenuOpen
              ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/30 scale-110'
              : 'bg-zinc-900/90 text-zinc-400 hover:text-white hover:bg-zinc-800 border border-white/10 hover:border-white/20'
          }
        `}
        style={{
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          boxShadow: isMenuOpen
            ? '0 8px 30px rgba(16, 185, 129, 0.4)'
            : '0 4px 20px rgba(0, 0, 0, 0.3)',
        }}
        title="Help & Tips"
      >
        <HelpCircle
          className={`w-5 h-5 transition-transform duration-300 ${
            isMenuOpen ? 'rotate-180' : 'group-hover:rotate-12'
          }`}
        />
      </button>
    </div>
  );
}
