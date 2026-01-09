# 🧶 MaschenWerk

A self-hosted knitting project management system with integrated PDF pattern search and timeline visualization.

## ✨ Features

- **Project Management**: Create, organize, and showcase your knitting projects with images and detailed descriptions
- **Pattern Library**: Upload and manage PDF knitting patterns with full-text search capabilities
- **Smart Search**: Meilisearch-powered full-text search across all PDF patterns
- **Timeline View**: Visualize your knitting journey chronologically
- **Admin Dashboard**: Secure admin interface for content management
  - Upload new projects and patterns
  - Publish/unpublish projects (draft mode)
  - Delete projects and patterns
- **Dark Mode**: Fully responsive design with beautiful dark mode support
- **Authentication**: Secure login system with role-based access control and automatic token refresh

## 🏗️ Tech Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS v4** - Modern utility-first styling with custom dark mode
- **NextAuth.js v5** - Authentication with JWT and automatic token refresh
- **date-fns** - Date formatting and manipulation

### Backend
- **Directus** - Headless CMS for content management
- **PostgreSQL** - Relational database
- **Meilisearch** - Fast and relevant full-text search engine
- **Docker Compose** - Container orchestration for all services

### Worker Services
- **PDF Indexer** - Python worker that automatically indexes uploaded PDF patterns for searchability

## 📁 Project Structure

```
myKnittingProjects/
├── frontend/                    # Next.js application
│   ├── app/                    # App Router pages and API routes
│   │   ├── (auth)/            # Authentication pages
│   │   ├── admin/             # Admin-only pages (upload forms)
│   │   ├── api/               # API routes (delete, publish)
│   │   ├── projects/          # Project pages
│   │   ├── patterns/          # Pattern pages
│   │   └── timeline/          # Timeline view
│   ├── components/            # Reusable React components
│   ├── lib/                   # Utilities and Directus client
│   ├── auth.ts                # NextAuth.js configuration
│   └── middleware.ts          # Route protection middleware
├── pdf_worker/                # Python PDF indexer service
│   ├── worker.py              # Main worker script
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Worker container image
├── docker-compose.yml         # Docker services configuration
├── .env                       # Environment variables (not in git)
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Node.js 18+ (for frontend development)
- Python 3.9+ (for worker development, optional)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd myKnittingProjects
   ```

2. **Set up environment variables**
   ```bash
   # Generate secure .env file
   python3 generate-env.py
   
   # IMPORTANT: Edit .env and change:
   # - ADMIN_EMAIL
   # - ADMIN_PASSWORD
   # - NEXTAUTH_SECRET
   ```

