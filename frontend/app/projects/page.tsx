import { auth } from '@/auth';
import { createAuthenticatedClient, directusServer, getImageUrl } from '@/lib/directus';
import { readItems } from '@directus/sdk';
import { format } from 'date-fns';
import Image from 'next/image';
import Link from 'next/link';

export default async function ProjectsPage() {
  const session = await auth();
  const isAdmin = session?.user?.role === 'Administrator';

  // Use authenticated client for admins to see draft projects
  let projects;
  try {
    if (isAdmin && session?.user?.accessToken && !session.error) {
      const { client } = createAuthenticatedClient(session.user.accessToken);
      projects = await client.request(
        readItems('projects', {
          sort: '-finished_at',
        })
      );
    } else {
      // Public users only see public projects
      projects = await directusServer.request(
        readItems('projects', {
          filter: { status: { _eq: 'public' } },
          sort: '-finished_at',
        })
      );
    }
  } catch (error) {
    console.error('Error loading projects:', error);
    // If token expired, fall back to public projects
    projects = await directusServer.request(
      readItems('projects', {
        filter: { status: { _eq: 'public' } },
        sort: '-finished_at',
      })
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="mb-12">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-slate-100 mb-4">
          My Knitting Projects
        </h1>
        <p className="text-lg text-gray-600 dark:text-slate-300">
          A collection of {projects.length} {isAdmin ? 'projects (including drafts)' : 'finished projects'}
        </p>
      </div>

      {projects.length === 0 ? (
        <div className="text-center py-12 text-gray-500 dark:text-slate-400">
          <p className="text-xl">No projects yet. Check back soon!</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {projects.map((project) => (
            <Link
              key={project.id}
              href={`/projects/${project.slug}`}
              className="group bg-white dark:bg-slate-900 rounded-xl shadow-sm hover:shadow-lg transition overflow-hidden border border-gray-200 dark:border-slate-700"
            >
              {/* Hero Image */}
              {project.hero_image ? (
                <div className="aspect-[4/3] relative overflow-hidden bg-gray-200 dark:bg-slate-800">
                  <Image
                    src={getImageUrl(project.hero_image, { width: 800, height: 600, fit: 'cover' }) || ''}
                    alt={project.title}
                    fill
                    className="object-cover group-hover:scale-105 transition duration-300"
                  />
                </div>
              ) : (
                <div className="aspect-[4/3] bg-gradient-to-br from-gray-200 to-gray-300 dark:from-slate-800 dark:to-slate-900 flex items-center justify-center">
                  <span className="text-6xl">🧶</span>
                </div>
              )}

              {/* Content */}
              <div className="p-6">
                <div className="flex items-start justify-between mb-2">
                  <h2 className="text-2xl font-semibold text-gray-900 dark:text-slate-100 group-hover:text-pink-600 dark:group-hover:text-pink-400 transition">
                    {project.title}
                  </h2>
                  {isAdmin && project.status === 'draft' && (
                    <span className="text-xs px-2 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 rounded-full font-medium">
                      Draft
                    </span>
                  )}
                </div>
                
                {project.finished_at && (
                  <p className="text-sm text-gray-500 dark:text-slate-400 mb-3">
                    Finished {format(new Date(project.finished_at), 'MMMM yyyy')}
                  </p>
                )}

                {project.description && (
                  <p className="text-gray-600 dark:text-slate-300 line-clamp-3">
                    {project.description.replace(/<[^>]*>/g, '').substring(0, 150)}...
                  </p>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
