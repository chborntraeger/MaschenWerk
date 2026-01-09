export default function Footer() {
  return (
    <footer className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-gray-600 dark:text-gray-400">
          <p>🧶 Knitting Projects • Selfhosted with Directus & Next.js</p>
          <p className="text-sm mt-2">© {new Date().getFullYear()} • Made with ❤️ and yarn</p>
        </div>
      </div>
    </footer>
  );
}
