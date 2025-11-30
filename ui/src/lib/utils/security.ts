/**
 * Security Utilities for Verridian AI UI
 *
 * Provides sanitization and validation functions to prevent XSS,
 * injection attacks, and other security vulnerabilities.
 */

import DOMPurify from 'dompurify';

/**
 * Allowed HTML tags for sanitized content
 * These are safe tags that don't execute scripts or create security risks
 */
const ALLOWED_TAGS = [
  // Text formatting
  'p', 'br', 'hr',
  'b', 'i', 'u', 's', 'em', 'strong', 'mark', 'small', 'sub', 'sup',
  'span', 'div',
  // Headings
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
  // Lists
  'ul', 'ol', 'li', 'dl', 'dt', 'dd',
  // Links & Media (safe subset)
  'a', 'img',
  // Tables
  'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'caption',
  // Block elements
  'blockquote', 'pre', 'code',
  // Semantic elements
  'article', 'section', 'header', 'footer', 'nav', 'aside',
  'figure', 'figcaption', 'time', 'address',
];

/**
 * Allowed HTML attributes
 * Only safe attributes that don't enable script execution
 */
const ALLOWED_ATTR = [
  // Global attributes
  'class', 'id', 'style', 'title', 'lang', 'dir',
  // Link attributes (href validated separately)
  'href', 'target', 'rel',
  // Image attributes
  'src', 'alt', 'width', 'height', 'loading',
  // Table attributes
  'colspan', 'rowspan', 'scope',
  // Data attributes (for styling)
  'data-*',
];

/**
 * Configure DOMPurify with secure defaults
 */
const createSanitizer = () => {
  // Only run in browser environment
  if (typeof window === 'undefined') {
    return {
      sanitize: (html: string) => html, // SSR fallback - content will be sanitized on client
    };
  }

  const config: DOMPurify.Config = {
    ALLOWED_TAGS,
    ALLOWED_ATTR,
    // Prevent all URL schemes except safe ones
    ALLOWED_URI_REGEXP: /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp|xxx):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i,
    // Remove scripts and other dangerous elements
    FORBID_TAGS: ['script', 'object', 'embed', 'link', 'style', 'iframe', 'frame', 'frameset'],
    FORBID_ATTR: ['onerror', 'onclick', 'onload', 'onmouseover', 'onfocus', 'onblur', 'onchange', 'onsubmit'],
    // Keep safe content structure
    KEEP_CONTENT: true,
    // Don't allow data: URLs in src attributes (potential XSS vector)
    ADD_URI_SAFE_ATTR: ['href'],
  };

  return {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    sanitize: (dirty: string, extraConfig?: any): string => {
      // Use extraConfig if provided, otherwise use base config
      const finalConfig = extraConfig || config;
      return DOMPurify.sanitize(dirty, finalConfig) as unknown as string;
    },
  };
};

export const sanitizer = createSanitizer();

/**
 * Sanitize HTML content for safe rendering
 * Use this with dangerouslySetInnerHTML
 *
 * @param html - Potentially unsafe HTML string
 * @returns Sanitized HTML string safe for rendering
 *
 * @example
 * <div dangerouslySetInnerHTML={{ __html: sanitizeHtml(userContent) }} />
 */
export function sanitizeHtml(html: string): string {
  if (!html) return '';
  return sanitizer.sanitize(html);
}

/**
 * Sanitize HTML with stricter rules for user-generated content
 * Only allows basic text formatting
 *
 * @param html - User-generated HTML content
 * @returns Heavily sanitized HTML
 */
export function sanitizeUserContent(html: string): string {
  if (!html) return '';
  return sanitizer.sanitize(html, {
    ALLOWED_TAGS: ['p', 'br', 'b', 'i', 'u', 'em', 'strong', 'a', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: ['href', 'target', 'rel'],
  });
}

/**
 * Validate URL for safety
 * Prevents javascript:, data:, and other dangerous URL schemes
 *
 * @param url - URL string to validate
 * @returns true if URL is safe, false otherwise
 */
export function isValidUrl(url: string): boolean {
  if (!url) return false;

  try {
    const parsed = new URL(url);
    // Only allow http and https protocols
    return ['http:', 'https:'].includes(parsed.protocol);
  } catch {
    // If URL parsing fails, check for relative URLs
    return url.startsWith('/') || url.startsWith('./') || url.startsWith('../');
  }
}

/**
 * Sanitize URL for safe use in href attributes
 * Returns empty string for unsafe URLs
 *
 * @param url - URL to sanitize
 * @returns Safe URL or empty string
 */
export function sanitizeUrl(url: string): string {
  if (!url) return '';

  // Remove any whitespace and control characters
  const cleaned = url.trim().replace(/[\x00-\x1f]/g, '');

  // Block dangerous protocols
  const dangerousProtocols = ['javascript:', 'vbscript:', 'data:', 'blob:'];
  const lowerUrl = cleaned.toLowerCase();

  for (const protocol of dangerousProtocols) {
    if (lowerUrl.startsWith(protocol)) {
      return '';
    }
  }

  return cleaned;
}

/**
 * Escape HTML entities to prevent injection
 * Use for text content that should not contain any HTML
 *
 * @param text - Text to escape
 * @returns Escaped text safe for HTML display
 */
export function escapeHtml(text: string): string {
  if (!text) return '';

  const htmlEntities: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '/': '&#x2F;',
    '`': '&#x60;',
    '=': '&#x3D;',
  };

  return text.replace(/[&<>"'`=/]/g, (char) => htmlEntities[char] || char);
}

/**
 * Validate and sanitize form input
 * Removes potentially dangerous characters
 *
 * @param input - User input string
 * @param options - Validation options
 * @returns Sanitized input
 */
export function sanitizeInput(
  input: string,
  options: {
    maxLength?: number;
    allowNewlines?: boolean;
    allowHtml?: boolean;
  } = {}
): string {
  if (!input) return '';

  let result = input;

  // Remove null bytes and other control characters
  result = result.replace(/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/g, '');

  // Optionally remove newlines
  if (!options.allowNewlines) {
    result = result.replace(/[\r\n]/g, ' ');
  }

  // Escape HTML if not allowed
  if (!options.allowHtml) {
    result = escapeHtml(result);
  }

  // Truncate if max length specified
  if (options.maxLength && result.length > options.maxLength) {
    result = result.slice(0, options.maxLength);
  }

  return result.trim();
}

/**
 * Check if a string contains potentially dangerous content
 *
 * @param content - Content to check
 * @returns true if content appears safe, false if suspicious
 */
export function isContentSafe(content: string): boolean {
  if (!content) return true;

  const suspiciousPatterns = [
    /<script\b/i,
    /javascript:/i,
    /on\w+\s*=/i, // onclick, onerror, etc.
    /data:\s*text\/html/i,
    /<iframe\b/i,
    /<object\b/i,
    /<embed\b/i,
    /expression\s*\(/i, // CSS expression
    /url\s*\(\s*["']?\s*javascript/i,
  ];

  return !suspiciousPatterns.some(pattern => pattern.test(content));
}

export default {
  sanitizeHtml,
  sanitizeUserContent,
  sanitizeUrl,
  escapeHtml,
  sanitizeInput,
  isValidUrl,
  isContentSafe,
};
