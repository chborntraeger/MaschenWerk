import 'next-auth';

declare module 'next-auth' {
  interface Session {
    user: {
      id: string;
      email: string;
      name: string;
      accessToken: string;
      role: string;
    };
  }

  interface User {
    id: string;
    email: string;
    name: string;
    accessToken: string;
    refreshToken: string;
    accessTokenExpires: number;
    role: string;
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    accessToken?: string;
    refreshToken?: string;
    accessTokenExpires?: number;
    role?: string;
  }
}
