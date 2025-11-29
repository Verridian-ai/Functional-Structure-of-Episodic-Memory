'use client';

import React from 'react';

interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'circular' | 'rectangular' | 'rounded';
  width?: string | number;
  height?: string | number;
  animation?: 'pulse' | 'wave' | 'none';
}

/**
 * Skeleton loading placeholder component
 *
 * @example
 * <Skeleton variant="text" width="80%" />
 * <Skeleton variant="circular" width={40} height={40} />
 * <Skeleton variant="rounded" height={100} />
 */
export function Skeleton({
  className = '',
  variant = 'text',
  width,
  height,
  animation = 'pulse',
}: SkeletonProps) {
  const baseClasses = 'bg-zinc-800';

  const variantClasses = {
    text: 'rounded',
    circular: 'rounded-full',
    rectangular: 'rounded-none',
    rounded: 'rounded-xl',
  };

  const animationClasses = {
    pulse: 'animate-pulse',
    wave: 'skeleton-wave',
    none: '',
  };

  const style: React.CSSProperties = {
    width: typeof width === 'number' ? `${width}px` : width,
    height: typeof height === 'number' ? `${height}px` : height,
  };

  // Default heights for text variant
  if (variant === 'text' && !height) {
    style.height = '1em';
  }

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${animationClasses[animation]} ${className}`}
      style={style}
      aria-hidden="true"
    />
  );
}

/**
 * Message skeleton for chat loading states
 */
export function MessageSkeleton({ isUser = false }: { isUser?: boolean }) {
  return (
    <div className={`flex gap-4 p-6 ${isUser ? '' : 'bg-zinc-900/40'}`}>
      {/* Avatar */}
      <Skeleton variant="rounded" width={36} height={36} />

      {/* Content */}
      <div className="flex-1 space-y-3">
        {/* Header */}
        <div className="flex items-center gap-2">
          <Skeleton variant="text" width={80} />
          <Skeleton variant="text" width={40} />
        </div>

        {/* Message lines */}
        <div className="space-y-2">
          <Skeleton variant="text" width="90%" />
          <Skeleton variant="text" width="75%" />
          <Skeleton variant="text" width="60%" />
        </div>
      </div>
    </div>
  );
}

/**
 * Conversation item skeleton for sidebar
 */
export function ConversationSkeleton() {
  return (
    <div className="flex items-center gap-3.5 p-3.5 rounded-2xl">
      <Skeleton variant="rounded" width={40} height={40} />
      <div className="flex-1 space-y-2">
        <Skeleton variant="text" width="70%" />
        <Skeleton variant="text" width="40%" height={12} />
      </div>
    </div>
  );
}

/**
 * Card skeleton for artifacts/documents
 */
export function CardSkeleton({ lines = 3 }: { lines?: number }) {
  return (
    <div className="p-4 bg-zinc-900/50 rounded-xl border border-white/5 space-y-3">
      <div className="flex items-center gap-3">
        <Skeleton variant="rounded" width={32} height={32} />
        <Skeleton variant="text" width="60%" />
      </div>
      <div className="space-y-2">
        {Array.from({ length: lines }).map((_, i) => (
          <Skeleton key={i} variant="text" width={`${90 - i * 10}%`} />
        ))}
      </div>
    </div>
  );
}

/**
 * Button skeleton
 */
export function ButtonSkeleton({ width = 100 }: { width?: number | string }) {
  return <Skeleton variant="rounded" width={width} height={40} />;
}

/**
 * Input skeleton
 */
export function InputSkeleton() {
  return <Skeleton variant="rounded" width="100%" height={48} />;
}

/**
 * Full page loading skeleton
 */
export function PageSkeleton() {
  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-white/5">
        <Skeleton variant="text" width={120} />
        <div className="flex gap-2">
          <Skeleton variant="circular" width={32} height={32} />
          <Skeleton variant="circular" width={32} height={32} />
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 p-4 space-y-4">
        <MessageSkeleton />
        <MessageSkeleton isUser />
        <MessageSkeleton />
      </div>

      {/* Input */}
      <div className="p-4">
        <InputSkeleton />
      </div>
    </div>
  );
}

export default Skeleton;
