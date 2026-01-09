#!/usr/bin/env python3
import os
import secrets

# Generate secure random keys
db_password = secrets.token_urlsafe(32)[:32]
directus_key = secrets.token_hex(32)
directus_secret = secrets.token_hex(32)
meilisearch_key = secrets.token_hex(32)

env_content = f"""# Database Configuration
DB_USER=directus
DB_PASSWORD={db_password}
DB_DATABASE=directus

# Directus Configuration
DIRECTUS_PORT=8055
DIRECTUS_KEY={directus_key}
DIRECTUS_SECRET={directus_secret}

# Admin User (CHANGE THESE!)
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=ChangeMe123!

# URLs
PUBLIC_URL=http://localhost:8055
FRONTEND_URL=http://localhost:3000

# Meilisearch Configuration
MEILISEARCH_PORT=7700
MEILISEARCH_MASTER_KEY={meilisearch_key}
MEILISEARCH_ENV=development

# Worker Service Token (create this in Directus after first start)
WORKER_TOKEN=to_be_created_later

# Next.js Configuration
NEXT_PUBLIC_DIRECTUS_URL=http://localhost:8055
NEXT_PUBLIC_MEILISEARCH_URL=http://localhost:7700
MEILISEARCH_SEARCH_KEY=to_be_created_later
"""

with open('.env', 'w') as f:
    f.write(env_content)

print("✅ .env file created with secure random keys")
print("\n⚠️  WICHTIG: Ändere ADMIN_EMAIL und ADMIN_PASSWORD vor dem ersten Start!")
