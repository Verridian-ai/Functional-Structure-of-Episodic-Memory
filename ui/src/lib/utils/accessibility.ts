/**
 * Accessibility Utilities
 *
 * Provides hooks and utilities for implementing accessible UI components
 * following WCAG 2.1 guidelines.
 */

import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * Keyboard key constants for event handling
 */
export const Keys = {
  Enter: 'Enter',
  Space: ' ',
  Escape: 'Escape',
  Tab: 'Tab',
  ArrowUp: 'ArrowUp',
  ArrowDown: 'ArrowDown',
  ArrowLeft: 'ArrowLeft',
  ArrowRight: 'ArrowRight',
  Home: 'Home',
  End: 'End',
  PageUp: 'PageUp',
  PageDown: 'PageDown',
} as const;

/**
 * Hook for managing focus trap within a container
 * Useful for modals, dialogs, and dropdown menus
 *
 * @example
 * const { containerRef } = useFocusTrap(isOpen);
 * <div ref={containerRef}>...</div>
 */
export function useFocusTrap(enabled: boolean = true) {
  const containerRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!enabled || !containerRef.current) return;

    // Store current focus to restore later
    previousFocusRef.current = document.activeElement as HTMLElement;

    // Get focusable elements
    const getFocusableElements = () => {
      const container = containerRef.current;
      if (!container) return [];

      const focusableSelectors = [
        'button:not([disabled])',
        'input:not([disabled])',
        'select:not([disabled])',
        'textarea:not([disabled])',
        'a[href]',
        '[tabindex]:not([tabindex="-1"])',
      ].join(', ');

      return Array.from(container.querySelectorAll<HTMLElement>(focusableSelectors))
        .filter(el => !el.hasAttribute('disabled') && el.offsetParent !== null);
    };

    // Focus first element
    const focusableElements = getFocusableElements();
    if (focusableElements.length > 0) {
      focusableElements[0].focus();
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key !== Keys.Tab) return;

      const elements = getFocusableElements();
      if (elements.length === 0) return;

      const firstElement = elements[0];
      const lastElement = elements[elements.length - 1];

      if (event.shiftKey) {
        // Shift + Tab
        if (document.activeElement === firstElement) {
          event.preventDefault();
          lastElement.focus();
        }
      } else {
        // Tab
        if (document.activeElement === lastElement) {
          event.preventDefault();
          firstElement.focus();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      // Restore focus when unmounting
      previousFocusRef.current?.focus();
    };
  }, [enabled]);

  return { containerRef };
}

/**
 * Hook for handling Escape key to close modals/menus
 *
 * @example
 * useEscapeKey(() => setIsOpen(false), isOpen);
 */
export function useEscapeKey(onEscape: () => void, enabled: boolean = true) {
  useEffect(() => {
    if (!enabled) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === Keys.Escape) {
        event.preventDefault();
        onEscape();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onEscape, enabled]);
}

/**
 * Hook for arrow key navigation in lists/menus
 *
 * @example
 * const { activeIndex, handleKeyDown } = useArrowNavigation(items.length);
 */
export function useArrowNavigation(
  itemCount: number,
  options: {
    wrap?: boolean;
    orientation?: 'vertical' | 'horizontal' | 'both';
    onSelect?: (index: number) => void;
  } = {}
) {
  const { wrap = true, orientation = 'vertical', onSelect } = options;
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent) => {
      const isVertical = orientation === 'vertical' || orientation === 'both';
      const isHorizontal = orientation === 'horizontal' || orientation === 'both';

      let newIndex = activeIndex;
      let handled = false;

      switch (event.key) {
        case Keys.ArrowUp:
          if (isVertical) {
            newIndex = activeIndex - 1;
            handled = true;
          }
          break;
        case Keys.ArrowDown:
          if (isVertical) {
            newIndex = activeIndex + 1;
            handled = true;
          }
          break;
        case Keys.ArrowLeft:
          if (isHorizontal) {
            newIndex = activeIndex - 1;
            handled = true;
          }
          break;
        case Keys.ArrowRight:
          if (isHorizontal) {
            newIndex = activeIndex + 1;
            handled = true;
          }
          break;
        case Keys.Home:
          newIndex = 0;
          handled = true;
          break;
        case Keys.End:
          newIndex = itemCount - 1;
          handled = true;
          break;
        case Keys.Enter:
        case Keys.Space:
          onSelect?.(activeIndex);
          handled = true;
          break;
      }

      if (handled) {
        event.preventDefault();

        // Handle wrapping or clamping
        if (wrap) {
          newIndex = ((newIndex % itemCount) + itemCount) % itemCount;
        } else {
          newIndex = Math.max(0, Math.min(newIndex, itemCount - 1));
        }

        setActiveIndex(newIndex);
      }
    },
    [activeIndex, itemCount, orientation, wrap, onSelect]
  );

  return { activeIndex, setActiveIndex, handleKeyDown };
}

