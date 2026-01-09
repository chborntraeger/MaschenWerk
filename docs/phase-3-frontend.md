# Phase 3: Next.js Frontend

## ✅ Was erstellt wurde:

### Projekt-Setup
- ✅ Next.js 15 mit TypeScript
- ✅ Tailwind CSS für Styling
- ✅ ESLint konfiguriert
- ✅ Directus SDK integriert

### Layout & Navigation
- ✅ `components/Header.tsx` - Navigation mit Links
- ✅ `components/Footer.tsx` - Footer
- ✅ Responsive Layout mit Sticky Header

### Pages
- ✅ **Homepage** (`/`) - Hero mit Quick Links
- ✅ **Projects** (`/projects`) - Grid-Übersicht aller öffentlichen Projekte
- ✅ **Project Detail** (`/projects/[slug]`) - Einzelne Projektansicht
- ✅ **Timeline** (`/timeline`) - Chronologische Ansicht nach Jahr
- ✅ **Login** (`/login`) - Login-Seite (Placeholder)

### Directus Integration
- ✅ Type-safe SDK Setup
- ✅ Helper-Funktionen für Asset-URLs
- ✅ Image Optimization Support

---

## 🚀 Frontend starten

```bash
cd frontend
npm run dev
```

Öffne: **http://localhost:3000**

---

## 📁 Projektstruktur

```
frontend/
├── app/
│   ├── layout.tsx              # Root Layout mit Header/Footer
│   ├── page.tsx                # Homepage
│   ├── projects/
│   │   ├── page.tsx            # Projects Übersicht
│   │   └── [slug]/page.tsx     # Project Detail
│   ├── timeline/page.tsx       # Timeline View
│   └── login/page.tsx          # Login Page
├── components/
│   ├── Header.tsx              # Navigation
│   └── Footer.tsx              # Footer
├── lib/
│   └── directus.ts             # Directus Client & Types
├── .env.local                  # Environment Variables
└── package.json
```

---

## 🎨 Features

### Projects Übersicht
- Grid-Layout (responsive: 1/2/3 Spalten)
- Hero-Bilder mit Hover-Effekt
- Datum der Fertigstellung
- Textauszug aus Beschreibung
- Link zur Detailseite

### Project Detail
- Vollbild Hero-Image
- Markdown-Rendering der Beschreibung
- Fertigstellungsdatum
- Back-Navigation

### Timeline
- Gruppierung nach Jahr
- Chronologische Sortierung (neueste zuerst)
- Timeline-Design mit Punkten
- Sticky Jahr-Header

---

## 🔧 Nächste Schritte

### Phase 4: Auth & geschützte Bereiche

1. **Authentifizierung implementieren**
   ```bash
   npm install next-auth
   ```

2. **Protected Routes**
   - `/patterns` - Anleitungs-Bibliothek
   - `/patterns/[slug]` - PDF-Viewer

3. **PDF-Proxy Route**
   ```typescript
   // app/api/patterns/[id]/pdf/route.ts
   // Lädt PDFs serverseitig von Directus
   ```

4. **User Context**
   - Login/Logout
   - Session Management
   - Conditional Rendering

### Phase 5: Suche (Meilisearch)

1. **Search Page** (`/search`)
2. **Autocomplete Component**
3. **Filter (Tags, Jahr)**

---

## ✅ Test-Checklist

Teste das Frontend nachdem Directus läuft:

- [ ] Homepage lädt korrekt
- [ ] Projects-Seite zeigt alle public projects
- [ ] Timeline zeigt Projekte nach Jahr sortiert
- [ ] Project-Detail-Seiten sind erreichbar
- [ ] Navigation funktioniert
- [ ] Bilder werden geladen (wenn Directus läuft)
- [ ] Responsive Design auf Mobile

---

## 🐛 Troubleshooting

**Bilder laden nicht:**
- Prüfe ob Directus läuft: `docker compose ps`
- Prüfe `.env.local`: `NEXT_PUBLIC_DIRECTUS_URL=http://localhost:8055`

**"Error: Unable to fetch projects":**
- Prüfe Directus Public Permissions
- `python3 test-api.py` sollte Projects zeigen

**CORS Fehler:**
- In Directus `.env`: `CORS_ORIGIN=http://localhost:3000`
- Docker neu starten: `docker compose restart directus`

---

## 📝 Development

```bash
# Dev Server (mit Hot Reload)
npm run dev

# Build für Production
npm run build

# Production Server
npm run start

# Type Check
npm run type-check

# Lint
npm run lint
```

---

## 🎉 Phase 3 abgeschlossen!

Das Frontend ist ready! Du kannst jetzt:
- Projects durchstöbern
- Timeline ansehen
- Basis-UI nutzen

**Weiter zu Phase 4**: Auth & geschützte Patterns
