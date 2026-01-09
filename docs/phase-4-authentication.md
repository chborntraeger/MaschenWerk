# Phase 4: Authentication & Protected Areas

## ✅ Completed

Phase 4 has been successfully completed! Your knitting projects app now has full authentication and protected pattern access.

## 🎉 What's New

### 1. Authentication System
- **NextAuth.js v5** integration with Directus backend
- JWT-based session management
- Secure credential-based authentication
- Automatic token refresh handling

### 2. Protected Patterns Section
- `/patterns` - List of all patterns (authenticated users only)
- `/patterns/[slug]` - Individual pattern detail pages
- Visibility badges (Friends & Family / Private)
- Protected PDF downloads

### 3. PDF Proxy API
- Server-side PDF fetching from Directus
- Token-based authorization
- Secure file delivery without exposing Directus URLs
- Automatic filename handling

### 4. User Interface Updates
- Dynamic header with login/logout
- User name display when authenticated
- Conditional "Patterns" navigation link
- Redirect to login for protected pages

## 📁 New Files Created

```
frontend/
├── auth.ts                                    # NextAuth configuration
├── types/next-auth.d.ts                       # TypeScript type definitions
├── app/
│   ├── api/
│   │   ├── auth/[...nextauth]/route.ts       # NextAuth API route
│   │   └── download-pattern/[slug]/route.ts  # PDF proxy API
│   ├── patterns/
│   │   ├── page.tsx                          # Patterns list (protected)
│   │   └── [slug]/page.tsx                   # Pattern detail (protected)
│   └── login/page.tsx                        # Updated with NextAuth
└── .env.local                                 # Added AUTH_SECRET
```

## 🔧 Modified Files

- **lib/directus.ts**: Added `createAuthenticatedClient()` helper
- **components/Header.tsx**: Now async server component with auth state
- **app/login/page.tsx**: Full NextAuth integration with form handling

## 🔐 Authentication Flow

1. **Login Process**:
   - User enters credentials on `/login`
   - NextAuth validates with Directus `/auth/login` endpoint
   - On success, creates JWT session with access token
   - Redirects to callback URL or homepage

2. **Protected Routes**:
   - `/patterns/*` routes check for valid session
   - Unauthenticated users redirected to login
   - Session token used for Directus API requests

3. **PDF Downloads**:
   - Click "Download PDF" on pattern detail page
   - API route verifies session
   - Fetches PDF from Directus with user's token
   - Streams file to browser with proper headers

## 🧪 Testing Authentication

### Test Account
```
Email: test@familie.de
Password: TestPass123!
```

### Test Flow
1. Start dev server: `npm run dev`
2. Open http://localhost:3000
3. Click "Login" in header
4. Use test credentials above
5. Access http://localhost:3000/patterns
6. View pattern details and download PDFs

### Expected Behavior
- ✅ Unauthenticated: Only see Projects, Timeline, Login
- ✅ Authenticated: See Projects, Timeline, Patterns, User name, Logout
- ✅ Logout: Redirects to homepage, session cleared
- ✅ Protected routes: Redirect to login with callback URL

## 📝 Environment Variables

Add to `frontend/.env.local`:
```env
# NextAuth Configuration
AUTH_SECRET=your-super-secret-auth-secret-change-this-in-production
NEXTAUTH_URL=http://localhost:3000
```

⚠️ **Important**: Generate a new `AUTH_SECRET` for production:
```bash
openssl rand -base64 32
```

## 🎨 Features by Role

### Public (No Login)
- ✅ View public projects
- ✅ Browse timeline
- ✅ Read project details

### Friends & Family (test@familie.de)
- ✅ All public features
- ✅ Access pattern library
- ✅ Download PDF patterns
- ✅ View friends_family visibility patterns

### Admin (admin@example.com / ChangeMe123!)
- ✅ All Friends & Family features
- ✅ View all patterns (including private)
- ✅ Access Directus admin panel

## 🔒 Security Features

1. **Server-Side Authentication**
   - Session validation on server components
   - No client-side token exposure
   - Secure HTTP-only cookies

2. **Protected API Routes**
   - Token verification on every request
   - Direct Directus integration
   - No public asset URLs

3. **Type-Safe Sessions**
   - TypeScript definitions for user data
   - Autocomplete for session properties
   - Compile-time type checking

## 🚀 Next Steps - Phase 5

Ready to implement **Search with Meilisearch**:

1. Create `/search` page with search UI
2. Implement autocomplete component
3. Add filters for tags and years
4. Connect to Meilisearch index (port 7700)
5. Display search results with highlighting

Would you like to proceed with Phase 5? 🔍

## 📚 Technical Details

### NextAuth Configuration
- **Strategy**: JWT-based sessions
- **Provider**: Custom Directus credentials provider
- **Callbacks**: JWT and session callbacks for token management
- **Pages**: Custom login page at `/login`

### Directus Integration
- **Login Endpoint**: `/auth/login` for credentials validation
- **User Endpoint**: `/users/me` for user details
- **Assets Endpoint**: `/assets/{id}` for file access
- **Authorization**: Bearer token in headers

### Type Definitions
```typescript
interface Session {
  user: {
    id: string;
    email: string;
    name: string;
    accessToken: string;
    role: string;
  };
}
```

## 🐛 Troubleshooting

### "Unauthorized" when accessing patterns
- Make sure you're logged in
- Check that test user exists in Directus
- Verify Directus is running (http://localhost:8055)

### Login fails with "Invalid credentials"
- Confirm test user password: TestPass123!
- Check Directus user in admin panel
- Review browser console for errors

### PDF download fails
- Ensure pattern has PDF file uploaded
- Check Directus permissions for pattern visibility
- Verify API route logs in terminal

### Session not persisting
- Check AUTH_SECRET is set in .env.local
- Clear browser cookies and try again
- Restart Next.js dev server

## 📖 Code Examples

### Check Authentication in Server Component
```typescript
import { auth } from '@/auth';

export default async function ProtectedPage() {
  const session = await auth();
  
  if (!session?.user) {
    redirect('/login');
  }
  
  return <div>Welcome {session.user.name}!</div>;
}
```

### Authenticated API Request
```typescript
import { createAuthenticatedClient } from '@/lib/directus';

const { client, token } = createAuthenticatedClient(session.user.accessToken);

const data = await client.request(
  readItems('patterns', { limit: 10 }),
  {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
);
```

---

**Phase 4 Status**: ✅ Complete  
**Next Phase**: Phase 5 - Meilisearch Integration
