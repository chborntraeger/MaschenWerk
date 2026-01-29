'use client';

import { PatternSearchResult } from '@/lib/meilisearch';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { Suspense, useEffect, useState } from 'react';

function SearchResults() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get('q') || '';

  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState<PatternSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [totalHits, setTotalHits] = useState(0);

  useEffect(() => {
    if (initialQuery) {
      performSearch(initialQuery);
    }
  }, [initialQuery]);

  const performSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) {
      setResults([]);
      setTotalHits(0);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);
      
      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data = await response.json();
      setResults(data.hits || []);
      setTotalHits(data.estimatedTotalHits || 0);
    } catch (err) {
      setError('Search failed. Please try again.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    router.push(`/search?q=${encodeURIComponent(query)}`);
    performSearch(query);
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        {/* Search Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🔍 Search Patterns
          </h1>
          <p className="text-lg text-gray-600">
            Search through your knitting pattern collection
          </p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="relative">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for patterns, techniques, yarn types..."
              className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:border-pink-500 focus:ring-2 focus:ring-pink-200 outline-none transition"
              autoFocus
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 bg-pink-600 text-white rounded-lg hover:bg-pink-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Results Count */}
        {query && !loading && (
          <div className="mb-6 text-gray-600">
            {totalHits === 0 ? (
              <p>No results found for "{query}"</p>
            ) : (
              <p>Found {totalHits} {totalHits === 1 ? 'result' : 'results'} for "{query}"</p>
            )}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-pink-500 border-t-transparent"></div>
            <p className="mt-4 text-gray-600">Searching...</p>
          </div>
        )}

        {/* Search Results */}
        {!loading && results.length > 0 && (
          <div className="space-y-6">
            {results.map((result) => (
              <Link
                key={result.id}
                href={`/patterns/${result.slug}`}
                className="block bg-white rounded-xl shadow-sm hover:shadow-lg transition p-6 border border-gray-100"
              >
                <div className="flex items-start justify-between mb-3">
                  <h3
                    className="text-2xl font-semibold text-gray-900 hover:text-pink-600 transition"
                    dangerouslySetInnerHTML={{
                      __html: result._formatted?.title || result.title,
                    }}
                  />
                  <span
                    className={`text-xs px-2 py-1 rounded-full whitespace-nowrap ${
                      result.visibility === 'friends_family'
                        ? 'bg-blue-100 text-blue-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    {result.visibility === 'friends_family' ? 'Friends & Family' : 'Private'}
                  </span>
                </div>

                {result._formatted?.content && (
                  <div
                    className="text-gray-600 prose max-w-none mb-4"
                    dangerouslySetInnerHTML={{
                      __html: result._formatted.content,
                    }}
                  />
                )}

                {result._formatted?.notes && (
                  <div
                    className="text-gray-600 prose max-w-none mb-4"
                    dangerouslySetInnerHTML={{
                      __html: result._formatted.notes,
                    }}
                  />
                )}

                <div className="flex items-center gap-4 text-sm text-gray-500 pt-4 border-t border-gray-100">
                  <span>{new Date(result.date_created).toLocaleDateString()}</span>
                  {result.pdf_file && (
                    <span className="flex items-center gap-1 text-pink-600 font-medium">
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                      PDF Available
                    </span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && !query && results.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <svg
              className="w-24 h-24 mx-auto mb-4 text-gray-300"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <p className="text-xl mb-2">Start searching for patterns</p>
            <p className="text-gray-400">
              Try searching for yarn types, techniques, or pattern names
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={
      <div className="container mx-auto px-4 py-12">
        <div className="text-center">Loading search...</div>
      </div>
    }>
      <SearchResults />
    </Suspense>
  );
}
