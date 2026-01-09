import { authentication, createDirectus, rest } from '@directus/sdk';

// Directus Collections Type Definitions
export type Project = {
  id: string;
  status: 'draft' | 'public' | 'private';
  title: string;
  slug: string;
  description: string;
  finished_at: string | null;
  hero_image: string | null;
  date_created: string;
  date_updated: string;
};

export type Pattern = {
  id: string;
  title: string;
  slug: string;
  visibility: 'friends_family' | 'private';
  pdf_file: string | null;
  notes: string | null;
  date_created: string;
  date_updated: string;
};

export type Tag = {
  id: number;
  name: string;
  slug: string;
};

export type ProjectImage = {
  id: number;
  project_id: string;
  directus_files_id: string;
  caption: string | null;
  sort: number | null;
};

// Directus Schema
export type Schema = {
  projects: Project[];
  patterns: Pattern[];
  tags: Tag[];
  project_images: ProjectImage[];
};

// Create Directus client
const directusUrl = process.env.NEXT_PUBLIC_DIRECTUS_URL || 'http://localhost:8055';

export const directus = createDirectus<Schema>(directusUrl)
  .with(rest())
  .with(authentication());

// Server-side client (for API routes)
export const directusServer = createDirectus<Schema>(directusUrl).with(rest());

// Create authenticated client with token
export function createAuthenticatedClient(token: string) {
  const client = createDirectus<Schema>(directusUrl)
    .with(rest())
    .with(authentication('json', { credentials: 'include' }));
  
  // Set the static token
  client.setToken(token);
  
  return {
    client,
    token,
  };
}

// Helper: Get asset URL
export function getAssetUrl(fileId: string | null): string | null {
  if (!fileId) return null;
  return `${directusUrl}/assets/${fileId}`;
}

// Helper: Get responsive image URL with transformations
export function getImageUrl(
  fileId: string | null,
  options?: { width?: number; height?: number; quality?: number; fit?: 'cover' | 'contain' | 'inside' | 'outside' }
): string | null {
  if (!fileId) return null;
  
  const params = new URLSearchParams();
  if (options?.width) params.append('width', options.width.toString());
  if (options?.height) params.append('height', options.height.toString());
  if (options?.quality) params.append('quality', options.quality.toString());
  if (options?.fit) params.append('fit', options.fit);
  
  const query = params.toString();
  return `${directusUrl}/assets/${fileId}${query ? '?' + query : ''}`;
}
