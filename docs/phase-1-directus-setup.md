# Phase 1: Directus Collections & Datenmodell

## Übersicht

In dieser Phase richten wir die Datenstrukturen in Directus ein:
- Collection für Strickprojekte
- Collection für Anleitungen (Patterns)
- Collection für Tags
- Verknüpfungen (Junctions) für Bilder und Pattern-Zuordnung

## Voraussetzungen

- Directus läuft unter http://localhost:8055
- Admin-Login funktioniert

## 1. Collection `projects` erstellen

### Über Directus UI:

1. **Settings** → **Data Model** → **Create Collection**
2. Name: `projects`
3. Icon: 🧶 (optional)
4. Singleton: Nein

### Felder hinzufügen:

| Feld | Type | Interface | Optionen |
|------|------|-----------|----------|
| `id` | UUID | Input (readonly) | Auto-generiert, Primary Key |
| `status` | String | Dropdown | Choices: `draft`, `public`, `private` |
| `title` | String | Input | Required, max 255 |
| `slug` | String | Input | Required, Unique, URL-safe |
| `description` | Text | WYSIWYG / Markdown | Rich Text Editor |
| `finished_at` | Date | Date/Time | Nullable |
| `hero_image` | File | Image | Many-to-One zu `directus_files` |
| `private_notes` | Text | Textarea | Nur für Admins sichtbar |
| `date_created` | Timestamp | Datetime (readonly) | Auto |
| `date_updated` | Timestamp | Datetime (readonly) | Auto |

### Slug Auto-Generation (optional)

Für automatische Slug-Erstellung aus dem Titel:
- Gehe zu `slug` Feld → **Options**
- Aktiviere "Generate on create"
- Template: `{{title}}` (Directus macht automatisch URL-safe)

## 2. Collection `patterns` erstellen

1. **Settings** → **Data Model** → **Create Collection**
2. Name: `patterns`

### Felder:

| Feld | Type | Interface | Optionen |
|------|------|-----------|----------|
| `id` | UUID | Input (readonly) | Primary Key |
| `title` | String | Input | Required |
| `slug` | String | Input | Required, Unique |
| `visibility` | String | Dropdown | Choices: `friends_family`, `private` |
| `pdf_file` | File | File | Many-to-One zu `directus_files` |
| `notes` | Text | Textarea | Nullable |
| `date_created` | Timestamp | Datetime (readonly) | Auto |
| `date_updated` | Timestamp | Datetime (readonly) | Auto |

## 3. Collection `tags` erstellen

1. **Settings** → **Data Model** → **Create Collection**
2. Name: `tags`

### Felder:

| Feld | Type | Interface | Optionen |
|------|------|-----------|----------|
| `id` | Integer | Input (readonly) | Auto-increment, Primary Key |
| `name` | String | Input | Required, max 100 |
| `slug` | String | Input | Required, Unique |

## 4. Junction Table: `projects_tags` (Many-to-Many)

1. Gehe zu `projects` Collection
2. **Create Field** → **Many to Many (M2M)**
3. Related Collection: `tags`
4. Junction Collection: `projects_tags` (wird automatisch erstellt)

## 5. Junction Table: `project_images`

Für Galerie-Bilder mit Reihenfolge und Beschreibung.

1. **Create Collection**: `project_images`
2. **Hidden**: Ja (nur über Relation sichtbar)

### Felder:

| Feld | Type | Interface | Optionen |
|------|------|-----------|----------|
| `id` | Integer | Input (readonly) | Auto-increment |
| `project_id` | UUID | Input | Many-to-One zu `projects` |
| `directus_files_id` | UUID | Image | Many-to-One zu `directus_files` |
| `caption` | String | Input | Nullable, Bildbeschreibung |
| `sort` | Integer | Input | Für Reihenfolge |

3. Gehe zu `projects` Collection
4. **Create Field** → **One to Many (O2M)**
5. Related Collection: `project_images`
6. Foreign Key: `project_id`

## 6. Junction Table: `projects_patterns`

Verknüpfung zwischen Projekten und verwendeten Anleitungen.

1. **Create Collection**: `projects_patterns`
2. **Hidden**: Ja

### Felder:

| Feld | Type | Interface | Optionen |
|------|------|-----------|----------|
| `id` | Integer | Input (readonly) | Auto-increment |
| `projects_id` | UUID | Input | Many-to-One zu `projects` |
| `patterns_id` | UUID | Input | Many-to-One zu `patterns` |

3. Gehe zu `projects` Collection
4. **Create Field** → **Many to Many (M2M)**
5. Related Collection: `patterns`
6. Junction Collection: `projects_patterns`

## 7. Darstellungs-Optionen

### Projects Collection Layout

1. Gehe zu `projects` Collection
2. Klicke auf das Layout-Icon (oben rechts)
3. Wähle **Table** oder **Cards**
4. Für Cards: Display Template: `{{title}}`
5. Sortierung: `finished_at DESC` (neueste zuerst)

### Patterns Collection Layout

1. Display Template: `{{title}}`
2. Sortierung: `title ASC`

## 8. Validierung & Test

Teste die Collections durch Anlegen von Beispieldaten:

1. **Erstelle Tags**:
   - Name: "Socken", Slug: "socken"
   - Name: "Pullover", Slug: "pullover"
   - Name: "Anfänger", Slug: "anfaenger"

2. **Erstelle ein Test-Projekt**:
   - Title: "Meine ersten Socken"
   - Slug: "meine-ersten-socken"
   - Status: "public"
   - Description: "Ein einfaches Sockenprojekt..."
   - Finished: 2026-01-01
   - Tags: Socken, Anfänger

3. **Erstelle eine Test-Anleitung**:
   - Title: "Basis Socken Anleitung"
   - Slug: "basis-socken"
   - Visibility: "friends_family"
   - PDF: (lade eine Test-PDF hoch)

## ✅ Checkliste Phase 1

- [ ] Collection `projects` mit allen Feldern erstellt
- [ ] Collection `patterns` mit allen Feldern erstellt
- [ ] Collection `tags` erstellt
- [ ] M2M Relation `projects` ↔ `tags` eingerichtet
- [ ] O2M Relation `projects` → `project_images` eingerichtet
- [ ] M2M Relation `projects` ↔ `patterns` eingerichtet
- [ ] Display Templates konfiguriert
- [ ] Test-Daten angelegt und verifiziert

## Nächste Schritte

→ **Phase 2**: Rollen & Rechte konfigurieren (`docs/phase-2-permissions.md`)
