import { auth } from '@/auth';
import DeleteProjectButton from '@/components/DeleteProjectButton';
import PublishProjectButton from '@/components/PublishProjectButton';
import { createAuthenticatedClient, directusServer, getImageUrl } from '@/lib/directus';
import { readItems } from '@directus/sdk';
import { format } from 'date-fns';
import Image from 'next/image';
import Link from 'next/link';
import { notFound } from 'next/navigation';

type Props = {
  params: Promise<{ slug: string }>;
};

export default async function ProjectDetailPage({ params }: Props) {
  const { slug } = await params;
  const session = await auth();
  const isAdmin = session?.user?.role === 'Administrator';

  // Fetch project by slug
  try {
    // Admins can see all projects, others only public ones
    let filter: any = { slug: { _eq: slug } };
    
    // Non-admins can only see public projects
    if (!isAdmin) {
      filter = {
        _and: [
          { slug: { _eq: slug } },
          { status: { _eq: 'public' } }
        ]
      };
    }

    // Use authenticated client for admins to see draft projects
    const client = isAdmin && session?.user?.accessToken
      ? createAuthenticatedClient(session.user.accessToken).client
      : directusServer;

    const projects = await client.request(
      readItems('projects', {
        filter,
        limit: 1
      })
    );

    if (!projects || projects.length === 0) {
      notFound();
    }

    const project = projects[0];

    return (
      <div className="min-h-screen">
        <article className="container mx-auto px-4 py-8 max-w-5xl">
          {/* Back Link */}
          <Link 
            href="/projects"
            className="inline-flex items-center text-pink-600 dark:text-pink-400 hover:text-pink-700 dark:hover:text-pink-300 mb-8 font-medium transition group"
          >
            <svg className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
              <path d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            Back to Projects
          </Link>

          {/* Hero Image */}
          {project.hero_image && (
            <div className="aspect-video relative overflow-hidden rounded-2xl mb-8 shadow-2xl border border-gray-200 dark:border-slate-700">
              <Image
                src={getImageUrl(project.hero_image, { width: 1200, height: 675, fit: 'cover' }) || ''}
                alt={project.title}
                fill
                className="object-cover"
                priority
              />
            </div>
          )}

          {/* Content Card */}
          <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-lg border border-gray-200 dark:border-slate-700 overflow-hidden">
            {/* Header */}
            <header className="p-8 pb-6 border-b border-gray-200 dark:border-slate-700">
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-slate-100 mb-4">
                {project.title}
              </h1>
              
              {project.finished_at && (
                <div className="flex items-center gap-2 text-lg text-gray-600 dark:text-slate-400">
                  <svg className="w-5 h-5 text-pink-500" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                    <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  <span>Finished in <strong className="text-pink-600 dark:text-pink-400">{format(new Date(project.finished_at), 'MMMM yyyy')}</strong></span>
                </div>
              )}
            </header>

            {/* Description */}
            {project.description && (
              <div className="p-8 bg-white dark:bg-slate-800 text-gray-700 dark:text-slate-300">
                <div 
                  className="prose prose-lg max-w-none 
                    [&_*]:text-gray-700 dark:[&_*]:!text-slate-300
                    [&_h1]:!text-gray-900 dark:[&_h1]:!text-slate-100 [&_h1]:font-bold
                    [&_h2]:!text-gray-900 dark:[&_h2]:!text-slate-100 [&_h2]:font-semibold
                    [&_h3]:!text-gray-900 dark:[&_h3]:!text-slate-100 [&_h3]:font-semibold
                    [&_strong]:!text-gray-900 dark:[&_strong]:!text-slate-200 [&_strong]:font-semibold
                    [&_a]:text-pink-600 dark:[&_a]:!text-pink-400 [&_a]:hover:underline"
                  dangerouslySetInnerHTML={{ __html: project.description }}
                />
              </div>
            )}

            {/* Footer */}
            <div className="border-t border-gray-200 dark:border-slate-700 p-6 bg-gray-50 dark:bg-slate-800/50">
              <div className="flex items-center justify-between">
                <Link 
                  href="/projects"
                  className="inline-flex items-center text-gray-600 dark:text-slate-400 hover:text-pink-600 dark:hover:text-pink-400 transition group font-medium"
                >
                  <svg className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                    <path d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                  </svg>
                  View all projects
                </Link>
                
                <div className="flex gap-3">
                  {isAdmin && project.status === 'draft' && (
                    <PublishProjectButton projectId={project.id} projectTitle={project.title} />
                  )}
                  {isAdmin && (
                    <DeleteProjectButton projectId={project.id} projectTitle={project.title} />
                  )}
                </div>
              </div>
            </div>
          </div>
        </article>
      </div>
    );
  } catch (error) {
    notFound();
  }
}
