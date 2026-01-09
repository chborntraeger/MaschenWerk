'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

interface NewProjectFormProps {
  accessToken: string;
}

export default function NewProjectForm({ accessToken }: NewProjectFormProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [heroImage, setHeroImage] = useState<File | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError('');

    const formData = new FormData(e.currentTarget);
    
    try {
      const directusUrl = process.env.NEXT_PUBLIC_DIRECTUS_URL || 'http://localhost:8055';
      
      // Upload hero image if provided
      let heroImageId = null;
      if (heroImage) {
        const imageFormData = new FormData();
        imageFormData.append('file', heroImage);
        
        const uploadResponse = await fetch(`${directusUrl}/files`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
          body: imageFormData,
        });

        if (!uploadResponse.ok) {
          throw new Error('Failed to upload image');
        }

        const uploadData = await uploadResponse.json();
        heroImageId = uploadData.data.id;
      }

      // Create project
      const projectData = {
        title: formData.get('title'),
        slug: (formData.get('title') as string).toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, ''),
        description: formData.get('description'),
        finished_at: formData.get('finished_at') || null,
        status: formData.get('status') || 'draft',
        hero_image: heroImageId,
      };

      const response = await fetch(`${directusUrl}/items/projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify(projectData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.errors?.[0]?.message || 'Failed to create project');
      }

      const data = await response.json();
      router.push(`/projects/${data.data.slug}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-200 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
          Project Title *
        </label>
        <input
          type="text"
          id="title"
          name="title"
          required
          className="w-full px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-slate-100 rounded-lg focus:border-pink-500 focus:ring-2 focus:ring-pink-500/50 outline-none"
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          rows={6}
          className="w-full px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-slate-100 rounded-lg focus:border-pink-500 focus:ring-2 focus:ring-pink-500/50 outline-none"
        />
      </div>

      <div>
        <label htmlFor="finished_at" className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
          Finished Date
        </label>
        <input
          type="date"
          id="finished_at"
          name="finished_at"
          className="w-full px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-slate-100 rounded-lg focus:border-pink-500 focus:ring-2 focus:ring-pink-500/50 outline-none"
        />
      </div>

      <div>
        <label htmlFor="status" className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
          Status *
        </label>
        <select
          id="status"
          name="status"
          required
          className="w-full px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-slate-100 rounded-lg focus:border-pink-500 focus:ring-2 focus:ring-pink-500/50 outline-none"
        >
          <option value="draft">Draft</option>
          <option value="public">Public</option>
        </select>
      </div>

      <div>
        <label htmlFor="hero_image" className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-2">
          Hero Image
        </label>
        <input
          type="file"
          id="hero_image"
          accept="image/*"
          onChange={(e) => setHeroImage(e.target.files?.[0] || null)}
          className="w-full px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-slate-100 rounded-lg focus:border-pink-500 focus:ring-2 focus:ring-pink-500/50 outline-none file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-pink-50 dark:file:bg-pink-900/20 file:text-pink-700 dark:file:text-pink-300 file:cursor-pointer hover:file:bg-pink-100 dark:hover:file:bg-pink-900/30"
        />
      </div>

      <div className="flex gap-4">
        <button
          type="submit"
          disabled={loading}
          className="flex-1 bg-pink-600 hover:bg-pink-700 disabled:bg-gray-400 text-white font-medium py-3 px-6 rounded-lg transition"
        >
          {loading ? 'Creating...' : 'Create Project'}
        </button>
        <button
          type="button"
          onClick={() => router.back()}
          className="px-6 py-3 bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-slate-300 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-600 transition"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
