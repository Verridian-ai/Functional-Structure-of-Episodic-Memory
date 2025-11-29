'use client';

import { useState, useEffect, useCallback } from 'react';

/**
 * Breakpoints matching Tailwind CSS defaults
 */
export const breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536,
} as const;

type Breakpoint = keyof typeof breakpoints;

/**
 * Hook to detect mobile/tablet/desktop viewports
 *
 * @example
 * const { isMobile, isTablet, isDesktop } = useMobile();
 */
export function useMobile() {
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 1024,
    height: typeof window !== 'undefined' ? window.innerHeight : 768,
  });

  useEffect(() => {
    // Only run on client
    if (typeof window === 'undefined') return;

    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Set initial size
    handleResize();

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const isMobile = windowSize.width < breakpoints.md;
  const isTablet = windowSize.width >= breakpoints.md && windowSize.width < breakpoints.lg;
  const isDesktop = windowSize.width >= breakpoints.lg;

  const isBelow = useCallback(
    (breakpoint: Breakpoint) => windowSize.width < breakpoints[breakpoint],
    [windowSize.width]
  );

  const isAbove = useCallback(
    (breakpoint: Breakpoint) => windowSize.width >= breakpoints[breakpoint],
    [windowSize.width]
  );

  return {
    isMobile,
    isTablet,
    isDesktop,
    isBelow,
    isAbove,
    width: windowSize.width,
    height: windowSize.height,
  };
}

/**
 * Hook for detecting touch devices
 */
export function useTouchDevice() {
  const [isTouch, setIsTouch] = useState(() => {
    if (typeof window === 'undefined') return false;
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  });

  // Re-check on mount in case SSR value differs
  useEffect(() => {
    const touchSupported = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    if (touchSupported !== isTouch) {
      setIsTouch(touchSupported);
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return isTouch;
}

/**
 * Hook for safe area insets (notch, home indicator)
 */
export function useSafeArea() {
  const [insets, setInsets] = useState({
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
  });

  useEffect(() => {
    const root = document.documentElement;

    const updateInsets = () => {
      const styles = getComputedStyle(root);
      setInsets({
        top: parseInt(styles.getPropertyValue('--sat') || '0', 10),
        right: parseInt(styles.getPropertyValue('--sar') || '0', 10),
        bottom: parseInt(styles.getPropertyValue('--sab') || '0', 10),
        left: parseInt(styles.getPropertyValue('--sal') || '0', 10),
      });
    };

    // Set CSS variables for safe area
    root.style.setProperty('--sat', 'env(safe-area-inset-top)');
    root.style.setProperty('--sar', 'env(safe-area-inset-right)');
    root.style.setProperty('--sab', 'env(safe-area-inset-bottom)');
    root.style.setProperty('--sal', 'env(safe-area-inset-left)');

    updateInsets();
    window.addEventListener('resize', updateInsets);
    return () => window.removeEventListener('resize', updateInsets);
  }, []);

  return insets;
}

/**
 * Hook for viewport height (handles mobile browser chrome)
 * Returns the actual visible viewport height
 */
export function useViewportHeight() {
  const [height, setHeight] = useState(
    typeof window !== 'undefined' ? window.innerHeight : 0
  );

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const updateHeight = () => {
      // Use visualViewport if available (better for mobile)
      const vh = window.visualViewport?.height || window.innerHeight;
      setHeight(vh);
      // Also set CSS variable for use in styles
      document.documentElement.style.setProperty('--vh', `${vh * 0.01}px`);
    };

    updateHeight();

    // Listen to both resize and visualViewport changes
    window.addEventListener('resize', updateHeight);
    window.visualViewport?.addEventListener('resize', updateHeight);

    return () => {
      window.removeEventListener('resize', updateHeight);
      window.visualViewport?.removeEventListener('resize', updateHeight);
    };
  }, []);

  return height;
}

/**
 * Hook for orientation detection
 */
export function useOrientation() {
  const [orientation, setOrientation] = useState<'portrait' | 'landscape'>('portrait');

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const updateOrientation = () => {
      setOrientation(
        window.innerWidth > window.innerHeight ? 'landscape' : 'portrait'
      );
    };

    updateOrientation();
    window.addEventListener('resize', updateOrientation);
    return () => window.removeEventListener('resize', updateOrientation);
  }, []);

  return orientation;
}

/**
 * Hook for detecting standalone mode (PWA installed)
 */
export function useStandalone() {
  const [isStandalone, setIsStandalone] = useState(() => {
    if (typeof window === 'undefined') return false;
    return (
      window.matchMedia('(display-mode: standalone)').matches ||
      (window.navigator as Navigator & { standalone?: boolean }).standalone === true
    );
  });

  // Re-check on mount in case SSR value differs
  useEffect(() => {
    const standalone =
      window.matchMedia('(display-mode: standalone)').matches ||
      (window.navigator as Navigator & { standalone?: boolean }).standalone === true;
    if (standalone !== isStandalone) {
      setIsStandalone(standalone);
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return isStandalone;
}

/**
 * Hook for swipe gestures
 */
export function useSwipe(
  onSwipeLeft?: () => void,
  onSwipeRight?: () => void,
  onSwipeUp?: () => void,
  onSwipeDown?: () => void,
  threshold = 50
) {
  const [touchStart, setTouchStart] = useState<{ x: number; y: number } | null>(null);

  const handleTouchStart = useCallback((e: React.TouchEvent | TouchEvent) => {
    setTouchStart({
      x: e.touches[0].clientX,
      y: e.touches[0].clientY,
    });
  }, []);

  const handleTouchEnd = useCallback(
    (e: React.TouchEvent | TouchEvent) => {
      if (!touchStart) return;

      const deltaX = e.changedTouches[0].clientX - touchStart.x;
      const deltaY = e.changedTouches[0].clientY - touchStart.y;

      const absX = Math.abs(deltaX);
      const absY = Math.abs(deltaY);

      // Determine if horizontal or vertical swipe
      if (absX > absY && absX > threshold) {
        if (deltaX > 0) {
          onSwipeRight?.();
        } else {
          onSwipeLeft?.();
        }
      } else if (absY > absX && absY > threshold) {
        if (deltaY > 0) {
          onSwipeDown?.();
        } else {
          onSwipeUp?.();
        }
      }

      setTouchStart(null);
    },
    [touchStart, threshold, onSwipeLeft, onSwipeRight, onSwipeUp, onSwipeDown]
  );

  return {
    onTouchStart: handleTouchStart,
    onTouchEnd: handleTouchEnd,
  };
}

export default useMobile;
