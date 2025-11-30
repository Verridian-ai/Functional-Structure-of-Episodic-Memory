/**
 * Error Handling Utilities
 *
 * Centralized error handling for API calls, validation, and user-facing errors.
 */

// Error types for categorization
export type ErrorCategory =
  | 'network'
  | 'auth'
  | 'validation'
  | 'server'
  | 'client'
  | 'timeout'
  | 'unknown';

// Custom error class with additional metadata
export class AppError extends Error {
  public readonly category: ErrorCategory;
  public readonly statusCode?: number;
  public readonly originalError?: Error;
  public readonly retryable: boolean;
  public readonly userMessage: string;

  constructor(
    message: string,
    options: {
      category?: ErrorCategory;
      statusCode?: number;
      originalError?: Error;
      retryable?: boolean;
      userMessage?: string;
    } = {}
  ) {
    super(message);
    this.name = 'AppError';
    this.category = options.category ?? 'unknown';
    this.statusCode = options.statusCode;
    this.originalError = options.originalError;
    this.retryable = options.retryable ?? false;
    this.userMessage = options.userMessage ?? this.getDefaultUserMessage();
  }

  private getDefaultUserMessage(): string {
    switch (this.category) {
      case 'network':
        return 'Unable to connect. Please check your internet connection.';
      case 'auth':
        return 'Authentication failed. Please check your credentials.';
      case 'validation':
        return 'Invalid input. Please check your data and try again.';
      case 'server':
        return 'Server error. Please try again later.';
      case 'timeout':
        return 'Request timed out. Please try again.';
      case 'client':
        return 'Something went wrong. Please refresh and try again.';
      default:
        return 'An unexpected error occurred. Please try again.';
    }
  }
}

/**
 * Parse API error responses into AppError
 */
export function parseApiError(error: unknown): AppError {
  // Already an AppError
  if (error instanceof AppError) {
    return error;
  }

  // Fetch API errors
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return new AppError('Network request failed', {
      category: 'network',
      originalError: error as Error,
      retryable: true,
    });
  }

  // Response-like errors (from fetch)
  if (typeof error === 'object' && error !== null && 'status' in error) {
    const responseError = error as { status: number; statusText?: string; message?: string };
    const statusCode = responseError.status;

    if (statusCode === 401 || statusCode === 403) {
      return new AppError(responseError.message ?? 'Authentication failed', {
        category: 'auth',
        statusCode,
        userMessage: 'Your session has expired. Please sign in again.',
      });
    }

    if (statusCode === 404) {
      return new AppError('Resource not found', {
        category: 'client',
        statusCode,
        userMessage: 'The requested resource could not be found.',
      });
    }

    if (statusCode === 422 || statusCode === 400) {
      return new AppError(responseError.message ?? 'Validation failed', {
        category: 'validation',
        statusCode,
      });
    }

    if (statusCode === 429) {
      return new AppError('Rate limited', {
        category: 'server',
        statusCode,
        retryable: true,
        userMessage: 'Too many requests. Please wait a moment and try again.',
      });
    }

    if (statusCode >= 500) {
      return new AppError(responseError.message ?? 'Server error', {
        category: 'server',
        statusCode,
        retryable: true,
      });
    }
  }

  // Standard Error objects
  if (error instanceof Error) {
    // Timeout detection
    if (error.message.includes('timeout') || error.name === 'AbortError') {
      return new AppError('Request timed out', {
        category: 'timeout',
        originalError: error,
        retryable: true,
      });
    }

    return new AppError(error.message, {
      category: 'client',
      originalError: error,
    });
  }

  // Unknown error types
  return new AppError(String(error), {
    category: 'unknown',
  });
}

/**
 * Async function wrapper with error handling
 *
 * @example
 * const [data, error] = await tryCatch(() => fetchData());
 * if (error) {
 *   handleError(error);
 *   return;
 * }
 * // use data
 */
export async function tryCatch<T>(
  fn: () => Promise<T>
): Promise<[T, null] | [null, AppError]> {
  try {
    const result = await fn();
    return [result, null];
  } catch (error) {
    return [null, parseApiError(error)];
  }
}

/**
 * Synchronous function wrapper with error handling
 */
export function tryCatchSync<T>(fn: () => T): [T, null] | [null, AppError] {
  try {
    const result = fn();
    return [result, null];
  } catch (error) {
    return [null, parseApiError(error)];
  }
}

/**
 * Retry a function with exponential backoff
 *
 * @example
 * const result = await withRetry(() => fetchData(), { maxRetries: 3 });
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    initialDelay?: number;
    maxDelay?: number;
    shouldRetry?: (error: AppError, attempt: number) => boolean;
  } = {}
): Promise<T> {
  const {
    maxRetries = 3,
    initialDelay = 1000,
    maxDelay = 10000,
    shouldRetry = (error) => error.retryable,
  } = options;

  let lastError: AppError | null = null;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = parseApiError(error);

      if (attempt < maxRetries && shouldRetry(lastError, attempt)) {
        const delay = Math.min(initialDelay * Math.pow(2, attempt), maxDelay);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError ?? new AppError('Max retries exceeded');
}

/**
 * Log error with structured format
 */
export function logError(
  error: unknown,
  context?: Record<string, unknown>
): void {
  const appError = error instanceof AppError ? error : parseApiError(error);

  const logData = {
    timestamp: new Date().toISOString(),
    category: appError.category,
    message: appError.message,
    statusCode: appError.statusCode,
    retryable: appError.retryable,
    stack: appError.stack,
    originalError: appError.originalError?.message,
    ...context,
  };

  // In development, log to console
  if (process.env.NODE_ENV !== 'production') {
    console.error('Error:', logData);
  }

  // In production, you would send to a logging service
  // e.g., Sentry, LogRocket, etc.
}

/**
 * Format error for display to users
 */
export function formatErrorForDisplay(error: unknown): {
  title: string;
  message: string;
  canRetry: boolean;
} {
  const appError = error instanceof AppError ? error : parseApiError(error);

  const titleMap: Record<ErrorCategory, string> = {
    network: 'Connection Error',
    auth: 'Authentication Error',
    validation: 'Validation Error',
    server: 'Server Error',
    client: 'Application Error',
    timeout: 'Request Timeout',
    unknown: 'Error',
  };

  return {
    title: titleMap[appError.category],
    message: appError.userMessage,
    canRetry: appError.retryable,
  };
}

export default {
  AppError,
  parseApiError,
  tryCatch,
  tryCatchSync,
  withRetry,
  logError,
  formatErrorForDisplay,
};
