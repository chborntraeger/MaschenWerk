import { searchPatterns } from '@/lib/meilisearch';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('q') || '';
  const limit = parseInt(searchParams.get('limit') || '20');
  const offset = parseInt(searchParams.get('offset') || '0');

  if (!query) {
    return NextResponse.json({
      hits: [],
      estimatedTotalHits: 0,
      query: '',
    });
  }

  try {
    const results = await searchPatterns({
      query,
      limit,
      offset,
      attributesToHighlight: ['title', 'notes', 'content'],
      attributesToCrop: ['content', 'notes'],
      cropLength: 200,
    });

    return NextResponse.json({
      hits: results.hits,
      estimatedTotalHits: results.estimatedTotalHits,
      query: results.query,
      processingTimeMs: results.processingTimeMs,
    });
  } catch (error) {
    console.error('Search API error:', error);
    return NextResponse.json(
      { error: 'Search failed' },
      { status: 500 }
    );
  }
}
