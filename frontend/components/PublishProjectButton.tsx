'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

type Props = {
  projectId: string;
  projectTitle: string;
};

export default function PublishProjectButton({ projectId, projectTitle }: Props) {
  const [isPublishing, setIsPublishing] = useState(false);
  const router = useRouter();

  const handlePublish = async () => {
    if (!confirm(`Möchtest du das Projekt "${projectTitle}" wirklich veröffentlichen?`)) {
      return;
    }

    setIsPublishing(true);

    try {
      const response = await fetch(`/api/projects/${projectId}/publish`, {
        method: 'POST',
      });

      if (response.status === 401) {
        // Session expired, redirect to login
        router.push('/login');
        return;
      }

      if (!response.ok) {
        throw new Error('Failed to publish project');
      }

      router.refresh();
    } catch (error) {
      console.error('Error publishing project:', error);
      alert('Fehler beim Veröffentlichen des Projekts');
    } finally {
      setIsPublishing(false);
    }
  };

  return (
    <button
      onClick={handlePublish}
      disabled={isPublishing}
      className="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 text-white font-medium rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <svg className="w-5 h-5 mr-2" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
        <path d="M5 13l4 4L19 7"></path>
      </svg>
      {isPublishing ? 'Veröffentliche...' : 'Veröffentlichen'}
    </button>
  );
}
