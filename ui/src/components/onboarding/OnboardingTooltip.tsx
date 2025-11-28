'use client';

import React, { useEffect, useState, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { ChevronLeft, ChevronRight, X, Sparkles } from 'lucide-react';
import { useOnboarding, OnboardingStep } from './OnboardingProvider';

interface TooltipPosition {
  top: number;
  left: number;
  arrowPosition: 'top' | 'bottom' | 'left' | 'right' | 'none';
}

interface SpotlightRect {
  top: number;
  left: number;
  width: number;
  height: number;
  borderRadius: number;
}

export function OnboardingTooltip() {
  const {
    isOnboardingActive,
    currentStep,
    currentStepIndex,
    steps,
    nextStep,
    prevStep,
    skipOnboarding,
    completeOnboarding,
  } = useOnboarding();

  const [tooltipPosition, setTooltipPosition] = useState<TooltipPosition>({
    top: 0,
    left: 0,
    arrowPosition: 'none',
  });
  const [spotlightRect, setSpotlightRect] = useState<SpotlightRect | null>(
    null
  );
  const [isAnimating, setIsAnimating] = useState(false);
  const [mounted, setMounted] = useState(false);
  const tooltipRef = useRef<HTMLDivElement>(null);

  // Portal mount
  useEffect(() => {
    setMounted(true);
    return () => setMounted(false);
  }, []);

  // Calculate position based on target element
  const calculatePosition = useCallback(
    (step: OnboardingStep) => {
      const targetElement = document.getElementById(step.targetId);
      const tooltipElement = tooltipRef.current;

      if (!targetElement) {
        // If no target element, center the tooltip
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const tooltipWidth = tooltipElement?.offsetWidth || 400;
        const tooltipHeight = tooltipElement?.offsetHeight || 200;

        setTooltipPosition({
          top: (windowHeight - tooltipHeight) / 2,
          left: (windowWidth - tooltipWidth) / 2,
          arrowPosition: 'none',
        });
        setSpotlightRect(null);
        return;
      }

      const targetRect = targetElement.getBoundingClientRect();
      const padding = step.spotlightPadding || 8;
      const tooltipWidth = tooltipElement?.offsetWidth || 400;
      const tooltipHeight = tooltipElement?.offsetHeight || 200;
      const margin = 16; // Space between tooltip and target
      const windowWidth = window.innerWidth;
      const windowHeight = window.innerHeight;

      // Set spotlight rectangle
      setSpotlightRect({
        top: targetRect.top - padding,
        left: targetRect.left - padding,
        width: targetRect.width + padding * 2,
        height: targetRect.height + padding * 2,
        borderRadius: 12,
      });

      let top = 0;
      let left = 0;
      let arrowPosition: TooltipPosition['arrowPosition'] = 'none';

      switch (step.position) {
        case 'top':
          top = targetRect.top - tooltipHeight - margin - padding;
          left = targetRect.left + targetRect.width / 2 - tooltipWidth / 2;
          arrowPosition = 'bottom';
          break;
        case 'bottom':
          top = targetRect.bottom + margin + padding;
          left = targetRect.left + targetRect.width / 2 - tooltipWidth / 2;
          arrowPosition = 'top';
          break;
        case 'left':
          top = targetRect.top + targetRect.height / 2 - tooltipHeight / 2;
          left = targetRect.left - tooltipWidth - margin - padding;
          arrowPosition = 'right';
          break;
        case 'right':
          top = targetRect.top + targetRect.height / 2 - tooltipHeight / 2;
          left = targetRect.right + margin + padding;
          arrowPosition = 'left';
          break;
        case 'center':
        default:
          top = (windowHeight - tooltipHeight) / 2;
          left = (windowWidth - tooltipWidth) / 2;
          arrowPosition = 'none';
          break;
      }

      // Clamp to viewport
      const clampedLeft = Math.max(
        margin,
        Math.min(left, windowWidth - tooltipWidth - margin)
      );
      const clampedTop = Math.max(
        margin,
        Math.min(top, windowHeight - tooltipHeight - margin)
      );

      // Adjust if tooltip was clamped significantly
      if (Math.abs(clampedLeft - left) > 50) {
        arrowPosition = 'none';
      }
      if (Math.abs(clampedTop - top) > 50) {
        arrowPosition = 'none';
      }

      setTooltipPosition({
        top: clampedTop,
        left: clampedLeft,
        arrowPosition,
      });
    },
    []
  );

  // Recalculate on step change
  useEffect(() => {
    if (isOnboardingActive && currentStep) {
      setIsAnimating(true);
      const timer = setTimeout(() => {
        calculatePosition(currentStep);
        setIsAnimating(false);
      }, 50);

      return () => clearTimeout(timer);
    }
  }, [isOnboardingActive, currentStep, calculatePosition]);

  // Recalculate on resize
  useEffect(() => {
    if (!isOnboardingActive || !currentStep) return;

    const handleResize = () => {
      calculatePosition(currentStep);
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('scroll', handleResize, true);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('scroll', handleResize, true);
    };
  }, [isOnboardingActive, currentStep, calculatePosition]);

  // Keyboard navigation
  useEffect(() => {
    if (!isOnboardingActive) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        skipOnboarding();
      } else if (e.key === 'ArrowRight' || e.key === 'Enter') {
        if (currentStepIndex < steps.length - 1) {
          nextStep();
        } else {
          completeOnboarding();
        }
      } else if (e.key === 'ArrowLeft') {
        prevStep();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [
    isOnboardingActive,
    currentStepIndex,
    steps.length,
    nextStep,
    prevStep,
    skipOnboarding,
    completeOnboarding,
  ]);

  if (!mounted || !isOnboardingActive || !currentStep) {
    return null;
  }

  const isLastStep = currentStepIndex === steps.length - 1;
  const isFirstStep = currentStepIndex === 0;

  const tooltipContent = (
    <>
      {/* Overlay with spotlight cutout */}
      <div className="fixed inset-0 z-[9998] pointer-events-none">
        {/* Dark overlay */}
        <svg className="w-full h-full">
          <defs>
            <mask id="spotlight-mask">
              <rect x="0" y="0" width="100%" height="100%" fill="white" />
              {spotlightRect && (
                <rect
                  x={spotlightRect.left}
                  y={spotlightRect.top}
                  width={spotlightRect.width}
                  height={spotlightRect.height}
                  rx={spotlightRect.borderRadius}
                  fill="black"
                />
              )}
            </mask>
          </defs>
          <rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="rgba(0, 0, 0, 0.75)"
            mask="url(#spotlight-mask)"
            className="transition-all duration-300 ease-out"
          />
        </svg>

        {/* Spotlight border glow */}
        {spotlightRect && (
          <div
            className="absolute transition-all duration-300 ease-out"
            style={{
              top: spotlightRect.top,
              left: spotlightRect.left,
              width: spotlightRect.width,
              height: spotlightRect.height,
              borderRadius: spotlightRect.borderRadius,
              boxShadow: `
                0 0 0 2px rgba(16, 185, 129, 0.6),
                0 0 20px rgba(16, 185, 129, 0.4),
                0 0 40px rgba(16, 185, 129, 0.2),
                inset 0 0 20px rgba(16, 185, 129, 0.1)
              `,
              pointerEvents: 'none',
            }}
          />
        )}
      </div>

      {/* Clickable backdrop to skip */}
      <div
        className="fixed inset-0 z-[9999] cursor-pointer"
        onClick={skipOnboarding}
        style={{ pointerEvents: 'auto' }}
      />

      {/* Tooltip */}
      <div
        ref={tooltipRef}
        className={`
          fixed z-[10000] w-[380px] max-w-[calc(100vw-32px)]
          transition-all duration-300 ease-out
          ${isAnimating ? 'opacity-0 scale-95' : 'opacity-100 scale-100'}
        `}
        style={{
          top: tooltipPosition.top,
          left: tooltipPosition.left,
          pointerEvents: 'auto',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Glass morphism card */}
        <div
          className="relative overflow-hidden rounded-2xl"
          style={{
            background:
              'linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(9, 9, 11, 0.95) 30%, rgba(9, 9, 11, 0.98) 100%)',
            backdropFilter: 'blur(24px)',
            WebkitBackdropFilter: 'blur(24px)',
            border: '1px solid rgba(16, 185, 129, 0.25)',
            boxShadow: `
              0 25px 50px -12px rgba(0, 0, 0, 0.5),
              0 0 0 1px rgba(255, 255, 255, 0.05),
              inset 0 1px 0 rgba(255, 255, 255, 0.1),
              0 0 40px rgba(16, 185, 129, 0.15)
            `,
          }}
        >
          {/* Subtle gradient overlay */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              background:
                'radial-gradient(circle at 20% 20%, rgba(16, 185, 129, 0.1), transparent 50%)',
            }}
          />

          {/* Content */}
          <div className="relative p-6">
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center"
                  style={{
                    background:
                      'linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.05))',
                    border: '1px solid rgba(16, 185, 129, 0.3)',
                  }}
                >
                  <Sparkles className="w-5 h-5 text-emerald-400" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">
                    {currentStep.title}
                  </h3>
                  <p className="text-xs text-zinc-500 mt-0.5">
                    Step {currentStepIndex + 1} of {steps.length}
                  </p>
                </div>
              </div>

              {/* Close button */}
              <button
                onClick={skipOnboarding}
                className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-300 hover:bg-white/5 transition-colors"
                title="Skip tutorial"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Description */}
            <p className="text-sm text-zinc-300 leading-relaxed mb-6">
              {currentStep.description}
            </p>

            {/* Progress dots */}
            <div className="flex items-center justify-center gap-2 mb-5">
              {steps.map((_, index) => (
                <button
                  key={index}
                  onClick={() => {
                    // Navigate to specific step if needed
                  }}
                  className={`
                    transition-all duration-300
                    ${
                      index === currentStepIndex
                        ? 'w-6 h-2 bg-emerald-500 rounded-full shadow-lg shadow-emerald-500/50'
                        : index < currentStepIndex
                        ? 'w-2 h-2 bg-emerald-600/60 rounded-full'
                        : 'w-2 h-2 bg-zinc-700 rounded-full hover:bg-zinc-600'
                    }
                  `}
                  title={`Step ${index + 1}`}
                />
              ))}
            </div>

            {/* Action buttons */}
            <div className="flex items-center justify-between gap-3">
              {/* Skip button */}
              <button
                onClick={skipOnboarding}
                className="px-4 py-2 text-sm text-zinc-400 hover:text-zinc-200 transition-colors"
              >
                Skip tour
              </button>

              <div className="flex items-center gap-2">
                {/* Previous button */}
                {!isFirstStep && (
                  <button
                    onClick={prevStep}
                    className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-medium text-zinc-300 hover:text-white hover:bg-white/5 border border-zinc-700 hover:border-zinc-600 transition-all"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    Back
                  </button>
                )}

                {/* Next/Done button */}
                <button
                  onClick={isLastStep ? completeOnboarding : nextStep}
                  className="flex items-center gap-1.5 px-5 py-2 rounded-xl text-sm font-semibold text-black transition-all"
                  style={{
                    background:
                      'linear-gradient(135deg, #10b981, #059669)',
                    boxShadow: '0 4px 14px rgba(16, 185, 129, 0.4)',
                  }}
                >
                  {isLastStep ? (
                    'Get Started'
                  ) : (
                    <>
                      Next
                      <ChevronRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Arrow indicator */}
          {tooltipPosition.arrowPosition !== 'none' && (
            <TooltipArrow position={tooltipPosition.arrowPosition} />
          )}
        </div>
      </div>
    </>
  );

  return createPortal(tooltipContent, document.body);
}

function TooltipArrow({
  position,
}: {
  position: 'top' | 'bottom' | 'left' | 'right';
}) {
  const baseStyles =
    'absolute w-4 h-4 rotate-45 border-emerald-500/25';
  const bgStyle = {
    background: 'rgba(9, 9, 11, 0.95)',
    borderWidth: '1px',
    borderColor: 'rgba(16, 185, 129, 0.25)',
  };

  switch (position) {
    case 'top':
      return (
        <div
          className={`${baseStyles} -top-2 left-1/2 -translate-x-1/2 border-t border-l`}
          style={{ ...bgStyle, borderRight: 'none', borderBottom: 'none' }}
        />
      );
    case 'bottom':
      return (
        <div
          className={`${baseStyles} -bottom-2 left-1/2 -translate-x-1/2 border-b border-r`}
          style={{ ...bgStyle, borderTop: 'none', borderLeft: 'none' }}
        />
      );
    case 'left':
      return (
        <div
          className={`${baseStyles} -left-2 top-1/2 -translate-y-1/2 border-l border-b`}
          style={{ ...bgStyle, borderTop: 'none', borderRight: 'none' }}
        />
      );
    case 'right':
      return (
        <div
          className={`${baseStyles} -right-2 top-1/2 -translate-y-1/2 border-r border-t`}
          style={{ ...bgStyle, borderBottom: 'none', borderLeft: 'none' }}
        />
      );
    default:
      return null;
  }
}
