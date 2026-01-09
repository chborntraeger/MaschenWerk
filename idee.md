# 🧶 Knitting Projects – Selfhosted CMS (Directus + Next.js)

## Ziel
Selfhosted Web-App zur Dokumentation von Strickprojekten:
- Öffentlicher Blog / Projekt-Showcase
- Suche inkl. PDF-Volltext
- Geschützte Anleitungen (nur Freunde/Familie)
- Kalender-/Timeline-Ansicht fertiger Projekte

---

## Phase 0 – Grundlagen & Setup

- [ ] Git-Repository initialisieren
- [ ] Docker Compose Grundsetup anlegen
  - [ ] Postgres
  - [ ] Directus
  - [ ] Meilisearch
  - [ ] (optional) MinIO oder lokales Storage
- [ ] Environment Variablen definieren (`.env`)
- [ ] Reverse Proxy (Caddy / Traefik / Nginx) vorbereiten
- [ ] HTTPS lokal (optional mkcert)

---

## Phase 1 – Directus konfigurieren

### Collections / Datenmodell
- [ ] Collection `projects` anlegen
  - [ ] title
  - [ ] slug (unique)
  - [ ] status (`draft`, `public`, `private`)
  - [ ] finished_at (date)
  - [ ] description (rich text / markdown)
  - [ ] hero_image (file)
  - [ ] gallery (relation)
  - [ ] tags (m2m)
  - [ ] private_notes (text)

- [ ] Collection `patterns` (Anleitungen)
  - [ ] title
  - [ ] slug
  - [ ] visibility (`friends_family`, `private`)
  - [ ] pdf_file (file)
  - [ ] notes
  - [ ] tags (m2m)

- [ ] Collection `tags`
  - [ ] name
  - [ ] slug

- [ ] Junction tables
  - [ ] `project_images`
    - project_id
    - file_id
    - caption
    - sort
  - [ ] `project_patterns`
    - project_id
    - pattern_id

---

## Phase 2 – Rollen & Rechte

- [ ] Rolle `Public` konfigurieren
  - [ ] Read: `projects` mit `status=public`
  - [ ] Read: zugehörige Bilder

- [ ] Rolle `Friends_Family` konfigurieren
  - [ ] Read: public projects
  - [ ] Read: `patterns` mit `visibility=friends_family`
  - [ ] Kein direkter Asset-Zugriff auf PDFs

- [ ] Rolle `Admin`
  - [ ] Vollzugriff

- [ ] Service-Account / Static Token für Worker anlegen

---

## Phase 3 – Frontend (Next.js)

### Basis
- [ ] Next.js App initialisieren
- [ ] Auth-Anbindung an Directus (JWT / Session)
- [ ] Layout & Theme (Blog/Portfolio-Stil)

### Öffentliche Seiten
- [ ] `/projects` – Projektübersicht
- [ ] `/projects/[slug]` – Projekt-Detailseite
- [ ] Galerie-Komponente (responsive)
- [ ] Timeline-/Jahresübersicht (finished_at)

### Geschützte Bereiche
- [ ] Login-Seite
- [ ] Sichtbarkeit für Friends/Family
- [ ] Anzeige verknüpfter Anleitungen

---

## Phase 4 – Geschützte PDF-Auslieferung

- [ ] API-Route `/api/patterns/[id]/pdf`
  - [ ] Auth prüfen
  - [ ] Rolle prüfen (Friends/Family oder Admin)
  - [ ] PDF serverseitig von Directus abrufen
  - [ ] PDF streamen (keine public URLs)

- [ ] PDF-Viewer im Frontend einbinden

---

## Phase 5 – Suche (Meilisearch)

### Indizes
- [ ] Index `projects_index`
  - [ ] title
  - [ ] description_plain
  - [ ] tags
  - [ ] finished_at
  - [ ] visibility

- [ ] Index `patterns_index`
  - [ ] title
  - [ ] notes
  - [ ] tags
  - [ ] visibility
  - [ ] pdf_text

### Search UI
- [ ] `/search` Seite
- [ ] Autocomplete
- [ ] Filter (Tags, Jahr)
- [ ] Treffer-Typen (Projekt vs. Anleitung)

---

## Phase 6 – PDF-Volltext-Indexing

- [ ] Worker-Service anlegen
- [ ] PDF-Text-Extraktion
  - [ ] `pdftotext` (Poppler)
  - [ ] Fallback optional: Apache Tika
- [ ] Meilisearch Upsert für `patterns_index`
- [ ] Directus Webhook / Flow
  - [ ] Trigger bei Upload / Update von `patterns.pdf_file`

---

## Phase 7 – Polishing & Qualität

- [ ] Bildverarbeitung
  - [ ] Thumbnails
  - [ ] Responsive Images
  - [ ] EXIF-Daten entfernen
- [ ] SEO
  - [ ] Slugs
  - [ ] Meta / OpenGraph
  - [ ] Sitemap
- [ ] Suche Ranking feinjustieren
- [ ] Fehler- & Access-Logging
- [ ] Backup-Strategie (DB + Uploads)

---

## Phase 8 – Nice-to-have

- [ ] Kalenderansicht (Monat/Jahr)
- [ ] Import/Export (JSON)
- [ ] Kommentare / Notizen pro Projekt (privat)
- [ ] Einladungssystem für Friends/Family
- [ ] Dark Mode 😄

---

## Definition of Done
- Öffentliche, optisch ansprechende Projektübersicht
- Schnelle Suche inkl. PDF-Volltext
- Anleitungen sicher nur für autorisierte Nutzer
- Komplett selfhosted, dokumentiert, wartbar
