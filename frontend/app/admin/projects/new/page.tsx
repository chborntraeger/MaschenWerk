import { auth } from '@/auth';
import { redirect } from 'next/navigation';
import NewProjectForm from './NewProjectForm';

export default async function NewProjectPage() {
  const session = await auth();

  if (!session?.user) {
    redirect('/login?callbackUrl=/admin/projects/new');
  }

  // Check if user is admin
  if (session.user.role !== 'Administrator') {
    redirect('/');
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-3xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-slate-100 mb-4">
          Create New Project
        </h1>
        <p className="text-lg text-gray-600 dark:text-slate-300">
          Add a new knitting project to your collection
        </p>
      </div>

      <NewProjectForm accessToken={session.user.accessToken} />
    </div>
  );
}
