/**
 * Performance Utilities
 *
 * Utilities for optimizing React component performance including
 * memoization helpers, debouncing, throttling, and virtual list helpers.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

/**
 * Deep equality comparison for React.memo
 * Use for complex objects where shallow comparison isn't sufficient
 *
 * @example
 * const MemoizedComponent = React.memo(MyComponent, deepCompare);
 */
export function deepCompare<T>(prevProps: T, nextProps: T): boolean {
  return JSON.stringify(prevProps) === JSON.stringify(nextProps);
}

/**
 * Shallow comparison with specific keys
 * Use when you only want to compare certain props
 *
 * @example
 * const MemoizedComponent = React.memo(MyComponent, compareKeys(['id', 'name']));
 */
export function compareKeys<T extends Record<string, unknown>>(
  keys: (keyof T)[]
): (prev: T, next: T) => boolean {
  return (prev: T, next: T) => {
    return keys.every((key) => prev[key] === next[key]);
  };
}

/**
 * Hook for debounced values
 * Useful for search inputs, API calls, etc.
 *
 * @example
 * const debouncedSearch = useDebounce(searchTerm, 300);
 */
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

/**
 * Hook for debounced callbacks
 *
 * @example
 * const debouncedSave = useDebouncedCallback((data) => save(data), 500);
 */
export function useDebouncedCallback<T extends (...args: Parameters<T>) => ReturnType<T>>(
  callback: T,
  delay: number
): (...args: Parameters<T>) => void {
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const callbackRef = useRef(callback);

  // Keep callback ref updated
  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return useCallback(
    (...args: Parameters<T>) => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      timeoutRef.current = setTimeout(() => {
        callbackRef.current(...args);
      }, delay);
    },
    [delay]
  );
}

/**
 * Hook for throttled callbacks
 * Ensures function is called at most once per interval
 *
 * @example
 * const throttledScroll = useThrottledCallback(handleScroll, 100);
 */
export function useThrottledCallback<T extends (...args: Parameters<T>) => ReturnType<T>>(
  callback: T,
  interval: number
): (...args: Parameters<T>) => void {
  const lastCallRef = useRef<number>(0);
  const callbackRef = useRef(callback);

  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  return useCallback(
    (...args: Parameters<T>) => {
      const now = Date.now();
      if (now - lastCallRef.current >= interval) {
        lastCallRef.current = now;
        callbackRef.current(...args);
      }
    },
    [interval]
  );
}

/**
 * Hook for lazy initialization of expensive computations
 *
 * @example
 * const expensiveData = useLazyInit(() => computeExpensiveData());
 */
export function useLazyInit<T>(factory: () => T): T {
  const ref = useRef<{ value: T } | null>(null);

  if (ref.current === null) {
    ref.current = { value: factory() };
  }

  return ref.current.value;
}

/**
 * Hook for tracking previous value
 * Useful for comparing current and previous props/state
 *
 * @example
 * const prevCount = usePrevious(count);
 */
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

/**
 * Hook for memoizing expensive computations with dependencies
 * Similar to useMemo but with additional options
 *
 * @example
 * const processed = useDeepMemo(() => processData(data), [data]);
 */
export function useDeepMemo<T>(factory: () => T, deps: unknown[]): T {
  const ref = useRef<{ deps: unknown[]; value: T } | null>(null);

  if (ref.current === null || !deepArrayCompare(ref.current.deps, deps)) {
    ref.current = { deps, value: factory() };
  }

  return ref.current.value;
}

function deepArrayCompare(a: unknown[], b: unknown[]): boolean {
  if (a.length !== b.length) return false;
  return a.every((item, index) => JSON.stringify(item) === JSON.stringify(b[index]));
}

/**
 * Hook for intersection observer (lazy loading, infinite scroll)
 *
 * @example
 * const { ref, isIntersecting } = useIntersectionObserver({ threshold: 0.5 });
 */
export function useIntersectionObserver<T extends HTMLElement>(
  options: IntersectionObserverInit = {}
): {
  ref: React.RefObject<T | null>;
  isIntersecting: boolean;
  entry: IntersectionObserverEntry | null;
} {
  const ref = useRef<T | null>(null);
  const [entry, setEntry] = useState<IntersectionObserverEntry | null>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(([entry]) => {
      setEntry(entry);
    }, options);

    observer.observe(element);

    return () => observer.disconnect();
  }, [options.root, options.rootMargin, options.threshold]);

  return {
    ref,
    isIntersecting: entry?.isIntersecting ?? false,
    entry,
  };
}

/**
 * Virtual list item data for windowed rendering
 */
export interface VirtualItem {
  index: number;
  start: number;
  size: number;
}

/**
 * Hook for basic virtual list rendering
 *
 * @example
 * const { virtualItems, totalSize } = useVirtualList({
 *   count: items.length,
 *   estimateSize: () => 50,
 *   overscan: 5,
 * });
 */
export function useVirtualList(options: {
  count: number;
  estimateSize: (index: number) => number;
  overscan?: number;
  containerHeight: number;
  scrollOffset?: number;
}): {
  virtualItems: VirtualItem[];
  totalSize: number;
} {
  const { count, estimateSize, overscan = 3, containerHeight, scrollOffset = 0 } = options;

  const measurements = useMemo(() => {
    const sizes: number[] = [];
    const starts: number[] = [];
    let totalSize = 0;

    for (let i = 0; i < count; i++) {
      const size = estimateSize(i);
      sizes.push(size);
      starts.push(totalSize);
      totalSize += size;
    }

    return { sizes, starts, totalSize };
  }, [count, estimateSize]);

  const virtualItems = useMemo(() => {
    const items: VirtualItem[] = [];

    // Find first visible item
    let startIndex = 0;
    for (let i = 0; i < count; i++) {
      if (measurements.starts[i] + measurements.sizes[i] > scrollOffset) {
        startIndex = Math.max(0, i - overscan);
        break;
      }
    }

    // Find last visible item
    let endIndex = count - 1;
    for (let i = startIndex; i < count; i++) {
      if (measurements.starts[i] > scrollOffset + containerHeight) {
        endIndex = Math.min(count - 1, i + overscan);
        break;
      }
    }

    // Generate virtual items
    for (let i = startIndex; i <= endIndex; i++) {
      items.push({
        index: i,
        start: measurements.starts[i],
        size: measurements.sizes[i],
      });
    }

    return items;
  }, [count, measurements, scrollOffset, containerHeight, overscan]);

  return {
    virtualItems,
    totalSize: measurements.totalSize,
  };
}

/**
 * Request idle callback polyfill hook
 * Use for non-critical updates that can wait for browser idle time
 *
 * @example
 * const scheduleUpdate = useIdleCallback((data) => processData(data));
 */
export function useIdleCallback<T extends (...args: Parameters<T>) => void>(
  callback: T,
  options: { timeout?: number } = {}
): (...args: Parameters<T>) => void {
  const callbackRef = useRef(callback);

  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  return useCallback(
    (...args: Parameters<T>) => {
      const ric = window.requestIdleCallback || ((cb) => setTimeout(cb, 1));
      ric(() => callbackRef.current(...args), options);
    },
    [options.timeout]
  );
}

export default {
  deepCompare,
  compareKeys,
  useDebounce,
  useDebouncedCallback,
  useThrottledCallback,
  useLazyInit,
  usePrevious,
  useDeepMemo,
  useIntersectionObserver,
  useVirtualList,
  useIdleCallback,
};