3. **Start Docker services**
   ```bash
   # Start all backend services
   docker compose up -d
   
   # This starts:
   # - Directus CMS (http://localhost:8055)
   # - PostgreSQL database
   # - Meilisearch (http://localhost:7700)
   # - PDF indexer worker
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

5. **Start the development server**
   ```bash
   npm run dev
   ```
   
   Frontend available at **http://localhost:3000**

### First-Time Setup

1. **Access Directus Admin** at http://localhost:8055
   - Login with ADMIN_EMAIL and ADMIN_PASSWORD from `.env`
   - The database schema is automatically set up

2. **Login to Frontend** at http://localhost:3000/login
   - Use the same Directus credentials
   - Administrator role is required for admin features

3. **Start Creating!**
   - Use Admin dropdown → "New Project" to upload projects
   - Use Admin dropdown → "New Pattern" to upload PDF patterns
   - PDFs are automatically indexed within ~60 seconds

## 🎯 Usage Guide

### For Administrators

**Upload Projects:**
1. Click Admin dropdown in navigation
2. Select "New Project"
3. Fill in title, description, upload hero image
4. Choose "Draft" or "Public" status
5. Click "Create Project"

**Upload Patterns:**
1. Admin dropdown → "New Pattern"
2. Upload PDF file
3. Set visibility (Private or Friends & Family)
4. Add optional notes
5. Pattern is auto-indexed for search

**Manage Content:**
- View draft projects (yellow "Draft" badge)
- Publish drafts using green "Publish" button on detail pages
- Delete projects/patterns using red "Delete" button

### For Users

- **Browse Projects**: All published projects on `/projects`
- **Search Patterns**: Use search bar for full-text PDF search
- **Timeline**: View chronological project timeline
- **Dark Mode**: Toggle in navigation (persists across sessions)

## 🔐 Authentication & Security

- **JWT Authentication**: Secure token-based auth with NextAuth.js
- **Automatic Token Refresh**: Expired tokens are refreshed automatically
- **Role-Based Access**: Administrator role required for admin features
- **Protected Routes**: Middleware guards all `/admin/*` routes
- **Session Management**: Expired sessions redirect to login page
- **Secure Defaults**: All passwords hashed, secrets in environment variables

## 🐛 Troubleshooting

### Images Not Loading
**Problem**: Project images show broken links  
**Solution**: 
- Ensure Directus is running on `localhost:8055`
- Check `next.config.ts` has `unoptimized: true` for development
- Verify image files exist in Directus: http://localhost:8055/admin/files

### PDF Search Not Working
**Problem**: Search doesn't find PDF content  
**Solution**:
- Check worker is running: `docker compose logs pdf_worker`
- Verify Meilisearch: `curl http://localhost:7700/health`
- Wait ~60 seconds after PDF upload for indexing
- Check Meilisearch index: `curl http://localhost:7700/indexes`

### Token Expired / Login Issues
**Problem**: "Token expired" errors or constant redirects to login  
**Solution**:
- Clear browser cookies and localStorage
- Log in again with Directus credentials
- Check `.env` has correct `NEXTAUTH_SECRET`
- Restart frontend: `npm run dev`

### 404 on Draft Projects
**Problem**: Can't access draft projects as admin  
**Solution**:
- Ensure you're logged in with Administrator role
- Check session in browser dev tools (Application → Cookies)
- Verify Directus user has "Administrator" role (not just UUID)

### Port Already in Use
**Problem**: `Port 3000 already in use`  
**Solution**:
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
# Or kill all Next.js processes
pkill -f "next dev"
```

## 🔧 Useful Commands

### Docker Services

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f directus
docker compose logs -f meilisearch
docker compose logs -f pdf_worker

# Stop all services
docker compose down

# Restart services (e.g., after .env changes)
docker compose restart

# Remove all containers and volumes (CAUTION: deletes data!)
docker compose down -v
```

### Development

```bash
# Frontend development
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint

# Database backups
docker compose exec postgres pg_dump -U directus directus > backups/backup_$(date +%Y%m%d_%H%M%S).sql

# Backup uploaded files
tar -czf backups/uploads_$(date +%Y%m%d_%H%M%S).tar.gz directus/uploads/
```

## ⚙️ Configuration

### Environment Variables

Key variables in `.env`:

```bash
# Directus
ADMIN_EMAIL=your@email.com
ADMIN_PASSWORD=your-secure-password
KEY=<random-32-char-string>
SECRET=<random-32-char-string>

# NextAuth.js
NEXTAUTH_SECRET=<random-secret>
NEXTAUTH_URL=http://localhost:3000

# Meilisearch
MEILISEARCH_API_KEY=<random-api-key>

# URLs
NEXT_PUBLIC_DIRECTUS_URL=http://localhost:8055
MEILISEARCH_HOST=http://meilisearch:7700
```

Generate secure secrets: `python3 generate-env.py`

## 🎨 Features in Detail

### Project Management
- Rich markdown descriptions with image support
- Hero images for visual appeal
- Draft/Public status control
- Chronological timeline view
- Admin-only draft visibility

### Pattern Library
- PDF upload with automatic indexing
- Visibility control (Private, Friends & Family)
- Full-text search across all PDF content
- Optional notes per pattern

### Search
- Instant search results
- Searches across all PDF content
- Highlight matching text
- Fast Meilisearch backend

### Authentication
- Secure JWT-based authentication
- Automatic token refresh
- Role-based access control
- Protected admin routes

## 📖 Project Status

**Completed Phases:**

- [x] **Phase 0-7**: Infrastructure setup (Docker, Postgres, Directus, Meilisearch)
- [x] **Phase 8**: UI/UX with Dark Mode
- [x] **Phase 9**: Admin upload functionality
- [x] **Phase 10**: Project management (publish, delete)
- [x] **Phase 11**: Authentication improvements with token refresh

**Current Features:**

✅ Full CRUD for projects and patterns  
✅ PDF full-text search  
✅ Timeline visualization  
✅ Dark mode support  
✅ Role-based admin interface  
✅ Automatic token refresh  
✅ Draft project management  

## 🔐 Security & Production

**Development Security:**
- `.env` contains sensitive data (in `.gitignore`)
- All passwords should be changed before production
- Default setup uses localhost only

**For Production Deployment:**
1. Set up HTTPS (e.g., with Caddy/Traefik + Let's Encrypt)
2. Change all passwords and secrets in `.env`
3. Update `NEXTAUTH_URL` to your domain
4. Configure `next.config.ts` image domains for production
5. Set up regular backups of database and uploads
6. Consider using managed PostgreSQL and Meilisearch services

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome via issues or pull requests!

## 📄 License

MIT License - Feel free to use this for your own knitting projects!

---

**Built with ❤️ for the knitting community. Happy knitting! 🧶**
