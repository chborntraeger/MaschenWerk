# 🚀 CI/CD Setup mit GitHub Actions

Diese Anleitung erklärt, wie du automatisches Bauen mit GitHub Actions einrichtest.

## Übersicht

Der Workflow [.github/workflows/build-and-deploy.yml](.github/workflows/build-and-deploy.yml):
1. **Baut** Frontend und Worker als Docker Images
2. **Pusht** sie zu GitHub Container Registry (ghcr.io)
3. **Watchtower** auf dem Server pulled und deployed automatisch neue Images

## Setup-Schritte

### 1. GitHub Packages aktivieren

Die Container Registry ist standardmäßig aktiviert. Stelle sicher, dass:
- Repository Settings → Actions → General → Workflow permissions: **Read and write permissions** aktiviert ist

### 3. Username in .env.production setzen

```bash
# In .env.production
GITHUB_USERNAME=dein-github-username
```

### 3. Images öffentlich machen (optional)

Damit der Server die Images ohne Login pullen kann:

1. Gehe zu github.com → dein Profil → Packages
2. Finde `maschenwerk-frontend` und `maschenwerk-worker`
3. Package settings → Change visibility → Public

**Oder** verwende GitHub Token auf dem Server (siehe unten).

### 4. Server mit Watchtower vorbereiten

Watchtower überwacht automatisch alle Container und updated sie, wenn neue Images verfügbar sind.

```bash
# Auf dem Server
cd /opt/maschenwerk

# .env.production mit GITHUB_USERNAME aktualisieren
nano .env.production

# Für private Images: Docker login einrichten
docker login ghcr.io -u DEIN-USERNAME -p DEIN-GITHUB-TOKEN
```

GitHub Token generieren:
- GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token mit `read:packages` Scope

Dein Watchtower sollte die Container überwachen. Typische Watchtower-Konfiguration:
```yaml
# In deinem Traefik/Watchtower docker-compose.yml
watchtower:
  image: containrrr/watchtower
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
    - ~/.docker/config.json:/config.json  # Für private registry auth
  environment:
    - WATCHTOWER_CLEANUP=true
    - WATCHTOWER_INCLUDE_STOPPED=true
    - WATCHTOWER_POLL_INTERVAL=300  # Alle 5 Minuten
```

## Workflow-Trigger

Der Workflow startet automatisch bei:
- **Push auf main Branch**
- **Manuell** via GitHub Actions Tab → "Build and Push Docker Images" → Run workflow

## Lokales Testen ohne GitHub Actions

Wenn du die Images lokal bauen möchtest:

```bash
# docker-compose.local.yml verwenden (erstelle es)
docker compose -f docker-compose.yml build
```

Oder Images manuell bauen und pushen:

```bash
# Login
docker login ghcr.io -u DEIN-USERNAME

# Frontend bauen
docker build -t ghcr.io/DEIN-USERNAME/maschenwerk-frontend:latest ./frontend
docker push ghcr.io/DEIN-USERNAME/maschenwerk-frontend:latest

# Worker bauen
docker build -t ghcr.io/DEIN-USERNAME/maschenwerk-worker:latest ./worker
docker push ghcr.io/DEIN-USERNAME/maschenwerk-worker:latest

# Auf Server deployen
```

Nach dem Push übernimmt Watchtower auf dem Server automatisch das Deployment.

## Manuelles Deployment

Falls du manuell deployen möchtest (z.B. bei Problemen mit Watchtower):

```bash
# Auf dem Server
cd /opt/maschenwerk
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker image prune -f

  3. deploy (nur bei main branch)
     - SSH zu Server
     - Pull neue Images
     - Container neu starten
     - Alte Images löschen
```

## Auto-Deploy deaktivieren

Falls du nicht automatisch deployen möchtest:

1. Entferne den `deploy` Job aus [build-and-deploy.yml](.github/workflows/build-and-deploy.yml)
2. Deploy manuell mit:
   ```bash
   ssh user@server "cd /opt/maschenwerk && docker compose -f docker-compose.prod.yml pull && docker compose -f docker-compose.prod.yml up -d"
   ```

## Troubleshooting

### "Permission denied" beim Push

```bWatchtower updated nicht

```bash
# Auf dem Server: Watchtower Logs prüfen
docker logs watchtower

# Manuell Images pullen
cd /opt/maschenwerk
docker compose -f docker-compose.prod.yml pull

# Prüfe ob neue Images da sind
docker images | grep maschenwerk
# Auf dem Server: Docker login
docker login ghcr.io -u DEIN-USERNAME -p DEIN-GITHUB-TOKEN

# Oder: Mache Package öffentlich
```

### Deployment schlägt fehl

```bash
# Prüfe SSH-Verbindung
ssh -i ~/.ssh/github_actions_key user@server

# Prüfe Pfad auf Server
ssh user@server "ls -la /opt/maschenwerk"
```

### Build-Cache löschen

```bash
# GitHub Actions → Actions → Caches → Delete all caches
```

## Image-Tags

Der Workflow erstellt folgende Tags:
- `latest` - Neuester Build vom main Branch
- `main-abc1234` - Spezifischer Commit SHA
- `main` - Branch-Name

Verwende `latest` für Production, spezifische SHAs für Rollbacks.

## Ressourcen

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
