/**
 * UI Components Library
 *
 * Pro-level UI components with:
 * - Full TypeScript support
 * - Accessibility (WCAG 2.1 AA compliant)
 * - Reduced motion support
 * - Light/dark theme support
 * - Mobile-first responsive design
 */

// Core Components
export { Button, IconButton } from './Button';
export type { ButtonProps } from './Button';

export { ErrorBoundary, useErrorHandler, withErrorBoundary } from './ErrorBoundary';
export { SkipLinks } from './SkipLinks';
export { VisuallyHidden } from './VisuallyHidden';
export { SafeHtmlProse } from './SafeHtml';
export { Skeleton, SkeletonText, SkeletonCircle, SkeletonCard } from './Skeleton';
export { SynapseLoader } from './SynapseLoader';

// Toast System
export { ToastProvider, useToast, toast } from './Toast';
export type { default as ToastProviderType } from './Toast';
