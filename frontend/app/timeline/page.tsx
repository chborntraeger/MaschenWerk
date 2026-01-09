import { directusServer } from '@/lib/directus';
import { readItems } from '@directus/sdk';
import { format } from 'date-fns';
import Link from 'next/link';

export default async function TimelinePage() {
  // Fetch public projects sorted by finished date
  const projects = await directusServer.request(
    readItems('projects', {
      filter: { 
        status: { _eq: 'public' },
        finished_at: { _nnull: true }
      },
      sort: ['-finished_at'],
      limit: -1,
    })
  );

  // Group by year
  const projectsByYear = projects.reduce((acc, project) => {
    if (!project.finished_at) return acc;
    
    const year = new Date(project.finished_at).getFullYear();
    if (!acc[year]) acc[year] = [];
    acc[year].push(project);
    return acc;
  }, {} as Record<number, typeof projects>);

  const years = Object.keys(projectsByYear).map(Number).sort((a, b) => b - a);

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <div className="mb-12 text-center">
        <div className="text-6xl mb-4">📅</div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-slate-100 mb-4">
          Project Timeline
        </h1>
        <p className="text-lg text-gray-600 dark:text-slate-300">
          A chronological view of all completed projects
        </p>
      </div>

      {years.length === 0 ? (
        <div className="text-center py-12 text-gray-500 dark:text-slate-400">
          <p className="text-xl">No completed projects yet.</p>
        </div>
      ) : (
        <div className="space-y-12">
          {years.map((year) => (
            <div key={year} className="relative">
              {/* Year Header */}
              <div className="sticky top-20 bg-slate-100 dark:bg-slate-900 py-4 mb-6 border-b border-gray-300 dark:border-slate-700 z-10">
                <h2 className="text-3xl font-bold text-gray-900 dark:text-slate-100">{year}</h2>
              </div>

              {/* Projects */}
              <div className="space-y-6 pl-4 border-l-2 border-pink-400 dark:border-pink-500">
                {projectsByYear[year].map((project) => (
                  <Link
                    key={project.id}
                    href={`/projects/${project.slug}`}
                    className="block group -ml-px pl-8 relative"
                  >
                    {/* Timeline dot */}
                    <div className="absolute left-0 top-2 w-4 h-4 bg-pink-400 dark:bg-pink-500 group-hover:bg-pink-600 dark:group-hover:bg-pink-400 rounded-full -translate-x-1/2 transition ring-4 ring-slate-100 dark:ring-slate-900"></div>

                    <div className="bg-white dark:bg-slate-900 p-6 rounded-lg shadow-sm hover:shadow-lg transition border border-gray-200 dark:border-slate-700">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-xl font-semibold text-gray-900 dark:text-slate-100 group-hover:text-pink-600 dark:group-hover:text-pink-400 transition">
                          {project.title}
                        </h3>
                        {project.finished_at && (
                          <span className="text-sm text-gray-500 dark:text-slate-400 whitespace-nowrap ml-4 font-medium">
                            {format(new Date(project.finished_at), 'MMM d')}
                          </span>
                        )}
                      </div>
                      
                      {project.description && (
                        <p className="text-gray-600 dark:text-slate-300 line-clamp-2">
                          {project.description.replace(/<[^>]*>/g, '').substring(0, 120)}...
                        </p>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
