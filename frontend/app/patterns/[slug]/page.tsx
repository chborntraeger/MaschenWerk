import { auth } from '@/auth';
import DeletePatternButton from '@/components/DeletePatternButton';
import { createAuthenticatedClient } from '@/lib/directus';
import { readItems } from '@directus/sdk';
import { format } from 'date-fns';
import Link from 'next/link';
import { notFound, redirect } from 'next/navigation';

export default async function PatternDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const session = await auth();

  if (!session?.user) {
    const { slug } = await params;
    redirect(`/login?callbackUrl=/patterns/${slug}`);
  }

  const { slug } = await params;
  const { client, token } = createAuthenticatedClient(session.user.accessToken);

  try {
    // Find pattern by slug
    const patterns = await client.request(
      readItems('patterns', {
        filter: {
          slug: { _eq: slug }
        },
        limit: 1
      })
    );

    if (!patterns || patterns.length === 0) {
      notFound();
    }

    const pattern = patterns[0];

    return (
      <div className="container mx-auto px-4 py-12">
        {/* Back Button */}
        <div className="mb-8">
          <Link
            href="/patterns"
            className="inline-flex items-center text-pink-600 hover:text-pink-700 transition"
          >
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            Back to Patterns
          </Link>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="bg-white rounded-xl shadow-sm p-8 mb-8 border border-gray-100">
            <div className="flex items-start justify-between mb-4">
              <h1 className="text-4xl font-bold text-gray-900">{pattern.title}</h1>
              <span
                className={`text-sm px-3 py-1 rounded-full ${
                  pattern.visibility === 'friends_family'
                    ? 'bg-blue-100 text-blue-700'
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                {pattern.visibility === 'friends_family' ? 'Friends & Family' : 'Private'}
              </span>
            </div>

            <div className="text-sm text-gray-500 mb-6">
              Added on {format(new Date(pattern.date_created), 'MMMM d, yyyy')}
            </div>

            {pattern.notes && (
              <div className="prose max-w-none">
                <p className="text-gray-700 whitespace-pre-wrap">{pattern.notes}</p>
              </div>
            )}
          </div>

          {/* Admin Actions */}
          {session?.user?.role === 'Administrator' && (
            <div className="mb-8">
              <DeletePatternButton patternId={pattern.id} patternTitle={pattern.title} />
            </div>
          )}

          {/* PDF Download */}
          {pattern.pdf_file && (
            <div className="bg-pink-50 rounded-xl p-8 border border-pink-100">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Download Pattern</h2>
              <p className="text-gray-600 mb-6">
                Click the button below to download the PDF pattern file.
              </p>
              <a
                href={`/api/download-pattern/${pattern.slug}`}
                className="inline-block bg-pink-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-pink-700 transition"
                target="_blank"
                rel="noopener noreferrer"
              >
                <svg
                  className="w-5 h-5 inline-block mr-2 -mt-1"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Download PDF
              </a>
            </div>
          )}
        </div>
      </div>
    );
  } catch (error) {
    notFound();
  }
}
