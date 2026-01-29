'use client';

import { PatternSearchResult } from '@/lib/meilisearch';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';

export default function SearchAutocomplete() {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<PatternSearchResult[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Debounced search
  useEffect(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    if (!query.trim()) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    timeoutRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&limit=5`);
        if (response.ok) {
          const data = await response.json();
          setResults(data.hits || []);
          setIsOpen(true);
        }
      } catch (error) {
        console.error('Autocomplete error:', error);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [query]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query)}`);
      setIsOpen(false);
      setQuery('');
    }
  };

  return (
    <div ref={wrapperRef} className="relative w-full max-w-md">
      <form onSubmit={handleSubmit}>
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search patterns..."
            className="w-full px-4 py-2 pr-10 bg-slate-700 border border-slate-600 text-slate-100 placeholder-slate-400 rounded-lg focus:border-pink-500 focus:ring-2 focus:ring-pink-500/50 outline-none transition text-sm"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-pink-600 transition"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </button>
        </div>
      </form>

      {/* Autocomplete Dropdown */}
      {isOpen && (results.length > 0 || loading) && (
        <div className="absolute z-50 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-96 overflow-y-auto">
          {loading ? (
            <div className="px-4 py-8 text-center text-gray-500">
              <div className="inline-block animate-spin rounded-full h-6 w-6 border-2 border-pink-500 border-t-transparent"></div>
            </div>
          ) : (
            <>
              {results.map((result) => (
                <Link
                  key={result.id}
                  href={`/patterns/${result.slug}`}
                  onClick={() => {
                    setIsOpen(false);
                    setQuery('');
                  }}
                  className="block px-4 py-3 hover:bg-gray-50 transition border-b border-gray-100 last:border-b-0"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <h4
                        className="text-sm font-medium text-gray-900 truncate"
                        dangerouslySetInnerHTML={{
                          __html: result._formatted?.title || result.title,
                        }}
                      />
                      {result._formatted?.notes && (
                        <p
                          className="text-xs text-gray-500 mt-1 line-clamp-1"
                          dangerouslySetInnerHTML={{
                            __html: result._formatted.notes,
                          }}
                        />
                      )}
                    </div>
                    {result.pdf_file && (
                      <svg
                        className="w-4 h-4 text-pink-600 ml-2 flex-shrink-0"
                        fill="none"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                    )}
                  </div>
                </Link>
              ))}
              <Link
                href={`/search?q=${encodeURIComponent(query)}`}
                onClick={() => {
                  setIsOpen(false);
                  setQuery('');
                }}
                className="block px-4 py-3 text-sm text-pink-600 hover:bg-pink-50 transition text-center font-medium"
              >
                See all results for "{query}"
              </Link>
            </>
          )}
        </div>
      )}
    </div>
  );
}
