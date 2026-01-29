import { auth } from '@/auth';
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

export async function middleware(request: NextRequest) {
  // Check if this is an admin route
  const isAdminRoute = request.nextUrl.pathname.startsWith('/admin');
  
  if (isAdminRoute) {
    const session = await auth();
    
    // If no session at all, redirect to login
    if (!session?.user) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
    
    // If not an admin, redirect to home
    if (session.user.role !== 'Administrator') {
      return NextResponse.redirect(new URL('/', request.url));
    }
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*'],
};
