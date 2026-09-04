# Contributing Guide

Danke dass du das Projekt unterstützen willst! 🙏

## Code of Conduct

- Sei respektvoll
- Akzeptiere konstruktive Kritik
- Fokussier auf das was best ist für die Community

## Wie kann ich helfen?

### Bug Reports
1. Überprüfe ob der Bug already reported wurde
2. Erstelle ein Issue mit:
   - Detaillierter Beschreibung
   - Steps to reproduce
   - Expected vs Actual Behavior
   - Screenshots if helpful

### Feature Requests
1. Erstelle ein Issue mit `[FEATURE]` Prefix
2. Beschreibe den Use Case
3. Erkläre warum du das brauchst

### Code Contributions

1. **Fork the Repository**
```bash
git clone https://github.com/your-username/personality-typing-system.git
cd personality-typing-system
```

2. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Development Setup**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

4. **Make Changes**
- Folge PEP 8 Style Guide
- Schreib Tests für neue Features
- Update Dokumentation

5. **Test Locally**
```bash
# Unit Tests
pytest tests/

# Type Checking
mypy app/

# Linting
flake8 app/

# Format
black app/
```

6. **Commit & Push**
```bash
git add .
git commit -m "feat: description of your change"
git push origin feature/your-feature-name
```

7. **Create Pull Request**
- Link to related issues
- Describe changes clearly
- Request review

## Development Guidelines

### Code Style
- Python: PEP 8
- Use type hints
- Document complex functions
- Keep functions small and focused

### Testing
- Minimum 80% code coverage
- Write tests BEFORE code (TDD where possible)
- Test edge cases

### Commit Messages
```
feat: add new feature
fix: fix bug in xyz
docs: update README
style: format code
test: add test for xyz
refactor: reorganize module
```

### Documentation
- Update README if behavior changes
- Add docstrings to functions
- Update CHANGELOG.md

## Project Structure

```
app/
├── models/          # Business logic
├── database/        # Database layer
├── surveys/         # Survey definitions
├── reports/         # Report generation
├── pages/           # Streamlit pages
└── utils/           # Utilities
```

## Review Process

1. At least one maintainer review required
2. All tests must pass
3. Code coverage must not decrease
4. Documentation must be updated

## Questions?

- GitHub Issues for bug reports & features
- GitHub Discussions for questions (coming soon)
- Contact: [email if available]

## Recognition

Contributors will be listed in:
- README.md Contributors section
- GitHub Contributors page

## License

By contributing, you agree your code will be licensed under the MIT License.

---

Thank you for making this project better! ❤️
