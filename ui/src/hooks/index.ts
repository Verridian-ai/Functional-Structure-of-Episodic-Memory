/**
 * Hooks Library
 *
 * Custom React hooks for common functionality:
 * - Viewport and responsive design
 * - Theme management
 * - Sound effects
 * - Accessibility utilities
 */

// Mobile and viewport hooks
export {
  useMobile,
  useTouchDevice,
  useSafeArea,
  useViewportHeight,
  useOrientation,
  useStandalone,
  useSwipe,
  breakpoints,
} from './useMobile';
export type { default as UseMobileType } from './useMobile';

// Theme management
export { useTheme } from './useTheme';
export type { Theme, ResolvedTheme } from './useTheme';

// Sound effects
export { useSound } from './useSound';
