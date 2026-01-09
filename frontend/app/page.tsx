import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-slate-100 mb-4">
          🧶 Welcome to my Knitting Journey
        </h1>
        <p className="text-xl text-gray-600 dark:text-slate-300 max-w-2xl mx-auto">
          A collection of handmade knitting projects, patterns, and creative adventures with yarn.
        </p>
      </div>

      {/* Quick Links */}
      <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <Link 
          href="/projects" 
          className="p-6 bg-white dark:bg-slate-800 rounded-xl shadow-sm hover:shadow-md transition border border-gray-200 dark:border-slate-600"
        >
          <div className="text-4xl mb-3">🎨</div>
          <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-slate-100">Browse Projects</h3>
          <p className="text-gray-600 dark:text-slate-300">
            Explore all finished and ongoing knitting projects
          </p>
        </Link>

        <Link 
          href="/timeline" 
          className="p-6 bg-white dark:bg-slate-800 rounded-xl shadow-sm hover:shadow-md transition border border-gray-200 dark:border-slate-600"
        >
          <div className="text-4xl mb-3">📅</div>
          <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-slate-100">Timeline</h3>
          <p className="text-gray-600 dark:text-slate-300">
            View projects chronologically by completion date
          </p>
        </Link>

        <Link 
          href="/login" 
          className="p-6 bg-white dark:bg-slate-800 rounded-xl shadow-sm hover:shadow-md transition border border-gray-200 dark:border-slate-600"
        >
          <div className="text-4xl mb-3">🔐</div>
          <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-slate-100">Pattern Library</h3>
          <p className="text-gray-600 dark:text-slate-300">
            Access to exclusive patterns (login required)
          </p>
        </Link>
      </div>
    </div>
  );
}
