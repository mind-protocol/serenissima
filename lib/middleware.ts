import { NextRequest, NextResponse } from 'next/server';
import { getAuthContext, checkRateLimit, getClientIP, hasPermission, canAccessCitizenData, canAccessFinancialData } from './auth';

/**
 * Authentication middleware
 */
export function withAuth(handler: (request: NextRequest, context: any) => Promise<NextResponse>) {
  return async (request: NextRequest, context: any = {}) => {
    const authContext = getAuthContext(request);
    
    if (!authContext.isAuthenticated) {
      return NextResponse.json(
        { error: 'Authentication required', code: 'AUTH_REQUIRED' },
        { status: 401 }
      );
    }
    
    // Add auth context to request context
    context.auth = authContext;
    
    return handler(request, context);
  };
}

/**
 * Permission-based authorization middleware
 */
export function withPermission(permission: string) {
  return function(handler: (request: NextRequest, context: any) => Promise<NextResponse>) {
    return withAuth(async (request: NextRequest, context: any) => {
      const { user } = context.auth;
      
      if (!hasPermission(user, permission)) {
        return NextResponse.json(
          { error: 'Insufficient permissions', code: 'INSUFFICIENT_PERMISSIONS', required: permission },
          { status: 403 }
        );
      }
      
      return handler(request, context);
    });
  };
}

/**
 * Rate limiting middleware
 */
export function withRateLimit(maxRequests: number = 100, windowMs: number = 60000) {
  return function(handler: (request: NextRequest, context: any) => Promise<NextResponse>) {
    return async (request: NextRequest, context: any = {}) => {
      const clientIP = getClientIP(request);
      const identifier = `${clientIP}:${request.nextUrl.pathname}`;
      
      if (!checkRateLimit(identifier, maxRequests, windowMs)) {
        return NextResponse.json(
          { error: 'Rate limit exceeded', code: 'RATE_LIMIT_EXCEEDED' },
          { status: 429 }
        );
      }
      
      return handler(request, context);
    };
  };
}

/**
 * Citizen data access middleware
 */
export function withCitizenAccess(handler: (request: NextRequest, context: any) => Promise<NextResponse>) {
  return withAuth(async (request: NextRequest, context: any) => {
    const { user } = context.auth;
    const url = new URL(request.url);
    const citizenId = url.searchParams.get('citizenId');
    
    if (!canAccessCitizenData(user, citizenId || undefined)) {
      return NextResponse.json(
        { error: 'Cannot access citizen data', code: 'CITIZEN_ACCESS_DENIED' },
        { status: 403 }
      );
    }
    
    return handler(request, context);
  });
}

/**
 * Financial data access middleware
 */
export function withFinancialAccess(handler: (request: NextRequest, context: any) => Promise<NextResponse>) {
  return withAuth(async (request: NextRequest, context: any) => {
    const { user } = context.auth;
    
    if (!canAccessFinancialData(user)) {
      return NextResponse.json(
        { error: 'Cannot access financial data', code: 'FINANCIAL_ACCESS_DENIED' },
        { status: 403 }
      );
    }
    
    return handler(request, context);
  });
}

/**
 * Error handling middleware
 */
export function withErrorHandling(handler: (request: NextRequest, context: any) => Promise<NextResponse>) {
  return async (request: NextRequest, context: any = {}) => {
    try {
      return await handler(request, context);
    } catch (error) {
      console.error('API Error:', error);
      
      // Don't expose internal errors in production
      const isDev = process.env.NODE_ENV === 'development';
      
      return NextResponse.json(
        {
          error: 'Internal server error',
          code: 'INTERNAL_ERROR',
          ...(isDev && { details: error instanceof Error ? error.message : String(error) })
        },
        { status: 500 }
      );
    }
  };
}

/**
 * Security headers middleware
 */
export function withSecurityHeaders(handler: (request: NextRequest, context: any) => Promise<NextResponse>) {
  return async (request: NextRequest, context: any = {}) => {
    const response = await handler(request, context);
    
    // Add security headers
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('X-Frame-Options', 'DENY');
    response.headers.set('X-XSS-Protection', '1; mode=block');
    response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    
    return response;
  };
}

/**
 * Logging middleware
 */
export function withLogging(handler: (request: NextRequest, context: any) => Promise<NextResponse>) {
  return async (request: NextRequest, context: any = {}) => {
    const startTime = Date.now();
    const clientIP = getClientIP(request);
    
    console.log(`🔍 ${request.method} ${request.nextUrl.pathname} - ${clientIP}`);
    
    const response = await handler(request, context);
    
    const duration = Date.now() - startTime;
    console.log(`✅ ${request.method} ${request.nextUrl.pathname} - ${response.status} (${duration}ms)`);
    
    return response;
  };
}

/**
 * Compose multiple middleware functions
 */
export function compose(...middlewares: Array<(handler: any) => any>) {
  return (handler: any) => {
    return middlewares.reduceRight((acc, middleware) => middleware(acc), handler);
  };
}

/**
 * Standard API middleware stack
 */
export const withStandardMiddleware = compose(
  withErrorHandling,
  withSecurityHeaders,
  withLogging,
  withRateLimit(100, 60000) // 100 requests per minute
);

/**
 * Protected API middleware stack (with auth)
 */
export const withProtectedMiddleware = compose(
  withErrorHandling,
  withSecurityHeaders,
  withLogging,
  withRateLimit(100, 60000),
  withAuth
);

/**
 * Financial API middleware stack
 */
export const withFinancialMiddleware = compose(
  withErrorHandling,
  withSecurityHeaders,
  withLogging,
  withRateLimit(50, 60000), // Stricter rate limit for financial APIs
  withFinancialAccess
);