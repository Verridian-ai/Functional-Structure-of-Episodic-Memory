'use client';

import React from 'react';

interface SkipLink {
  id: string;
  label: string;
}

const defaultLinks: SkipLink[] = [
  { id: 'main-content', label: 'Skip to main content' },
  { id: 'chat-input', label: 'Skip to chat input' },
];

interface SkipLinksProps {
  links?: SkipLink[];
}

/**
 * Skip Links for keyboard navigation accessibility
 *
 * Provides keyboard users a way to skip repetitive navigation
 * and jump directly to main content areas.
 *
 * Features:
 * - Hidden until focused (Tab key)
 * - High contrast for visibility
 * - Smooth scroll to target
 * - WCAG 2.1 AA compliant
 *
 * @example
 * // In layout
 * <SkipLinks />
 * <header>...</header>
 * <main id="main-content">...</main>
 */
export function SkipLinks({ links = defaultLinks }: SkipLinksProps) {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    e.preventDefault();
    const element = document.getElementById(id);

    if (element) {
      // Move focus to the element
      element.setAttribute('tabindex', '-1');
      element.focus({ preventScroll: true });

      // Smooth scroll to element
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });

      // Remove tabindex after blur to not affect tab order
      element.addEventListener(
        'blur',
        () => {
          element.removeAttribute('tabindex');
        },
        { once: true }
      );
    }
  };

  return (
    <nav
      aria-label="Skip links"
      className="skip-links fixed top-0 left-0 z-[100] p-2"
    >
      <ul className="flex flex-col gap-1">
        {links.map((link) => (
          <li key={link.id}>
            <a
              href={`#${link.id}`}
              onClick={(e) => handleClick(e, link.id)}
              className="
                sr-only focus:not-sr-only
                focus:absolute focus:z-[100]
                focus:px-4 focus:py-3
                focus:bg-cyan-600 focus:text-white
                focus:font-semibold focus:text-sm
                focus:rounded-lg focus:shadow-lg
                focus:outline-none focus:ring-2 focus:ring-white
                transition-all
              "
            >
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default SkipLinks;
