import { auth } from '@/auth';
import { redirect } from 'next/navigation';
import NewPatternForm from './NewPatternForm';

export default async function NewPatternPage() {
  const session = await auth();

  if (!session?.user) {
    redirect('/login?callbackUrl=/admin/patterns/new');
  }

  // Check if user is admin
  if (session.user.role !== 'Administrator') {
    redirect('/');
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-3xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-slate-100 mb-4">
          Upload New Pattern
        </h1>
        <p className="text-lg text-gray-600 dark:text-slate-300">
          Add a new knitting pattern with PDF
        </p>
      </div>

      <NewPatternForm accessToken={session.user.accessToken} />
    </div>
  );
}
