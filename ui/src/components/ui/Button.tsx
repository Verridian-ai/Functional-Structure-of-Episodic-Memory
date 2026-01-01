'use client';

import React, { forwardRef, ButtonHTMLAttributes, AnchorHTMLAttributes } from 'react';
import { Loader2 } from 'lucide-react';
import Link from 'next/link';

// ============================================================================
// Button Variants and Types
// ============================================================================

type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'success';
type ButtonSize = 'xs' | 'sm' | 'md' | 'lg';

interface BaseButtonProps {
  /** Visual variant of the button */
  variant?: ButtonVariant;
  /** Size of the button */
  size?: ButtonSize;
  /** Show loading spinner */
  loading?: boolean;
  /** Icon to show before children */
  leftIcon?: React.ReactNode;
  /** Icon to show after children */
  rightIcon?: React.ReactNode;
  /** Make button full width */
  fullWidth?: boolean;
  /** Whether button is disabled */
  disabled?: boolean;
  /** Additional CSS classes */
  className?: string;
  /** Children elements */
  children?: React.ReactNode;
}

type ButtonAsButton = BaseButtonProps &
  Omit<ButtonHTMLAttributes<HTMLButtonElement>, keyof BaseButtonProps> & {
    as?: 'button';
    href?: never;
  };

type ButtonAsLink = BaseButtonProps &
  Omit<AnchorHTMLAttributes<HTMLAnchorElement>, keyof BaseButtonProps> & {
    as: 'a';
    href: string;
  };

type ButtonAsNextLink = BaseButtonProps & {
  as: 'link';
  href: string;
};

export type ButtonProps = ButtonAsButton | ButtonAsLink | ButtonAsNextLink;

// ============================================================================
// Style Maps
// ============================================================================

const variantStyles: Record<ButtonVariant, string> = {
  primary: `
    bg-cyan-600 text-white
    hover:bg-cyan-500 active:bg-cyan-400
    focus-visible:ring-cyan-500/50
    disabled:bg-cyan-600/50
    shadow-sm shadow-cyan-500/20
  `,
  secondary: `
    bg-zinc-800 text-zinc-100 border border-zinc-700
    hover:bg-zinc-700 hover:border-zinc-600 active:bg-zinc-600
    focus-visible:ring-zinc-500/50
    disabled:bg-zinc-800/50 disabled:border-zinc-800
  `,
  ghost: `
    bg-transparent text-zinc-300
    hover:bg-white/10 hover:text-white active:bg-white/15
    focus-visible:ring-white/30
    disabled:text-zinc-600
  `,
  danger: `
    bg-red-600 text-white
    hover:bg-red-500 active:bg-red-400
    focus-visible:ring-red-500/50
    disabled:bg-red-600/50
    shadow-sm shadow-red-500/20
  `,
  success: `
    bg-emerald-600 text-white
    hover:bg-emerald-500 active:bg-emerald-400
    focus-visible:ring-emerald-500/50
    disabled:bg-emerald-600/50
    shadow-sm shadow-emerald-500/20
  `,
};

const sizeStyles: Record<ButtonSize, string> = {
  xs: 'h-7 px-2 text-xs gap-1 rounded-md',
  sm: 'h-8 px-3 text-sm gap-1.5 rounded-lg',
  md: 'h-10 px-4 text-sm gap-2 rounded-xl',
  lg: 'h-12 px-6 text-base gap-2.5 rounded-xl',
};

const iconSizes: Record<ButtonSize, string> = {
  xs: 'w-3 h-3',
  sm: 'w-3.5 h-3.5',
  md: 'w-4 h-4',
  lg: 'w-5 h-5',
};

// ============================================================================
// Button Component
// ============================================================================

