import { auth } from '@/auth';
import { createAuthenticatedClient } from '@/lib/directus';
import { readItems } from '@directus/sdk';
import { format } from 'date-fns';
import Link from 'next/link';
import { redirect } from 'next/navigation';

export default async function PatternsPage() {
  const session = await auth();

  if (!session?.user) {
    redirect('/login?callbackUrl=/patterns');
  }

  // Create authenticated client
  const { client, token } = createAuthenticatedClient(session.user.accessToken);

  // Fetch patterns based on user role
  // Friends & Family can see friends_family patterns
  const patterns = await client.request(
    readItems('patterns', {
      sort: '-date_created',
    })
  );

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mb-12">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-slate-100 mb-4">
          Knitting Patterns
        </h1>
        <p className="text-lg text-gray-600 dark:text-slate-300">
          A collection of {patterns.length} knitting patterns
        </p>
      </div>

      {patterns.length === 0 ? (
        <div className="text-center py-12 text-gray-500 dark:text-slate-400">
          <p className="text-xl">No patterns yet. Check back soon!</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {patterns.map((pattern) => (
            <Link
              key={pattern.id}
              href={`/patterns/${pattern.slug}`}
              className="group bg-white dark:bg-slate-900 rounded-xl shadow-sm hover:shadow-lg transition p-6 border border-gray-200 dark:border-slate-700"
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-slate-100 group-hover:text-pink-600 dark:group-hover:text-pink-400 transition">
                  {pattern.title}
                </h3>
                <span
                  className={`text-xs px-2 py-1 rounded-full ${
                    pattern.visibility === 'friends_family'
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                      : 'bg-gray-100 text-gray-700 dark:bg-slate-700 dark:text-slate-300'
                  }`}
                >
                  {pattern.visibility === 'friends_family' ? 'Friends & Family' : 'Private'}
                </span>
              </div>

              {pattern.notes && (
                <p className="text-gray-600 dark:text-slate-300 mb-4 line-clamp-3">{pattern.notes}</p>
              )}

              <div className="flex items-center justify-between text-sm text-gray-500 dark:text-slate-400 pt-4 border-t border-gray-200 dark:border-slate-700">
                <span>{format(new Date(pattern.date_created), 'MMM d, yyyy')}</span>
                {pattern.pdf_file && (
                  <span className="text-pink-600 dark:text-pink-400 font-medium">PDF Available</span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
