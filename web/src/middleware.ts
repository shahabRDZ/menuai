import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const SESSION_COOKIE = "menuai_session";

export function middleware(request: NextRequest) {
  const token = request.cookies.get(SESSION_COOKIE);
  if (!token) {
    const url = new URL("/login", request.url);
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/app/:path*"],
};