/**
 * Pro-level Button component with multiple variants, sizes, and states
 *
 * Features:
 * - Multiple visual variants (primary, secondary, ghost, danger, success)
 * - Multiple sizes (xs, sm, md, lg)
 * - Loading state with spinner
 * - Left and right icon support
 * - Polymorphic: can render as button, anchor, or Next.js Link
 * - Full keyboard and accessibility support
 * - Touch-optimized with 44px minimum targets on mobile
 *
 * @example
 * // Primary button
 * <Button variant="primary" onClick={handleClick}>Save Changes</Button>
 *
 * @example
 * // Button with loading state
 * <Button loading={isSubmitting}>Submit</Button>
 *
 * @example
 * // Button as a link
 * <Button as="link" href="/dashboard" leftIcon={<Home />}>Dashboard</Button>
 */
export const Button = forwardRef<
  HTMLButtonElement | HTMLAnchorElement,
  ButtonProps
>((props, ref) => {
  const {
    variant = 'primary',
    size = 'md',
    loading = false,
    leftIcon,
    rightIcon,
    fullWidth = false,
    className = '',
    children,
    disabled,
    ...rest
  } = props;

  const isDisabled = disabled || loading;

  // Build class string
  const baseClasses = `
    inline-flex items-center justify-center font-medium
    transition-all duration-200 ease-out
    focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-zinc-950
    disabled:cursor-not-allowed disabled:opacity-60
    touch-target select-none
    motion-safe:active:scale-[0.98]
  `;

  const classes = [
    baseClasses,
    variantStyles[variant],
    sizeStyles[size],
    fullWidth && 'w-full',
    className,
  ]
    .filter(Boolean)
    .join(' ')
    .replace(/\s+/g, ' ')
    .trim();

  const iconClass = iconSizes[size];

  // Content with icons
  const content = (
    <>
      {loading ? (
        <Loader2 className={`${iconClass} animate-spin`} aria-hidden="true" />
      ) : leftIcon ? (
        <span className={iconClass} aria-hidden="true">{leftIcon}</span>
      ) : null}
      {children && <span className="truncate">{children}</span>}
      {rightIcon && !loading && (
        <span className={iconClass} aria-hidden="true">{rightIcon}</span>
      )}
    </>
  );

  // Render as Next.js Link
  if (props.as === 'link') {
    return (
      <Link
        ref={ref as React.Ref<HTMLAnchorElement>}
        href={props.href}
        className={classes}
        aria-disabled={isDisabled}
        {...(rest as Omit<typeof rest, 'as' | 'href'>)}
      >
        {content}
      </Link>
    );
  }

  // Render as anchor
  if (props.as === 'a') {
    return (
      <a
        ref={ref as React.Ref<HTMLAnchorElement>}
        className={classes}
        aria-disabled={isDisabled}
        {...(rest as AnchorHTMLAttributes<HTMLAnchorElement>)}
      >
        {content}
      </a>
    );
  }

  // Render as button (default)
  return (
    <button
      ref={ref as React.Ref<HTMLButtonElement>}
      type={(rest as ButtonAsButton).type || 'button'}
      className={classes}
      disabled={isDisabled}
      aria-busy={loading}
      {...(rest as ButtonHTMLAttributes<HTMLButtonElement>)}
    >
      {content}
    </button>
  );
});

Button.displayName = 'Button';

// ============================================================================
// Icon Button Component
// ============================================================================

interface IconButtonProps extends Omit<ButtonAsButton, 'leftIcon' | 'rightIcon' | 'children'> {
  /** The icon to render */
  icon: React.ReactNode;
  /** Accessible label for the button */
  'aria-label': string;
}

/**
 * Icon-only button with required accessibility label
 *
 * @example
 * <IconButton icon={<X />} aria-label="Close dialog" onClick={onClose} />
 */
export const IconButton = forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ icon, size = 'md', className = '', ...props }, ref) => {
    const sizeClasses: Record<ButtonSize, string> = {
      xs: 'w-7 h-7',
      sm: 'w-8 h-8',
      md: 'w-10 h-10',
      lg: 'w-12 h-12',
    };

    return (
      <Button
        ref={ref}
        size={size}
        className={`${sizeClasses[size]} !px-0 ${className}`}
        {...props}
      >
        <span className={iconSizes[size]}>{icon}</span>
      </Button>
    );
  }
);

IconButton.displayName = 'IconButton';

export default Button;
