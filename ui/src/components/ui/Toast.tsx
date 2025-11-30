'use client';

import React, { createContext, useContext, useCallback, useState, useEffect, ReactNode } from 'react';
import { X, CheckCircle, AlertTriangle, Info, AlertCircle } from 'lucide-react';

// Toast types
type ToastType = 'success' | 'error' | 'warning' | 'info';

interface Toast {
  id: string;
  type: ToastType;
  title: string;
  message?: string;
  duration?: number;
  dismissible?: boolean;
}

interface ToastContextValue {
  toasts: Toast[];
  addToast: (toast: Omit<Toast, 'id'>) => string;
  removeToast: (id: string) => void;
  clearToasts: () => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

/**
 * Hook to access toast notifications
 *
 * @example
 * const { addToast } = useToast();
 * addToast({ type: 'success', title: 'Saved!', message: 'Your changes have been saved.' });
 */
export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}

interface ToastProviderProps {
  children: ReactNode;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
  maxToasts?: number;
}

/**
 * Toast Provider Component
 *
 * Wrap your app with this provider to enable toast notifications.
 *
 * @example
 * <ToastProvider position="bottom-center" maxToasts={5}>
 *   <App />
 * </ToastProvider>
 */
export function ToastProvider({ children, position = 'bottom-center', maxToasts = 5 }: ToastProviderProps) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((toast: Omit<Toast, 'id'>): string => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
    const newToast: Toast = {
      ...toast,
      id,
      duration: toast.duration ?? (toast.type === 'error' ? 8000 : 5000),
      dismissible: toast.dismissible ?? true,
    };

    setToasts(prev => {
      const updated = [...prev, newToast];
      // Limit number of toasts
      return updated.slice(-maxToasts);
    });

    return id;
  }, [maxToasts]);

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  }, []);

  const clearToasts = useCallback(() => {
    setToasts([]);
  }, []);

  // Position classes
  const positionClasses: Record<string, string> = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'top-center': 'top-4 left-1/2 -translate-x-1/2',
    'bottom-center': 'bottom-4 left-1/2 -translate-x-1/2',
  };

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast, clearToasts }}>
      {children}
      {/* Toast Container */}
      <div
        className={`fixed z-50 flex flex-col gap-2 max-w-md w-full px-4 pointer-events-none ${positionClasses[position]}`}
        aria-live="polite"
        aria-label="Notifications"
      >
        {toasts.map(toast => (
          <ToastItem
            key={toast.id}
            toast={toast}
            onRemove={() => removeToast(toast.id)}
          />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

// Toast item component
interface ToastItemProps {
  toast: Toast;
  onRemove: () => void;
}

function ToastItem({ toast, onRemove }: ToastItemProps) {
  const [isExiting, setIsExiting] = useState(false);

  // Auto-dismiss
  useEffect(() => {
    if (toast.duration && toast.duration > 0) {
      const timer = setTimeout(() => {
        setIsExiting(true);
        setTimeout(onRemove, 200); // Wait for exit animation
      }, toast.duration);

      return () => clearTimeout(timer);
    }
  }, [toast.duration, onRemove]);

  const handleDismiss = () => {
    setIsExiting(true);
    setTimeout(onRemove, 200);
  };

  // Type-specific styles and icons
  const typeConfig: Record<ToastType, { icon: typeof CheckCircle; bgClass: string; iconClass: string; borderClass: string }> = {
    success: {
      icon: CheckCircle,
      bgClass: 'bg-emerald-900/90',
      iconClass: 'text-emerald-400',
      borderClass: 'border-emerald-700/50',
    },
    error: {
      icon: AlertCircle,
      bgClass: 'bg-red-900/90',
      iconClass: 'text-red-400',
      borderClass: 'border-red-700/50',
    },
    warning: {
      icon: AlertTriangle,
      bgClass: 'bg-amber-900/90',
      iconClass: 'text-amber-400',
      borderClass: 'border-amber-700/50',
    },
    info: {
      icon: Info,
      bgClass: 'bg-blue-900/90',
      iconClass: 'text-blue-400',
      borderClass: 'border-blue-700/50',
    },
  };

  const config = typeConfig[toast.type];
  const Icon = config.icon;

  return (
    <div
      role="alert"
      aria-live={toast.type === 'error' ? 'assertive' : 'polite'}
      className={`
        pointer-events-auto flex items-start gap-3 p-4 rounded-xl border backdrop-blur-sm shadow-lg
        transition-all duration-200 ease-out
        ${config.bgClass} ${config.borderClass}
        ${isExiting ? 'opacity-0 scale-95 translate-y-2' : 'opacity-100 scale-100 translate-y-0'}
      `}
    >
      <Icon className={`w-5 h-5 flex-shrink-0 mt-0.5 ${config.iconClass}`} aria-hidden="true" />
      <div className="flex-1 min-w-0">
        <p className="font-medium text-white">{toast.title}</p>
        {toast.message && (
          <p className="mt-1 text-sm text-zinc-300">{toast.message}</p>
        )}
      </div>
      {toast.dismissible && (
        <button
          onClick={handleDismiss}
          className="flex-shrink-0 p-1 hover:bg-white/10 rounded transition"
          aria-label="Dismiss notification"
        >
          <X className="w-4 h-4 text-zinc-400" />
        </button>
      )}
    </div>
  );
}

// Convenience functions for creating toasts
export const toast = {
  success: (title: string, message?: string, options?: Partial<Toast>) => {
    // This is a placeholder - actual implementation uses the hook
    console.log('Toast:', { type: 'success', title, message, ...options });
  },
  error: (title: string, message?: string, options?: Partial<Toast>) => {
    console.log('Toast:', { type: 'error', title, message, ...options });
  },
  warning: (title: string, message?: string, options?: Partial<Toast>) => {
    console.log('Toast:', { type: 'warning', title, message, ...options });
  },
  info: (title: string, message?: string, options?: Partial<Toast>) => {
    console.log('Toast:', { type: 'info', title, message, ...options });
  },
};

export default ToastProvider;
