# Quick Start Guide

Starten Sie in **5 Minuten**! 🚀

## Voraussetzungen

- Python 3.9+ installiert
- Git installiert
- ~500 MB Speicher frei

## Installation (5 Minuten)

### 1. Repository klonen

```bash
git clone https://github.com/christianm38/personality-typing-system.git
cd personality-typing-system
```

### 2. Virtual Environment erstellen

```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 4. Konfigurieren (Optional)

```bash
cp .env.example .env
# Bearbeite .env wenn nötig (für Development: default ok)
```

### 5. App starten

```bash
streamlit run app/main.py
```

Die App öffnet sich automatisch auf: **http://localhost:8501**

## Erste Schritte

### Student Mode testen

1. Klick auf "🎓 Student Assessment"
2. Fülle 25 Fragen aus (~8 Minuten)
3. Klick "Show Results"
4. Sehe dein Personality Profil

### Enterprise Mode testen

1. Klick auf "🏢 Enterprise Team"
2. Erstelle eine Test-Organisation
3. Lade Employee List hoch (CSV)
4. Generiere QR-Codes
5. Teile mit Team
6. Sehe Team-Analysen

## Datenbank initialisieren

```bash
python app/database/init_db.py
```

Das erstellt SQLite Datenbank (für Development). Für Production nutze PostgreSQL.

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Stelle sicher virtual environment aktiv ist
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Installiere dependencies erneut
pip install -r requirements.txt
```

### "StreamlitAPIException"
```bash
# Lösche Streamlit cache
rm -r ~/.streamlit/
# oder
rmdir /s %USERPROFILE%\.streamlit  # Windows

# Starte app erneut
streamlit run app/main.py --logger.level=debug
```

### Database Fehler
```bash
# Reset database
python -c "from app.database.connection import reset_db; reset_db()"
```

## Nächste Schritte

1. **Read:** [README.md](README.md) - Vollständige Dokumentation
2. **Deploy:** [DEPLOYMENT.md](DEPLOYMENT.md) - Production Setup
3. **Test:** [TESTING.md](TESTING.md) - QA Strategy
4. **Contribute:** [CONTRIBUTING.md](CONTRIBUTING.md) - How to Help

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_personality.py::test_big_five_scoring -v

# With coverage
pytest --cov=app tests/
```

## Useful Commands

```bash
# Code formatting
black app/

# Type checking
mypy app/

# Linting
flake8 app/

# Database backup (if using PostgreSQL)
pg_dump -U user -d personality_db > backup.sql

# View logs (Docker)
docker-compose logs app -f

# Stop Docker services
docker-compose down
```

## Key Files to Know

- `app/config.py` - Central Configuration
- `app/models/personality.py` - Personality Scoring Logic
- `app/models/archetype.py` - Functional Archetypes
- `app/main.py` - Streamlit Entry Point
- `app/pages/` - Streamlit Pages
- `app/database/models.py` - Database Schema

## Questions?

- Create an [Issue](https://github.com/christianm38/personality-typing-system/issues)
- Check [Documentation](docs/)
- Email: [your-email if available]

---

**Happy coding! 🎉**
