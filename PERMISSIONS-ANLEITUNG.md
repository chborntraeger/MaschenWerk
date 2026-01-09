# 🎯 Permissions-Konfiguration - Schritt-für-Schritt

## ✅ Was bereits funktioniert:

- **Public Access**: Kann öffentliche Projects sehen ✓
- **Rollen erstellt**: Friends & Family, Worker ✓  
- **Testnutzer**: `test@familie.de` ✓

## 🔧 Was du jetzt in Directus UI machen musst:

### 1. Öffne Directus

👉 **http://localhost:8055**  
Login: `admin@example.com` / `ChangeMe123!`

---

### 2. Friends & Family Permissions

1. Klicke links auf **Settings** (Zahnrad)
2. **Access Control** → **Policies & Permissions**
3. **Create Policy** Button
   - Name: `Friends & Family Policy`
   - Icon: 👥 group
   - Admin Access: ❌ **NEIN**
   - App Access: ✅ **JA**
   - Roles: Wähle **Friends & Family** aus

4. Speichern → Policy öffnet sich

5. **Add Permission** für jede Collection:

#### **projects**
- Action: **Read**
- Item Permissions: **Use Custom**
  ```json
  {
    "status": {
      "_in": ["public", "private"]
    }
  }
  ```
- Field Permissions: **All fields EXCEPT**:
  - ❌ private_notes (abwählen!)

#### **patterns**
- Action: **Read**
- Item Permissions: **Use Custom**
  ```json
  {
    "visibility": {
      "_in": ["friends_family", "private"]
    }
  }
  ```
- Field Permissions: **All fields**

#### **tags**
- Action: **Read**
- Item Permissions: **All Access**
- Field Permissions: **All fields**

#### **project_images**
- Action: **Read**
- Item Permissions: **All Access**
- Field Permissions: **All fields**

#### **directus_files**
- Action: **Read**
- Item Permissions: **All Access**
- Field Permissions: **All fields**

---

### 3. Worker Permissions

1. **Create Policy**
   - Name: `Worker Policy`
   - Icon: ⚙️ settings
   - Admin Access: ❌ NEIN
   - App Access: ❌ NEIN
   - Roles: Wähle **Worker** aus

2. **Add Permission**:

#### **patterns**
- Action: **Read**
- Item Permissions: **All Access**
- Field Permissions: **All fields**

#### **directus_files**
- Action: **Read**
- Item Permissions: **All Access**
- Field Permissions: **All fields**

---

### 4. Worker Static Token erstellen

1. **Settings** → **Access Control** → **Users**
2. Finde **PDF Worker** User
3. Tab **Tokens**
4. **Create Token**
   - Name: `PDF Worker Token`
   - Expiration: **Never**
5. **KOPIERE DEN TOKEN!** (nur einmal sichtbar)
6. Terminal:
   ```bash
   echo 'WORKER_TOKEN=dein_kopierter_token_hier' >> .env
   ```

---

## ✅ Test durchführen

```bash
python3 test-api.py
```

**Erwartetes Ergebnis:**
```
📌 Public Access (ohne Login)
✅ 3 Projects sichtbar
   - Wintermütze mit Bommel (public)
   - Kuschel-Pullover (public)
   - Meine ersten Socken (public)
✅ Patterns korrekt geschützt (nicht sichtbar)

📌 Friends & Family Access
✅ Login erfolgreich
✅ 4 Projects sichtbar
✅ 2 Patterns sichtbar
   - Basis Socken Anleitung (friends_family)
   - Raglan-Pullover von oben (private)
```

---

## 🎉 Wenn alles funktioniert:

**Phase 2 ist abgeschlossen!** 🎊

Weiter zu **Phase 3: Next.js Frontend**

```bash
# Phase 3 starten
cd /Users/christina/_DEV/myKnittingProjects
# Next.js initialisieren (nächster Schritt)
```
