'use client';

import React from 'react';
import { sanitizeHtml, sanitizeUserContent } from '@/lib/utils/security';

/**
 * SafeHtml - Securely renders HTML content with XSS protection
 *
 * This component uses DOMPurify to sanitize HTML before rendering,
 * preventing cross-site scripting (XSS) attacks.
 *
 * @example
 * // Basic usage
 * <SafeHtml content={htmlString} />
 *
 * // With custom class
 * <SafeHtml content={htmlString} className="prose prose-invert" />
 *
 * // Strict mode for user content
 * <SafeHtml content={userInput} strict />
 */

interface SafeHtmlProps {
  /** HTML content to render */
  content: string;
  /** Additional CSS classes */
  className?: string;
  /** Use strict sanitization (fewer allowed tags) */
  strict?: boolean;
  /** HTML element to use as wrapper */
  as?: 'div' | 'span' | 'p' | 'article' | 'section';
  /** Additional inline styles */
  style?: React.CSSProperties;
  /** Test ID for testing */
  'data-testid'?: string;
}

export const SafeHtml = React.memo(function SafeHtml({
  content,
  className = '',
  strict = false,
  as = 'div',
  style,
  'data-testid': testId,
}: SafeHtmlProps) {
  // Sanitize the HTML content
  const sanitizedHtml = React.useMemo(() => {
    if (!content) return '';
    return strict ? sanitizeUserContent(content) : sanitizeHtml(content);
  }, [content, strict]);

  // Don't render anything if content is empty
  if (!sanitizedHtml) {
    return null;
  }

  const props = {
    className,
    style,
    'data-testid': testId,
    dangerouslySetInnerHTML: { __html: sanitizedHtml },
  };

  switch (as) {
    case 'span':
      return <span {...props} />;
    case 'p':
      return <p {...props} />;
    case 'article':
      return <article {...props} />;
    case 'section':
      return <section {...props} />;
    default:
      return <div {...props} />;
  }
});

/**
 * SafeHtmlProse - SafeHtml with prose styling applied
 *
 * Convenience component for rendering HTML content with
 * Tailwind prose classes for good typography.
 */
export const SafeHtmlProse = React.memo(function SafeHtmlProse({
  content,
  className = '',
  strict = false,
  dark = true,
  style,
  'data-testid': testId,
}: SafeHtmlProps & { dark?: boolean }) {
  const proseClasses = dark
    ? 'prose prose-invert prose-sm max-w-none'
    : 'prose prose-sm max-w-none';

  return (
    <SafeHtml
      content={content}
      className={`${proseClasses} ${className}`}
      strict={strict}
      style={style}
      data-testid={testId}
    />
  );
});

export default SafeHtml;
