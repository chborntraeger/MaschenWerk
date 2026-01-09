# Worker Service - PDF Text Extraction

Der Worker-Service extrahiert automatisch Text aus PDF-Anleitungen und indexiert sie in Meilisearch für die Volltext-Suche.

## Features

- Automatische PDF-Text-Extraktion
- Zwei Extraktionsmethoden:
  - `pdftotext` (Poppler) - primär, beste Qualität
  - PyPDF2 - Fallback
- Indexierung in Meilisearch
- Polling-basiert (überprüft regelmäßig neue PDFs)

## Konfiguration

Über Environment-Variablen in `.env`:

```bash
DIRECTUS_URL=http://directus:8055
DIRECTUS_TOKEN=your_worker_static_token
MEILISEARCH_URL=http://meilisearch:7700
MEILISEARCH_KEY=your_meilisearch_key
POLL_INTERVAL=60  # Sekunden zwischen Checks
```

## Verwendung

### Mit Docker Compose (empfohlen)

```bash
# Worker mit allen anderen Services starten
docker compose --profile worker up -d

# Nur Worker starten (wenn andere Services bereits laufen)
docker compose up -d pdf_worker

# Logs ansehen
docker compose logs -f pdf_worker
```

### Lokal zum Testen

```bash
cd worker

# Dependencies installieren
pip3 install -r requirements.txt

# Poppler installieren (für pdftotext)
# macOS:
brew install poppler

# Linux:
sudo apt-get install poppler-utils

# Worker starten
python worker.py
```

## Workflow

1. Worker startet und verbindet sich mit Directus und Meilisearch
2. Erstellt Meilisearch Index `patterns_index` (falls nicht vorhanden)
3. Alle 60 Sekunden (konfigurierbar):
   - Fragt Directus nach allen Patterns mit PDF-Dateien
   - Lädt PDFs herunter
   - Extrahiert Text
   - Indexiert in Meilisearch

## Meilisearch Index Schema

```javascript
{
  "id": "uuid",
  "title": "string",
  "slug": "string",
  "visibility": "friends_family | private",
  "notes": "string",
  "pdf_text": "string",  // Extrahierter Text
  "date_created": "timestamp",
  "date_updated": "timestamp"
}
```

### Searchable Attributes
- `title`
- `notes`
- `tags`
- `pdf_text`

### Filterable Attributes
- `visibility`
- `date_created`

## Zukünftige Verbesserungen

- [ ] Webhook-basiert statt Polling (Directus Flow Trigger)
- [ ] Incremental Updates (nur geänderte PDFs neu indexieren)
- [ ] Better error handling und retry logic
- [ ] Metrics & Monitoring
- [ ] Apache Tika als dritte Extraktionsmethode
- [ ] OCR für gescannte PDFs (Tesseract)
