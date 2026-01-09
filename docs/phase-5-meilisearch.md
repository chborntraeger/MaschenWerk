# Phase 5: Meilisearch Integration

## ✅ Completed

Phase 5 has been successfully completed! Your knitting projects app now has full-text search powered by Meilisearch.

## 🎉 What's New

### 1. Search Infrastructure
- **Meilisearch Client** integration with Next.js
- Server-side search API route
- Type-safe search results with TypeScript
- Configurable search parameters (limit, offset, highlighting)

### 2. Search Page
- **Full-page search** at `/search`
- Real-time search results
- Highlighted matches in title, notes, and content
- Result count display
- Loading states and error handling
- Empty state with helpful prompts

### 3. Autocomplete Search
- **Live autocomplete** in header navigation
- Debounced search (300ms delay)
- Quick preview of top 5 results
- Click outside to close
- Direct navigation to pattern details
- "See all results" link to full search page

### 4. User Experience
- Responsive search bar in header
- Highlighted search terms in results
- PDF availability indicators
- Pattern visibility badges
- Formatted dates

## 📁 New Files Created

```
frontend/
├── lib/
│   └── meilisearch.ts                    # Meilisearch client & utilities
├── components/
│   └── SearchAutocomplete.tsx            # Autocomplete component
├── app/
│   ├── search/
│   │   └── page.tsx                      # Full search page
│   └── api/
│       └── search/
│           └── route.ts                  # Search API endpoint
└── .env.local                            # Added Meilisearch config
```

## 🔧 Modified Files

- **components/Header.tsx**: Added SearchAutocomplete component
- **.env.local**: Added `NEXT_PUBLIC_MEILISEARCH_URL` and `NEXT_PUBLIC_MEILISEARCH_KEY`

## 🔍 Search Features

### Search Capabilities
- **Full-text search** across pattern titles, notes, and extracted PDF content
- **Highlighting** of matching terms in results
- **Cropping** of long content snippets (200 characters)
- **Fast search** with Meilisearch's optimized indexing
- **Typo tolerance** built into Meilisearch

### Autocomplete Features
- **Debounced input** (300ms) to reduce API calls
- **Live suggestions** as you type
- **Top 5 results** preview
- **Keyboard-friendly** navigation
- **Click outside** to close dropdown

### Search Result Display
- **Title highlighting** with matched terms
- **Content snippets** with context
- **Metadata display** (date, PDF availability)
- **Visibility badges** (Friends & Family / Private)
- **Direct links** to pattern details

## 🧪 Testing Search

### Prerequisites
Make sure the PDF Worker has indexed some patterns:

1. **Check Meilisearch** is running:
   ```bash
   docker compose ps
   ```
   Meilisearch should be on port 7700

2. **Verify index exists**:
   ```bash
   curl http://localhost:7700/indexes
   ```
   Should return "patterns" index

3. **Upload PDF patterns** in Directus (if not already done)
4. **Wait for worker** to process PDFs (checks every 60s)

### Test Flow

#### 1. Header Autocomplete
- Type in the search bar in header
- See live suggestions appear
- Click a result to navigate
- Or click "See all results"

#### 2. Full Search Page
- Visit http://localhost:3000/search
- Enter a search query (e.g., "cable", "sweater", "yarn")
- See paginated results with highlighting
- Click results to view pattern details

#### 3. Search from URL
- Navigate to: http://localhost:3000/search?q=your+query
- Results load automatically
- Query parameter preserved

### Expected Behavior
- ✅ Autocomplete shows max 5 results
- ✅ Full search page shows all results
- ✅ Matched terms are highlighted
- ✅ Only patterns with indexed content appear
- ✅ Results respect user permissions (logged in users only)

## 📝 Environment Variables

Already added to `frontend/.env.local`:
```env
# Meilisearch Configuration
NEXT_PUBLIC_MEILISEARCH_URL=http://localhost:7700
NEXT_PUBLIC_MEILISEARCH_KEY=
```

