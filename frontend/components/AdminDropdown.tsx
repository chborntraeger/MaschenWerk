'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function AdminDropdown() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div 
      className="relative"
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
    >
      <button className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium">
        Admin ▾
      </button>
      
      {isOpen && (
        <div className="absolute right-0 top-full pt-2 z-50">
          <div className="w-48 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg">
            <Link 
              href="/admin/projects/new"
              className="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-t-lg"
            >
              ➕ New Project
            </Link>
            <Link 
              href="/admin/patterns/new"
              className="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-b-lg"
            >
              📄 New Pattern
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
