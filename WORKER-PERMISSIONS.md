# Worker Permissions Konfiguration

## Problem
Der PDF Worker läuft, bekommt aber **403 Forbidden** beim Zugriff auf Patterns.

## Lösung: Worker Policy in Directus UI konfigurieren

### Schritt-für-Schritt Anleitung:

1. **Directus öffnen**
   - http://localhost:8055
   - Login: admin@example.com / ChangeMe123!

2. **Settings → Access Control → Policies**

3. **Worker Policy erstellen oder bearbeiten**
   - Falls nicht vorhanden: "Create Policy"
   - Name: **"Worker Policy"**
   - Icon: 🤖 oder ⚙️

4. **Permissions hinzufügen für "patterns" Collection:**
   
   **Read Permission:**
   - Collection: `patterns`
   - Action: ✅ **Read**
   - Fields: Alle auswählen oder mindestens:
     - `id`
     - `title`
     - `slug`
     - `visibility`
     - `notes`
     - `pdf_file`
     - `date_updated`
   - Permissions: `All Items` (keine Filter)

5. **Permissions hinzufügen für "directus_files" Collection:**
   
   **Read Permission:**
   - Collection: `directus_files`
   - Action: ✅ **Read**
   - Fields: Alle auswählen
   - Permissions: `All Items`

6. **Policy der Worker Role zuweisen**
   - Settings → Access Control → Roles
   - Finde "Worker" Role
   - Klicke darauf
   - Im Tab "Policies": Füge "Worker Policy" hinzu

7. **Worker Container neu starten**
   ```bash
   docker compose restart pdf_worker
   ```

8. **Logs überprüfen**
   ```bash
   docker compose logs pdf_worker -f
   ```

## Erwartetes Ergebnis

Nach korrekter Konfiguration sollte der Worker:
- ✅ Patterns abrufen können
- ✅ PDF-Dateien herunterladen
- ✅ Text extrahieren
- ✅ In Meilisearch indexieren

Logs sollten zeigen:
```
📄 Found X patterns with PDFs
📥 Processing: Pattern Name
✅ Indexed pattern: pattern-slug
```

## Troubleshooting

### Immer noch 403?
- Prüfe ob Policy wirklich der Worker Role zugewiesen ist
- Prüfe ob Read-Permission für beide Collections aktiviert ist
- Restart Worker nach jeder Änderung

### 401 Unauthorized?
- Token ist falsch oder abgelaufen
- Neuen Token in Directus UI erstellen
- In .env aktualisieren: `WORKER_TOKEN=<new-token>`
- Worker neu starten
