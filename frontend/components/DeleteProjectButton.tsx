'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

interface DeleteProjectButtonProps {
  projectId: string;
  projectTitle: string;
}

export default function DeleteProjectButton({ projectId, projectTitle }: DeleteProjectButtonProps) {
  const router = useRouter();
  const [isDeleting, setIsDeleting] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  async function handleDelete() {
    setIsDeleting(true);
    
    try {
      const response = await fetch(`/api/projects/${projectId}/delete`, {
        method: 'DELETE',
      });

      if (response.status === 401) {
        // Session expired, redirect to login
        router.push('/login');
        return;
      }

      if (!response.ok) {
        throw new Error('Failed to delete project');
      }

      router.push('/projects');
      router.refresh();
    } catch (error) {
      console.error('Delete error:', error);
      alert('Failed to delete project');
      setIsDeleting(false);
    }
  }

  if (!showConfirm) {
    return (
      <button
        onClick={() => setShowConfirm(true)}
        className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
      >
        🗑️ Delete Project
      </button>
    );
  }

  return (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <p className="text-red-800 dark:text-red-200 mb-4">
        Are you sure you want to delete <strong>{projectTitle}</strong>? This cannot be undone.
      </p>
      <div className="flex gap-3">
        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-400 transition"
        >
          {isDeleting ? 'Deleting...' : 'Yes, Delete'}
        </button>
        <button
          onClick={() => setShowConfirm(false)}
          disabled={isDeleting}
          className="px-4 py-2 bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-slate-300 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-600 transition"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
