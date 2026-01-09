# Phase 2: Rollen & Rechte

## Übersicht

In dieser Phase konfigurieren wir die Zugriffsrechte in Directus:
- **Public**: Anonyme Besucher (nur öffentliche Projekte)
- **Friends & Family**: Eingeloggte Nutzer (zusätzlich geschützte Anleitungen)
- **Admin**: Voller Zugriff auf alles

## Voraussetzungen

- Phase 1 abgeschlossen (alle Collections existieren)
- Directus Admin-Zugang

## 1. Rolle "Public" konfigurieren

Die Public-Rolle existiert bereits in Directus.

### Settings → Access Control → Public

#### Projects Collection

1. **Permissions** → `projects`
2. **Create**: ❌ Deaktiviert
3. **Read**: ✅ Aktiviert mit Filter
   - **Field Permissions**: Alle Felder AUSSER `private_notes`
   - **Item Permissions** → Custom Rule:
     ```json
     {
       "status": {
         "_eq": "public"
       }
     }
     ```
4. **Update**: ❌ Deaktiviert
5. **Delete**: ❌ Deaktiviert

#### Project Images

1. **Permissions** → `project_images`
2. **Read**: ✅ Aktiviert
   - **Item Permissions**: Custom Rule:
     ```json
     {
       "project_id": {
         "status": {
           "_eq": "public"
         }
       }
     }
     ```

#### Tags

1. **Permissions** → `tags`
2. **Read**: ✅ Aktiviert (alle Felder, keine Filter)

#### Files (Bilder)

1. **Permissions** → `directus_files`
2. **Read**: ✅ Aktiviert
   - Nur Bilder, die zu public projects gehören
   - Keine direkten PDF-Zugriffe!

#### Patterns

1. **Permissions** → `patterns`
2. **Read**: ❌ Komplett deaktiviert (Public sieht keine Anleitungen)

## 2. Rolle "Friends & Family" erstellen

### Settings → Access Control → Create Role

1. **Name**: `Friends & Family`
2. **Icon**: 👥
3. **Description**: "Eingeloggte Freunde und Familie - Zugriff auf geschützte Anleitungen"
4. **Admin Access**: ❌ Nein
5. **App Access**: ✅ Ja (optional, falls sie Directus-UI nutzen sollen)

### Permissions konfigurieren

#### Projects

- **Read**: ✅ Aktiviert mit Filter:
  ```json
  {
    "status": {
      "_in": ["public", "private"]
    }
  }
  ```
- **Field Permissions**: Alle Felder AUSSER `private_notes`

#### Patterns

- **Read**: ✅ Aktiviert mit Filter:
  ```json
  {
    "visibility": {
      "_in": ["friends_family", "private"]
    }
  }
  ```
- **Field Permissions**: Alle Felder

#### Files (für PDFs)

- **Read**: ✅ Aktiviert
  - Filter: Nur Files, die zu erlaubten Patterns gehören

#### Tags, Project Images

- **Read**: ✅ Aktiviert (alle)

## 3. Rolle "Worker" erstellen (für PDF Indexing)

### Settings → Access Control → Create Role

1. **Name**: `Worker`
2. **Description**: "Service Account für PDF-Indexierung"
3. **Admin Access**: ❌ Nein
4. **App Access**: ❌ Nein

### Permissions

#### Patterns

- **Read**: ✅ Alle Felder, kein Filter
- **Update**: ✅ Nur für Metadaten (z.B. last_indexed)

#### Files

- **Read**: ✅ Aktiviert

## 4. Static Token für Worker erstellen

1. **Settings** → **Access Control** → **Users**
2. **Create User**:
   - **First Name**: "PDF"
   - **Last Name**: "Worker"
   - **Email**: `worker@localhost` (muss nicht real sein)
   - **Password**: (generieren, aber wird nicht verwendet)
   - **Role**: `Worker`
   - **Status**: Active

3. **Static Token generieren**:
   - Gehe zum neu erstellten Worker-User
   - **Token** Tab → **Create Token**
   - Name: "PDF Worker Token"
   - **Kopiere den Token** und speichere ihn in `.env`:
     ```bash
     WORKER_TOKEN=dein_generierter_token_hier
     ```

## 5. Friends & Family Nutzer anlegen

### Testnutzer erstellen

1. **Settings** → **Access Control** → **Users**
2. **Create User**:
   - **First Name**: "Test"
   - **Last Name**: "Familie"
   - **Email**: `test@familie.de`
   - **Password**: `TestPass123!`
   - **Role**: `Friends & Family`
   - **Status**: Active

## 6. Testen der Permissions

### Test 1: Public API (ohne Auth)

```bash
# Sollte nur public projects zurückgeben
curl http://localhost:8055/items/projects

# Sollte KEINE patterns zurückgeben
curl http://localhost:8055/items/patterns
```

### Test 2: Friends & Family API

```bash
# Login
curl -X POST http://localhost:8055/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@familie.de",
    "password": "TestPass123!"
  }'

# Kopiere access_token aus der Antwort

# Patterns abrufen (sollte funktionieren)
curl http://localhost:8055/items/patterns \
  -H "Authorization: Bearer DEIN_ACCESS_TOKEN"
```

### Test 3: Worker Token

```bash
# Mit Static Token
curl http://localhost:8055/items/patterns \
  -H "Authorization: Bearer DEIN_WORKER_TOKEN"
```

## 7. Field-Level Security für private_notes

### Sicherstellen, dass private_notes wirklich privat bleiben

1. Gehe zu `projects` Collection
2. **Field** → `private_notes`
3. **Field Options** → **Interface Options**
4. **Note**: Nur für Admins sichtbar

### Public Role prüfen

- Gehe zu Public Permissions für `projects`
- Stelle sicher, dass `private_notes` in **Field Permissions** NICHT ausgewählt ist

## 8. Webhook-Permissions (für Worker)

Falls du Directus Flows für automatische PDF-Indexierung nutzen willst:

1. **Settings** → **Flows** → **Create Flow**
2. **Trigger**: "Item Update" auf `patterns` Collection
3. **Webhook** zu deinem Worker-Service
4. **Authentication**: Worker Static Token

## ✅ Checkliste Phase 2

- [ ] Public Role konfiguriert (nur public projects sichtbar)
- [ ] Friends & Family Role erstellt und konfiguriert
- [ ] Worker Role und User erstellt
- [ ] Static Token für Worker generiert und in .env gespeichert
- [ ] Testnutzer für Friends & Family angelegt
- [ ] API-Tests durchgeführt (Public, Friends, Worker)
- [ ] Field-Level Security für private_notes verifiziert
- [ ] PDFs sind NICHT direkt über Public erreichbar

## Sicherheits-Hinweise

- ⚠️ PDFs sollten NIEMALS über direkte Asset-URLs erreichbar sein für Public
- ⚠️ PDF-Auslieferung erfolgt über API-Route im Next.js Frontend (Phase 4)
- ⚠️ Worker-Token ist sensibel - nur in .env, nicht committen
- ⚠️ Regelmäßig prüfen, ob Permission-Regeln noch korrekt sind

## Nächste Schritte

→ **Phase 3**: Next.js Frontend entwickeln (`docs/phase-3-frontend.md`)
