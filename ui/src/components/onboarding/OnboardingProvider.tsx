'use client';

import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  ReactNode,
} from 'react';

// Define the onboarding steps
export interface OnboardingStep {
  id: string;
  targetId: string; // ID of the element to highlight
  title: string;
  description: string;
  position: 'top' | 'bottom' | 'left' | 'right' | 'center';
  spotlightPadding?: number;
}

// Default onboarding steps for Law OS
export const DEFAULT_ONBOARDING_STEPS: OnboardingStep[] = [
  {
    id: 'brain-visualization',
    targetId: 'brain-visualization',
    title: 'Neural Legal Brain',
    description:
      'This 3D visualization represents the AI\'s neural network. It reacts to your voice and mouse movements, symbolizing how the system processes and connects legal concepts in real-time.',
    position: 'center',
    spotlightPadding: 0,
  },
  {
    id: 'chat-input',
    targetId: 'chat-input-container',
    title: 'Ask Legal Questions',
    description:
      'Type your legal questions here. You can ask about case law, draft documents, review contracts, or get explanations of legal statutes. Press Enter to send or Shift+Enter for a new line.',
    position: 'top',
    spotlightPadding: 12,
  },
  {
    id: 'voice-input',
    targetId: 'voice-input-button',
    title: 'Voice Input',
    description:
      'Click the microphone icon or hold the Spacebar to speak your questions. The AI will transcribe and respond to your voice commands for hands-free operation.',
    position: 'top',
    spotlightPadding: 8,
  },
  {
    id: 'quick-actions',
    targetId: 'quick-actions-container',
    title: 'Quick Actions',
    description:
      'Use these shortcuts to quickly start common legal tasks like finding precedents, reviewing contracts, drafting letters, or explaining statutes.',
    position: 'top',
    spotlightPadding: 8,
  },
  {
    id: 'canvas-panel',
    targetId: 'canvas-toggle-button',
    title: 'Document Canvas',
    description:
      'Toggle the Canvas panel to view and edit generated documents. Export to Word, PDF, or use templates for legal briefs, reports, and newsletters.',
    position: 'right',
    spotlightPadding: 8,
  },
  {
    id: 'new-project',
    targetId: 'new-project-button',
    title: 'Start New Projects',
    description:
      'Click here to start a fresh conversation. Your previous conversations are saved in the sidebar for easy reference.',
    position: 'bottom',
    spotlightPadding: 8,
  },
];

interface OnboardingContextType {
  // State
  isOnboardingActive: boolean;
  currentStepIndex: number;
  currentStep: OnboardingStep | null;
  steps: OnboardingStep[];
  hasCompletedOnboarding: boolean;
  showWelcomeModal: boolean;

  // Actions
  startOnboarding: () => void;
  nextStep: () => void;
  prevStep: () => void;
  skipOnboarding: () => void;
  completeOnboarding: () => void;
  resetOnboarding: () => void;
  closeWelcomeModal: () => void;
  openWelcomeModal: () => void;
  goToStep: (index: number) => void;
}

const OnboardingContext = createContext<OnboardingContextType | undefined>(
  undefined
);

const STORAGE_KEY = 'verridian-law-os-onboarding-completed';
const WELCOME_SHOWN_KEY = 'verridian-law-os-welcome-shown';

interface OnboardingProviderProps {
  children: ReactNode;
  steps?: OnboardingStep[];
}

export function OnboardingProvider({
  children,
  steps = DEFAULT_ONBOARDING_STEPS,
}: OnboardingProviderProps) {
  const [isOnboardingActive, setIsOnboardingActive] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [hasCompletedOnboarding, setHasCompletedOnboarding] = useState(true); // Default true to prevent flash
  const [showWelcomeModal, setShowWelcomeModal] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  // Load completion status from localStorage on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const completed = localStorage.getItem(STORAGE_KEY);
      const welcomeShown = localStorage.getItem(WELCOME_SHOWN_KEY);

      setHasCompletedOnboarding(completed === 'true');

      // Show welcome modal if first time
      if (!welcomeShown) {
        setShowWelcomeModal(true);
      }

      setIsInitialized(true);
    }
  }, []);

  const currentStep =
    isOnboardingActive && steps[currentStepIndex]
      ? steps[currentStepIndex]
      : null;

  const startOnboarding = useCallback(() => {
    setShowWelcomeModal(false);
    setCurrentStepIndex(0);
    setIsOnboardingActive(true);
  }, []);

  const nextStep = useCallback(() => {
    if (currentStepIndex < steps.length - 1) {
      setCurrentStepIndex((prev) => prev + 1);
    } else {
      // Complete onboarding
      setIsOnboardingActive(false);
      setHasCompletedOnboarding(true);
      if (typeof window !== 'undefined') {
        localStorage.setItem(STORAGE_KEY, 'true');
      }
    }
  }, [currentStepIndex, steps.length]);

  const prevStep = useCallback(() => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex((prev) => prev - 1);
    }
  }, [currentStepIndex]);

  const goToStep = useCallback(
    (index: number) => {
      if (index >= 0 && index < steps.length) {
        setCurrentStepIndex(index);
      }
    },
    [steps.length]
  );

  const skipOnboarding = useCallback(() => {
    setIsOnboardingActive(false);
    setShowWelcomeModal(false);
    setHasCompletedOnboarding(true);
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, 'true');
      localStorage.setItem(WELCOME_SHOWN_KEY, 'true');
    }
  }, []);

  const completeOnboarding = useCallback(() => {
    setIsOnboardingActive(false);
    setHasCompletedOnboarding(true);
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, 'true');
      localStorage.setItem(WELCOME_SHOWN_KEY, 'true');
    }
  }, []);

  const resetOnboarding = useCallback(() => {
    setHasCompletedOnboarding(false);
    setCurrentStepIndex(0);
    setShowWelcomeModal(true);
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem(WELCOME_SHOWN_KEY);
    }
  }, []);

  const closeWelcomeModal = useCallback(() => {
    setShowWelcomeModal(false);
    if (typeof window !== 'undefined') {
      localStorage.setItem(WELCOME_SHOWN_KEY, 'true');
    }
  }, []);

  const openWelcomeModal = useCallback(() => {
    setShowWelcomeModal(true);
  }, []);

  const value: OnboardingContextType = {
    isOnboardingActive,
    currentStepIndex,
    currentStep,
    steps,
    hasCompletedOnboarding,
    showWelcomeModal: isInitialized ? showWelcomeModal : false,
    startOnboarding,
    nextStep,
    prevStep,
    skipOnboarding,
    completeOnboarding,
    resetOnboarding,
    closeWelcomeModal,
    openWelcomeModal,
    goToStep,
  };

  return (
    <OnboardingContext.Provider value={value}>
      {children}
    </OnboardingContext.Provider>
  );
}

export function useOnboarding(): OnboardingContextType {
  const context = useContext(OnboardingContext);
  if (context === undefined) {
    throw new Error('useOnboarding must be used within an OnboardingProvider');
  }
  return context;
}

// Hook to check if a specific element is the current target
export function useIsOnboardingTarget(targetId: string): boolean {
  const { isOnboardingActive, currentStep } = useOnboarding();
  return isOnboardingActive && currentStep?.targetId === targetId;
}
