import { auth, signOut } from '@/auth';
import Link from 'next/link';
import AdminDropdown from './AdminDropdown';
import DarkModeToggle from './DarkModeToggle';
import SearchAutocomplete from './SearchAutocomplete';

export default async function Header() {
  const session = await auth();

  return (
    <header className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <nav className="flex items-center justify-between gap-6">
          <Link href="/" className="text-2xl font-bold text-gray-900 dark:text-white hover:text-gray-700 dark:hover:text-gray-300 whitespace-nowrap">
            🧶 Knitting Projects
          </Link>
          
          {/* Search Bar - centered */}
          <div className="flex-1 max-w-xl hidden md:block">
            <SearchAutocomplete />
          </div>
          
          <div className="flex items-center gap-6">
            <DarkModeToggle />
            <Link 
              href="/projects" 
              className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium"
            >
              Projects
            </Link>
            <Link 
              href="/timeline" 
              className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium"
            >
              Timeline
            </Link>
            
            {session?.user ? (
              <>
                <Link 
                  href="/patterns" 
                  className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-medium"
                >
                  Patterns
                </Link>
                
                {/* Admin dropdown for admins only */}
                {session.user.role === 'Administrator' && (
                  <AdminDropdown />
                )}
                
                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {session.user.name}
                  </span>
                  <form
                    action={async () => {
                      'use server';
                      await signOut({ redirectTo: '/' });
                    }}
                  >
                    <button
                      type="submit"
                      className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition"
                    >
                      Logout
                    </button>
                  </form>
                </div>
              </>
            ) : (
              <Link 
                href="/login" 
                className="px-4 py-2 bg-gray-900 dark:bg-pink-600 text-white rounded-lg hover:bg-gray-800 dark:hover:bg-pink-700 transition"
              >
                Login
              </Link>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
}