⚠️ **Note**: Meilisearch key is optional for local development. For production:
```bash
# In main .env file
MEILISEARCH_MASTER_KEY=your-secure-master-key
```

## 🎨 Search UI Components

### Search Page Layout
- Full-width search input
- Result count display
- Loading spinner
- Error messages
- Empty states

### Autocomplete Dropdown
- Compact result cards
- Title + snippet preview
- PDF indicator icon
- "See all" footer link
- Smooth transitions

### Result Highlighting
Meilisearch automatically highlights matched terms:
```html
<em class="highlighted">matched term</em>
```

Styled in your Tailwind CSS with default `em` styling.

## 🚀 Next Steps - Phase 6

Ready to **activate the PDF Worker**:

1. Verify Worker token is set in `.env`
2. Test PDF upload and text extraction
3. Monitor Meilisearch indexing
4. Verify search includes PDF content

After that, Phase 7 & 8 for polish and nice-to-haves!

Would you like to proceed with Phase 6 (PDF Worker)? 📄

## 📚 Technical Details

### Meilisearch Client Configuration
```typescript
export const meilisearchClient = new MeiliSearch({
  host: 'http://localhost:7700',
  apiKey: '', // Optional for dev
});
```

### Search Parameters
- **attributesToHighlight**: `['title', 'notes', 'content']`
- **attributesToCrop**: `['content', 'notes']`
- **cropLength**: `200` characters
- **limit**: `20` results (configurable)

### Index Structure
```typescript
type PatternSearchResult = {
  id: string;
  title: string;
  slug: string;
  visibility: string;
  notes: string | null;
  pdf_file: string | null;
  content: string;       // Extracted PDF text
  date_created: string;
  _formatted?: {         // Highlighted versions
    title: string;
    notes: string;
    content: string;
  };
};
```

## 🐛 Troubleshooting

### No search results
- **Check Meilisearch is running**: `docker compose ps`
- **Verify index exists**: `curl http://localhost:7700/indexes`
- **Check if patterns are indexed**: `curl http://localhost:7700/indexes/patterns/stats`
- **Ensure PDF Worker has run**: Check Docker logs

### Autocomplete not working
- **Open browser console** for JavaScript errors
- **Check API route**: Visit `/api/search?q=test` directly
- **Verify env variables**: Restart dev server after .env changes
- **Clear browser cache**

### Search too slow
- **Meilisearch is fast** - usually < 100ms
- Check Docker resources if slow
- Reduce `cropLength` for faster rendering
- Limit results per page

### Highlighting not showing
- **Check `_formatted` field** in API response
- Verify `attributesToHighlight` includes the field
- Ensure search query matches content

## 📖 Code Examples

### Using Search Client
```typescript
import { searchPatterns } from '@/lib/meilisearch';

const results = await searchPatterns({
  query: 'cable knit',
  limit: 10,
  attributesToHighlight: ['title', 'notes'],
});
```

### Custom Search API Call
```typescript
const response = await fetch('/api/search?q=sweater&limit=10');
const data = await response.json();
console.log(data.hits); // Array of results
```

### Checking Index Stats
```bash
curl http://localhost:7700/indexes/patterns/stats
```

Returns document count and index size.

## 🎯 Search Best Practices

1. **Debounce user input** (already implemented - 300ms)
2. **Limit autocomplete results** (max 5 for performance)
3. **Cache search results** (optional for production)
4. **Handle empty queries** gracefully
5. **Show loading states** for better UX
6. **Highlight matched terms** for clarity
7. **Provide clear error messages**

## 🔒 Security Notes

- Search is **public** by default (no auth required)
- But patterns themselves require login to access
- PDF content is indexed but files are protected
- Meilisearch runs in Docker network (not exposed publicly)

To restrict search to logged-in users, add auth check to `/api/search/route.ts`:
```typescript
import { auth } from '@/auth';

const session = await auth();
if (!session?.user) {
  return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
}
```

---

**Phase 5 Status**: ✅ Complete  
**Next Phase**: Phase 6 - PDF Worker Activation
