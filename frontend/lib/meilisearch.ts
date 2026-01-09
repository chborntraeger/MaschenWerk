import { MeiliSearch } from 'meilisearch';

// Meilisearch client configuration
const meilisearchUrl = process.env.NEXT_PUBLIC_MEILISEARCH_URL || 'http://localhost:7700';
const meilisearchKey = process.env.NEXT_PUBLIC_MEILISEARCH_KEY || '';

export const meilisearchClient = new MeiliSearch({
  host: meilisearchUrl,
  apiKey: meilisearchKey,
});

// Index names
export const PATTERNS_INDEX = 'patterns_index';

// Search result types
export type PatternSearchResult = {
  id: string;
  title: string;
  slug: string;
  visibility: string;
  notes: string | null;
  pdf_file: string | null;
  content: string;
  date_created: string;
  _formatted?: {
    title: string;
    notes: string;
    content: string;
  };
};

// Search options
export type SearchOptions = {
  query: string;
  limit?: number;
  offset?: number;
  attributesToHighlight?: string[];
  attributesToCrop?: string[];
  cropLength?: number;
};

// Perform search
export async function searchPatterns(options: SearchOptions) {
  const index = meilisearchClient.index<PatternSearchResult>(PATTERNS_INDEX);
  
  const searchParams: any = {
    limit: options.limit || 20,
    offset: options.offset || 0,
  };

  if (options.attributesToHighlight) {
    searchParams.attributesToHighlight = options.attributesToHighlight;
  }

  if (options.attributesToCrop) {
    searchParams.attributesToCrop = options.attributesToCrop;
  }

  if (options.cropLength) {
    searchParams.cropLength = options.cropLength;
  }

  try {
    const results = await index.search(options.query, searchParams);
    return results;
  } catch (error) {
    console.error('Meilisearch error:', error);
    throw error;
  }
}
