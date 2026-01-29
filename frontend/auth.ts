import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

async function refreshAccessToken(token: any) {
  try {
    const directusUrl = process.env.NEXT_PUBLIC_DIRECTUS_URL || 'http://localhost:8055';
    
    if (!token.refreshToken) {
      return {
        ...token,
        error: 'RefreshAccessTokenError',
      };
    }
    
    const response = await fetch(`${directusUrl}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        refresh_token: token.refreshToken,
      }),
    });

    if (!response.ok) {
      // Token refresh failed - user needs to login again
      return {
        ...token,
        error: 'RefreshAccessTokenError',
      };
    }

    const data = await response.json();

    return {
      ...token,
      accessToken: data.data.access_token,
      refreshToken: data.data.refresh_token ?? token.refreshToken,
      accessTokenExpires: Date.now() + 7 * 24 * 60 * 60 * 1000, // 7 days
      error: undefined,
    };
  } catch (error) {
    return {
      ...token,
      error: 'RefreshAccessTokenError',
    };
  }
}

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Directus',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        try {
          const directusUrl = process.env.NEXT_PUBLIC_DIRECTUS_URL || 'http://localhost:8055';
          
          // Login to Directus
          const response = await fetch(`${directusUrl}/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          });

          if (!response.ok) {
            return null;
          }

          const data = await response.json();

          if (!data.data?.access_token) {
            return null;
          }

          // Fetch user details
          const userResponse = await fetch(`${directusUrl}/users/me?fields=*,role.name`, {
            headers: {
              Authorization: `Bearer ${data.data.access_token}`,
            },
          });

          if (!userResponse.ok) {
            return null;
          }

          const userData = await userResponse.json();

          return {
            id: userData.data.id,
            email: userData.data.email,
            name: userData.data.first_name || userData.data.email,
            accessToken: data.data.access_token,
            refreshToken: data.data.refresh_token,
            accessTokenExpires: Date.now() + 7 * 24 * 60 * 60 * 1000, // 7 days - we'll handle expiry via 401 responses
            role: userData.data.role?.name || userData.data.role,
          };
        } catch (error) {
          console.error('Auth error:', error);
          return null;
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user, account }) {
      // Initial sign in
      if (account && user) {
        return {
          ...token,
          accessToken: user.accessToken,
          refreshToken: user.refreshToken,
          accessTokenExpires: user.accessTokenExpires,
          role: user.role,
        };
      }

      // Return previous token if the access token has not expired yet
      if (Date.now() < (token.accessTokenExpires as number)) {
        return token;
      }

      // Access token has expired, try to refresh it
      return refreshAccessToken(token);
    },
    async session({ session, token }) {
      session.user.accessToken = token.accessToken as string;
      session.user.role = token.role as string;
      return session;
    },
  },
  pages: {
    signIn: '/login',
  },
  session: {
    strategy: 'jwt',
  },
});
