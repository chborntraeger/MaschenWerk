# ✅ Phase 2 Setup - Erledigt!

## Was wurde erstellt:

### Rollen
- ✅ **Friends & Family** Role
  - ID: `76d42f41-37af-4e76-aa92-a163ced9e02a`
  - App Access: Ja
  
- ✅ **Worker** Role  
  - ID: `e7640f3b-012a-4c6c-ac5c-fd5933269daa`
  - Für PDF-Indexierung

### Benutzer
- ✅ **Testnutzer**: `test@familie.de` / `TestPass123!`
  - Rolle: Friends & Family
  
- ✅ **Worker User**: `worker@localhost`
  - Rolle: Worker
  - Für PDF-Indexierung

---

## 🎯 NÄCHSTER SCHRITT: Permissions in Directus UI konfigurieren

### 1. Öffne Directus Admin UI

👉 **http://localhost:8055**

Login: `admin@example.com` / `ChangeMe123!`

### 2. Konfiguriere Public Role Permissions

1. **Settings** (Zahnrad links) → **Access Control**
2. Klicke auf **Public** Role
3. Für **projects** Collection:
   - ✅ Aktiviere **Read**
   - Klicke auf das **Auge-Icon** (Customize Permissions)
   - **Item Permissions** → Custom:
     ```json
     {
       "status": {
         "_eq": "public"
       }
     }
     ```
   - **Field Permissions** → Wähle aus:
     - ✅ id, status, title, slug, description, finished_at, hero_image
     - ❌ **NICHT** private_notes!

4. Für **tags** Collection:
   - ✅ Aktiviere **Read**
   - Alle Felder erlauben

5. Für **project_images** Collection:
   - ✅ Aktiviere **Read**
   - Alle Felder erlauben

6. Für **directus_files** Collection:
   - ✅ Aktiviere **Read**
   - Alle Felder erlauben

7. **patterns** Collection:
   - ❌ Keine Permissions (Public sieht keine Anleitungen)

### 3. Konfiguriere Friends & Family Role Permissions

1. **Settings** → **Access Control**
2. Klicke auf **Friends & Family** Role
3. Für **projects** Collection:
   - ✅ Aktiviere **Read**
   - **Item Permissions** → Custom:
     ```json
     {
       "status": {
         "_in": ["public", "private"]
       }
     }
     ```
   - **Field Permissions** → Alle AUSSER private_notes

4. Für **patterns** Collection:
   - ✅ Aktiviere **Read**
   - **Item Permissions** → Custom:
     ```json
     {
       "visibility": {
         "_in": ["friends_family", "private"]
       }
     }
     ```
   - **Field Permissions** → Alle Felder

5. Für **tags, project_images, directus_files**:
   - ✅ Aktiviere **Read**, alle Felder

### 4. Konfiguriere Worker Role Permissions

1. **Settings** → **Access Control**
2. Klicke auf **Worker** Role
3. Für **patterns** Collection:
   - ✅ **Read** - alle Felder

4. Für **directus_files** Collection:
   - ✅ **Read** - alle Felder

### 5. Erstelle Worker Static Token

1. **Settings** → **Access Control** → **Users**
2. Klicke auf **PDF Worker** User
3. Tab **Tokens**
4. **Create Token**
   - Name: `PDF Worker Token`
5. **Kopiere den Token!**
6. Speichere in `.env`:
   ```bash
   WORKER_TOKEN=dein_kopierter_token_hier
   ```

---

## ✅ Test nach Konfiguration

Führe aus:

```bash
python3 test-api.py
```

**Erwartetes Ergebnis:**
- ✅ Public Access: Nur public projects sichtbar
- ✅ Public Access: Patterns nicht sichtbar
- ✅ Friends & Family: Alle projects und patterns sichtbar

---

## 📝 Phase 2 ist fertig, wenn:

- [ ] Public kann public projects lesen
- [ ] Public kann KEINE patterns lesen
- [ ] Friends & Family kann projects UND patterns lesen
- [ ] Worker hat Read-Zugriff auf patterns & files
- [ ] Worker Token ist erstellt und in .env gespeichert
- [ ] Test-API Script zeigt korrekte Ergebnisse

---

## 🎉 Danach: Phase 3 - Next.js Frontend

Siehe: `docs/phase-3-frontend.md`
