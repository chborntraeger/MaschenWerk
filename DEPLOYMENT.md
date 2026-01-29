# 🚀 Deployment-Anleitung für MaschenWerk

Diese Anleitung zeigt dir, wie du MaschenWerk auf deinem Server mit Traefik deployst.

## Voraussetzungen

- Server mit Docker & Docker Compose
- Traefik läuft bereits und ist konfiguriert
- Domain mit DNS-Einträgen (siehe unten)
- SSH-Zugang zum Server

## 1. DNS-Einträge einrichten

Erstelle folgende A-Records für deine Domain:

```
maschenwerk.showcasehub.de     -> IP deines Servers
api.maschenwerk.showcasehub.de -> IP deines Servers
search.maschenwerk.showcasehub.de -> IP deines Servers
```

Oder verwende einen Wildcard-Record:
```
*.maschenwerk.showcasehub.de -> IP deines Servers
```

## 2. Traefik-Netzwerk prüfen

Stelle sicher, dass dein Traefik ein externes Netzwerk nutzt. In deiner bestehenden Traefik docker-compose.yml sollte stehen:

```yaml
networks:
  traefik_network:
    name: traefik_network
    driver: bridge
```

Falls es anders heißt, passe `docker-compose.prod.yml` entsprechend an.

## 3. Projekt auf den Server übertragen

```bash
# Auf deinem lokalen Rechner
cd /Users/christina/_DEV/MaschenWerk

# Repository zum Server pushen (oder via git clone)
rsync -avz --exclude 'node_modules' --exclude '.next' \
  ./ dein-user@dein-server:/opt/maschenwerk/
```

## 4. Environment-Variablen konfigurieren

```bash
# Auf dem Server
cd /opt/maschenwerk

# .env.production kopieren und anpassen
cp .env.production.example .env.production

# Bearbeite die Datei mit deinen Domains und generierten Secrets
nano .env.production
```

### Secrets generieren:

```bash
# Für DIRECTUS_KEY (32 Zeichen)
openssl rand -base64 32

# Für DIRECTUS_SECRET und NEXTAUTH_SECRET (64 Zeichen)
openssl rand -base64 64

# Für MEILISEARCH_MASTER_KEY (32 Zeichen)
openssl rand -base64 32

# Sichere Passwörter (20 Zeichen)
openssl rand -base64 20
```

## 5. Next.js für standalone output konfigurieren

Ergänze in `frontend/next.config.ts`:

```typescript
const nextConfig = {
  output: 'standalone', // Wichtig für Docker!
  // ... andere Konfiguration
};
```

## 6. Anwendung bauen und starten

```bash
# Auf dem Server
cd /opt/maschenwerk

# Docker Images bauen
docker compose -f docker-compose.prod.yml build

# Anwendung starten
docker compose -f docker-compose.prod.yml up -d

# Logs überwachen
docker compose -f docker-compose.prod.yml logs -f
```

## 7. Worker Token generieren

Nach dem ersten Start:

1. Gehe zu `https://api.maschenwerk.deine-domain.de/admin`
2. Login mit deinen ADMIN_EMAIL/ADMIN_PASSWORD Daten
3. Gehe zu Settings → Access Tokens
4. Erstelle einen Token mit Admin-Rechten
5. Kopiere den Token
6. Füge ihn in `.env.production` als `WORKER_TOKEN` ein
7. Worker neu starten:
   ```bash
   docker compose -f docker-compose.prod.yml restart pdf_worker
   ```

## 8. Directus Setup (einmalig)

Führe die Setup-Skripte aus (auf dem Server):

```bash
# Collections erstellen
docker compose -f docker-compose.prod.yml exec directus python3 /app/setup-collections.py

# Relationen einrichten
docker compose -f docker-compose.prod.yml exec directus python3 /app/setup-relations.py

# Permissions konfigurieren
docker compose -f docker-compose.prod.yml exec directus python3 /app/setup-permissions.py
```

Oder kopiere die Python-Skripte auf den Server und führe sie lokal aus.

## 9. Testen

Öffne folgende URLs im Browser:

- **Frontend**: https://maschenwerk.showcasehub.de
- **Directus Admin**: https://api.maschenwerk.showcasehub.de/admin
- **Meilisearch**: https://search.maschenwerk.showcasehub.de (mit API-Key)

## 10. Backup einrichten

Erstelle regelmäßige Backups der Docker Volumes:

```bash
# Backup-Skript erstellen
cat > /opt/maschenwerk/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/maschenwerk"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# PostgreSQL Backup
docker compose -f docker-compose.prod.yml exec -T postgres \
  pg_dump -U directus_prod directus_prod > "$BACKUP_DIR/db_$DATE.sql"

# Volume Backups
docker run --rm -v maschenwerk_directus_uploads:/data -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/uploads_$DATE.tar.gz -C /data .

# Alte Backups löschen (älter als 30 Tage)
find $BACKUP_DIR -type f -mtime +30 -delete
EOF

chmod +x /opt/maschenwerk/backup.sh

# Cronjob einrichten (täglich um 2 Uhr)
crontab -e
# Füge hinzu: 0 2 * * * /opt/maschenwerk/backup.sh
```

## Updates durchführen

```bash
cd /opt/maschenwerk

# Neueste Version ziehen (git pull oder rsync)
git pull

# Images neu bauen
docker compose -f docker-compose.prod.yml build

# Services neu starten (Zero-Downtime mit recreate)
docker compose -f docker-compose.prod.yml up -d

# Alte Images aufräumen
docker image prune -f
```

## Troubleshooting

### Logs anschauen
```bash
docker compose -f docker-compose.prod.yml logs -f [service-name]
```

### Container neu starten
```bash
docker compose -f docker-compose.prod.yml restart [service-name]
```

### In Container einloggen
```bash
docker compose -f docker-compose.prod.yml exec [service-name] sh
```

### SSL-Zertifikate prüfen
Traefik generiert automatisch Let's Encrypt Zertifikate. Prüfe Traefik-Logs:
```bash
docker logs traefik
```

## Sicherheitshinweise

- [ ] Ändere alle Default-Passwörter
- [ ] Nutze starke, zufällige Secrets
- [ ] Aktiviere Firewall (nur Port 80, 443, 22 öffnen)
- [ ] Richte automatische Updates ein
- [ ] Überwache Logs regelmäßig
- [ ] Teste Backups regelmäßig
- [ ] Beschränke Meilisearch-Zugriff über Traefik BasicAuth (optional)

## Konfigurierte Domain

Die Anwendung ist für `showcasehub.de` konfiguriert:
- Frontend: https://maschenwerk.showcasehub.de
- Directus API: https://api.maschenwerk.showcasehub.de
- Meilisearch: https://search.maschenwerk.showcasehub.de

## Ressourcen

- Traefik Docs: https://doc.traefik.io/traefik/
- Directus Docs: https://docs.directus.io/
- Next.js Deployment: https://nextjs.org/docs/deployment
