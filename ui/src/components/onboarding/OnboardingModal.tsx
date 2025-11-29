'use client';

import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  Brain,
  Sparkles,
  MessageSquare,
  FileText,
  Mic,
  Scale,
  ArrowRight,
  X,
  BookOpen,
  Zap,
} from 'lucide-react';
import Image from 'next/image';
import { useOnboarding } from './OnboardingProvider';

export function OnboardingModal() {
  const { showWelcomeModal, closeWelcomeModal, startOnboarding, skipOnboarding } =
    useOnboarding();
  const [mounted, setMounted] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (showWelcomeModal) {
      // Slight delay for animation
      const timer = setTimeout(() => setIsVisible(true), 50);
      return () => clearTimeout(timer);
    } else {
      setIsVisible(false);
    }
  }, [showWelcomeModal]);

  if (!mounted || !showWelcomeModal) {
    return null;
  }

  const features = [
    {
      icon: Brain,
      title: 'Neural Legal AI',
      description: 'Advanced AI that understands legal context and precedents',
      color: 'emerald',
    },
    {
      icon: MessageSquare,
      title: 'Natural Conversation',
      description: 'Ask questions in plain English, get expert-level answers',
      color: 'cyan',
    },
    {
      icon: FileText,
      title: 'Document Generation',
      description: 'Draft letters, briefs, and contracts with AI assistance',
      color: 'amber',
    },
    {
      icon: Mic,
      title: 'Voice Input',
      description: 'Hands-free operation with voice commands',
      color: 'violet',
    },
  ];

  const handleStartTour = () => {
    setIsVisible(false);
    setTimeout(() => {
      startOnboarding();
    }, 200);
  };

  const handleSkip = () => {
    setIsVisible(false);
    setTimeout(() => {
      skipOnboarding();
    }, 200);
  };

  const modalContent = (
    <div
      className={`
        fixed inset-0 z-[10001] flex items-center justify-center p-4
        transition-all duration-300 ease-out
        ${isVisible ? 'opacity-100' : 'opacity-0 pointer-events-none'}
      `}
    >
      {/* Backdrop */}
      <div
        className={`
          absolute inset-0 bg-black/80 backdrop-blur-md
          transition-opacity duration-300
          ${isVisible ? 'opacity-100' : 'opacity-0'}
        `}
        onClick={handleSkip}
      />

      {/* Modal */}
      <div
        className={`
          relative w-full max-w-2xl max-h-[90vh] overflow-y-auto
          rounded-3xl shadow-2xl
          transition-all duration-500 ease-out
          ${isVisible ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-95 translate-y-4'}
        `}
        style={{
          background:
            'linear-gradient(145deg, rgba(16, 185, 129, 0.08) 0%, rgba(9, 9, 11, 0.98) 20%, rgba(9, 9, 11, 1) 100%)',
          backdropFilter: 'blur(40px)',
          WebkitBackdropFilter: 'blur(40px)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          boxShadow: `
            0 40px 80px -20px rgba(0, 0, 0, 0.8),
            0 0 0 1px rgba(255, 255, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 100px rgba(16, 185, 129, 0.1)
          `,
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Decorative gradient */}
        <div
          className="absolute top-0 left-0 right-0 h-48 pointer-events-none"
          style={{
            background:
              'radial-gradient(ellipse 80% 50% at 50% 0%, rgba(16, 185, 129, 0.15), transparent 60%)',
          }}
        />

        {/* Close button */}
        <button
          onClick={handleSkip}
          className="absolute top-4 right-4 p-2 rounded-xl text-zinc-500 hover:text-zinc-300 hover:bg-white/5 transition-all z-10"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Content */}
        <div className="relative p-8 md:p-10">
          {/* Header */}
          <div className="text-center mb-8">
            {/* Logo */}
            <div className="relative w-20 h-20 mx-auto mb-6">
              <div
                className="absolute inset-0 rounded-2xl"
                style={{
                  background:
                    'linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.05))',
                  border: '1px solid rgba(16, 185, 129, 0.3)',
                  boxShadow: '0 0 30px rgba(16, 185, 129, 0.2)',
                }}
              />
              <div className="relative w-full h-full flex items-center justify-center">
                <Scale className="w-10 h-10 text-emerald-400" />
              </div>
            </div>

            <h1 className="text-3xl md:text-4xl font-bold text-white mb-3">
              Welcome to{' '}
              <span
                className="bg-gradient-to-r from-emerald-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent"
                style={{
                  backgroundSize: '200% 100%',
                  animation: 'gradient-shift 3s ease infinite',
                }}
              >
                LAW OS
              </span>
            </h1>

            <p className="text-lg text-zinc-400 max-w-md mx-auto">
              Your AI-powered legal assistant with advanced neural processing and
              document generation capabilities
            </p>
          </div>

          {/* Features grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className={`
                  group p-5 rounded-2xl transition-all duration-300
                  hover:scale-[1.02]
                `}
                style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid rgba(255, 255, 255, 0.05)',
                  animationDelay: `${index * 100}ms`,
                }}
              >
                <div className="flex items-start gap-4">
                  <div
                    className={`
                      w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0
                      transition-all duration-300 group-hover:scale-110
                    `}
                    style={{
                      background:
                        feature.color === 'emerald'
                          ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.05))'
                          : feature.color === 'cyan'
                          ? 'linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(6, 182, 212, 0.05))'
                          : feature.color === 'amber'
                          ? 'linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.05))'
                          : 'linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(139, 92, 246, 0.05))',
                      border:
                        feature.color === 'emerald'
                          ? '1px solid rgba(16, 185, 129, 0.3)'
                          : feature.color === 'cyan'
                          ? '1px solid rgba(6, 182, 212, 0.3)'
                          : feature.color === 'amber'
                          ? '1px solid rgba(245, 158, 11, 0.3)'
                          : '1px solid rgba(139, 92, 246, 0.3)',
                    }}
                  >
                    <feature.icon
                      className={`w-6 h-6 ${
                        feature.color === 'emerald'
                          ? 'text-emerald-400'
                          : feature.color === 'cyan'
                          ? 'text-cyan-400'
                          : feature.color === 'amber'
                          ? 'text-amber-400'
                          : 'text-violet-400'
                      }`}
                    />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">
                      {feature.title}
                    </h3>
                    <p className="text-sm text-zinc-500">{feature.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Action buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={handleStartTour}
              className="group flex items-center gap-3 px-8 py-4 rounded-2xl text-black font-semibold transition-all hover:scale-[1.02] active:scale-[0.98]"
              style={{
                background: 'linear-gradient(135deg, #10b981, #059669)',
                boxShadow: `
                  0 8px 30px rgba(16, 185, 129, 0.4),
                  inset 0 1px 0 rgba(255, 255, 255, 0.2)
                `,
              }}
            >
              <Sparkles className="w-5 h-5" />
              Take the Tour
              <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
            </button>

            <button
              onClick={handleSkip}
              className="flex items-center gap-2 px-6 py-4 rounded-2xl text-zinc-400 hover:text-white transition-colors hover:bg-white/5"
            >
              <Zap className="w-4 h-4" />
              Skip, I know what I'm doing
            </button>
          </div>

          {/* Keyboard hint */}
          <p className="text-center text-xs text-zinc-600 mt-6">
            Press <kbd className="px-2 py-1 bg-zinc-800 rounded text-zinc-400">Enter</kbd> to start
            or <kbd className="px-2 py-1 bg-zinc-800 rounded text-zinc-400">Esc</kbd> to skip
          </p>
        </div>
      </div>
    </div>
  );

  return createPortal(modalContent, document.body);
}

// Add gradient animation to globals.css
const gradientKeyframes = `
@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
`;