/**
 * Hook for click outside detection
 *
 * @example
 * const ref = useClickOutside(() => setIsOpen(false));
 */
export function useClickOutside<T extends HTMLElement>(
  callback: () => void,
  enabled: boolean = true
) {
  const ref = useRef<T>(null);

  useEffect(() => {
    if (!enabled) return;

    const handleClick = (event: MouseEvent | TouchEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        callback();
      }
    };

    document.addEventListener('mousedown', handleClick);
    document.addEventListener('touchstart', handleClick);

    return () => {
      document.removeEventListener('mousedown', handleClick);
      document.removeEventListener('touchstart', handleClick);
    };
  }, [callback, enabled]);

  return ref;
}

/**
 * Generate unique IDs for ARIA relationships
 *
 * @example
 * const id = useId('menu');
 * <button aria-controls={id}>Toggle</button>
 * <ul id={id}>...</ul>
 */
let idCounter = 0;

export function generateId(prefix: string = 'verridian'): string {
  return `${prefix}-${++idCounter}`;
}

/**
 * Hook for generating stable unique IDs
 */
export function useStableId(prefix: string = 'verridian'): string {
  const idRef = useRef<string | null>(null);

  if (idRef.current === null) {
    idRef.current = generateId(prefix);
  }

  return idRef.current;
}

/**
 * Visually hidden span for screen readers
 * Use for providing additional context that's visually redundant
 */
export const visuallyHiddenStyles: React.CSSProperties = {
  position: 'absolute',
  width: '1px',
  height: '1px',
  padding: 0,
  margin: '-1px',
  overflow: 'hidden',
  clip: 'rect(0, 0, 0, 0)',
  whiteSpace: 'nowrap',
  border: 0,
};

/**
 * ARIA live region announcements
 *
 * @example
 * const { announce } = useAnnounce();
 * announce('Item deleted');
 */
export function useAnnounce() {
  const announce = useCallback(
    (message: string, priority: 'polite' | 'assertive' = 'polite') => {
      const announcement = document.createElement('div');
      announcement.setAttribute('role', 'status');
      announcement.setAttribute('aria-live', priority);
      announcement.setAttribute('aria-atomic', 'true');
      Object.assign(announcement.style, visuallyHiddenStyles);
      announcement.textContent = message;

      document.body.appendChild(announcement);

      // Remove after announcement is made
      setTimeout(() => {
        document.body.removeChild(announcement);
      }, 1000);
    },
    []
  );

  return { announce };
}

/**
 * Check if reduced motion is preferred
 */
export function usePrefersReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
}

/**
 * Props for accessible buttons that act as toggles
 */
export function getToggleButtonProps(isPressed: boolean) {
  return {
    role: 'button',
    'aria-pressed': isPressed,
    tabIndex: 0,
    onKeyDown: (event: React.KeyboardEvent) => {
      if (event.key === Keys.Enter || event.key === Keys.Space) {
        event.preventDefault();
        (event.target as HTMLElement).click();
      }
    },
  };
}

/**
 * Props for accessible expandable sections
 */
export function getExpandableProps(
  isExpanded: boolean,
  contentId: string
) {
  return {
    trigger: {
      'aria-expanded': isExpanded,
      'aria-controls': contentId,
    },
    content: {
      id: contentId,
      role: 'region',
      hidden: !isExpanded,
    },
  };
}

export default {
  Keys,
  useFocusTrap,
  useEscapeKey,
  useArrowNavigation,
  useClickOutside,
  generateId,
  useStableId,
  visuallyHiddenStyles,
  useAnnounce,
  usePrefersReducedMotion,
  getToggleButtonProps,
  getExpandableProps,
};
