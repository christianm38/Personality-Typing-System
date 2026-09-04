# Deployment Guide

## Option 1: Cloud Deployment (Render + Supabase) - Empfohlen für Schulen ⭐

### Geschwindigkeit: 30-45 Minuten | Kosten: €0-10/Monat

**Warum diese Option?**
- ✅ Kostenlos oder sehr günstig
- ✅ Keine Systemadministration nötig
- ✅ Automatische Updates & Backups
- ✅ Global erreichbar
- ✅ Perfekt für Schulen & Startups

### Schritt 1: Supabase PostgreSQL Setup

1. **Supabase Account erstellen**
   - Gehe zu https://supabase.com
   - Sign up mit GitHub/Email
   - Create new project

2. **Projekt konfigurieren**
   ```
   Project Name: personality-typing
   Database Password: [Strong Password]
   Region: Europe (Frankfurt)
   ```

3. **Connection String kopieren**
   - In Supabase → Settings → Database → Connection Pooling
   - String sieht so aus: `postgresql://user:password@host:6543/postgres`

### Schritt 2: Render.com Deployment

1. **Render Account**
   - Gehe zu https://render.com
   - Sign up mit GitHub
   - Connect GitHub Repository

2. **Create New Web Service**
   - Connect to personality-typing-system repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app/main.py --server.port=10000`

3. **Environment Variables**
   ```
   DATABASE_URL=postgresql://user:password@host:6543/postgres
   DEBUG=False
   APP_ENV=production
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Warten auf Build (ca. 3-5 Minuten)
   - Deine App läuft dann auf: `https://personality-typing.onrender.com`

### Schritt 3: QR-Code Setup

1. In Render App → Settings → "URL"
2. Kopiere: `https://personality-typing.onrender.com`
3. Diese URL für QR-Codes verwenden

### Post-Deployment

```bash
# Initialize database
python app/database/init_db.py

# Test connection
python app/database/connection.py check_db_connection()
```

---

## Option 2: Docker Deployment (Local oder VPS)

### Geschwindigkeit: 15-20 Minuten | Kosten: €15-30/Monat (VPS)

**Für wen?**
- Kleine bis mittlere Unternehmen
- Möchte mehr Kontrolle
- Hat einen Server zur Verfügung

### Local Development

```bash
# 1. Docker Desktop installieren
# Mac: https://docs.docker.com/desktop/install/mac-install/
# Windows: https://docs.docker.com/desktop/install/windows-install/
# Linux: sudo apt-get install docker.io

# 2. Start Services
docker-compose up -d

# 3. Warte auf Database (ca. 30 Sekunden)
docker-compose ps

# 4. Initialize Database
docker-compose exec app python app/database/init_db.py

# 5. App ist bereit
# http://localhost:8501
```

### Production Deployment (Ubuntu VPS)

```bash
# 1. SSH in VPS
ssh root@your-vps-ip

# 2. Installiere Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 3. Klone Repository
cd /opt
git clone https://github.com/christianm38/personality-typing-system.git
cd personality-typing-system

# 4. Erstelle .env
cp .env.example .env
# Bearbeite .env mit Production-Werten

# 5. Start Services
docker-compose up -d

# 6. Nginx Reverse Proxy (optional)
# Siehe separate nginx-config.conf
```

### Nginx Configuration (Optional)

```nginx
server {
    listen 80;
    server_name personality-typing.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Option 3: Enterprise On-Premise

### Geschwindigkeit: 2-3 Tage | Kosten: Custom

**Für wen?**
- Große Unternehmen
- Strikte Daten-Residency Anforderungen
- Will maximale Kontrolle

### Anforderungen

- Ubuntu 20.04 LTS Server
- PostgreSQL 12+
- Docker & Docker Compose
- 4GB RAM minimum
- 20GB Storage minimum
- HTTPS/SSL Certificate

### Installation

```bash
# Siehe separate docs/ENTERPRISE_DEPLOYMENT.md
```

---

## Scaling & Monitoring

### Monitoring (Render)

- Render Dashboard → your-app → Logs
- Render Dashboard → Alerts konfigurieren

### Scaling

**Render:**
```
Settings → Instance Type → Upgrade
```

**Docker:**
```bash
# Update image
docker-compose up -d --build

# View logs
docker-compose logs app -f

# Database backup
docker-compose exec postgres pg_dump -U personality_user personality_db > backup.sql
```

---

## Troubleshooting

### Database Connection Failed

```bash
# 1. Check environment variable
echo $DATABASE_URL

# 2. Test connection
python -c "import sqlalchemy; sqlalchemy.create_engine('$DATABASE_URL')"

# 3. Check Supabase status
# https://status.supabase.com
```

### App Crashes

```bash
# Docker logs
docker-compose logs app --tail=100

# Render logs
# https://dashboard.render.com → your-app → Logs
```

### Slow Performance

```bash
# Check database connection pooling
# .env: DB_POOL_SIZE=20

# Check Streamlit cache
# Streamlit → Settings → Clear Cache
```

---

## Cost Comparison

| Option | Database | Hosting | Monthly |
|--------|----------|---------|---------|
| Cloud (Render) | Supabase Free | Render Free | €0-10 |
| Cloud (Render) | Supabase Pro | Render Starter | €25-40 |
| Docker (Local) | SQLite | N/A | €0 |
| Docker (VPS) | PostgreSQL | DigitalOcean | €12-48 |
| Enterprise | PostgreSQL | On-Premise | €100+ |

---

## Next Steps

1. **Schulen:** Wähle Option 1 (Cloud)
2. **Startups:** Wähle Option 1 oder 2 (Docker Local)
3. **Unternehmen:** Wähle Option 2 oder 3 (Docker VPS oder On-Premise)

Fragen? Erstelle ein GitHub Issue oder kontaktiere den Autor.
