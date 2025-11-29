/**
 * Utility Functions Index
 *
 * Centralized exports for all utility modules.
 */

// Security utilities
export {
  sanitizeHtml,
  sanitizeUserContent,
  sanitizeUrl,
  escapeHtml,
  sanitizeInput,
  isValidUrl,
  isContentSafe,
} from './security';

// Error handling utilities
export {
  AppError,
  parseApiError,
  tryCatch,
  tryCatchSync,
  withRetry,
  logError,
  formatErrorForDisplay,
  type ErrorCategory,
} from './errorHandling';

// Accessibility utilities
export {
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
} from './accessibility';

// Performance utilities
export {
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
  type VirtualItem,
} from './performance';

// Default export with all utilities grouped
export { default as security } from './security';
export { default as errorHandling } from './errorHandling';
export { default as accessibility } from './accessibility';
export { default as performance } from './performance';
