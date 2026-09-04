# 🚀 Quick Start Guide - Live Demo in 5 Minutes

## Prerequisites

```bash
# Python 3.9 or higher
python --version
```

## Installation

```bash
# 1. Clone repository
git clone https://github.com/christianm38/personality-typing-system.git
cd personality-typing-system

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python app/database/init_db.py

# 5. Run Streamlit app
streamlit run app/main.py
```

## What to Do First

The app will open in your browser at **http://localhost:8501**

### 🎓 Try Student Assessment:

1. Go to the **🏢 Enterprise QR Admin** page (sidebar)
2. Click **"📊 Batch erstellen"** button
3. Set count to **5**
4. Click the button to generate QR codes
5. Copy the **Survey ID** from the table
6. Go to **🎓 Student Assessment** page
7. Paste the Survey ID
8. Answer ~25 questions
9. **See instant results** with:
   - Big Five personality scores
   - Work Type & Social Type
   - Functional Archetype
   - **Top 5 ML-powered job recommendations** ✨

### 🏢 Try QR Admin:

1. Go to **🏢 Enterprise QR Admin** page
2. **Single QR:** Click to create one survey + see QR code
3. **Bulk QR:** Generate 20+ codes at once
4. Download as **CSV** or **ZIP** (with images)
5. Check **Dashboard** tab for analytics

## 🐳 Docker Alternative

```bash
# Build and run with Docker
docker-compose up --build

# App on http://localhost:8501
```

## 🚀 Deploy to Render.com (Free)

### 1. Push to GitHub

```bash
git add .
git commit -m "v1.0.0 Demo Ready"
git push origin main
```

### 2. Create Render.com Account
- Go to https://render.com
- Sign up (free)

### 3. Create New Web Service
- Connect GitHub repo
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app/main.py`
- Set environment:
  ```
  STREAMLIT_SERVER_PORT=10000
  STREAMLIT_SERVER_ADDRESS=0.0.0.0
  ```

### 4. Deploy
- Click "Create Web Service"
- Wait ~2 minutes
- Get your live URL!

## 📊 What's Included

✅ **Personality Models**
- Big Five (O, C, E, A, ES)
- 5 Work Types
- 4 Social Types
- 4 Functional Archetypes

✅ **Machine Learning**
- NLP text analysis
- Job recommendations (10 jobs)
- Team compatibility scoring
- Role fit prediction

✅ **Streamlit Pages**
- Student assessment (200 lines)
- QR admin dashboard (400 lines)
- Database persistence

✅ **Data Export**
- CSV download (Survey IDs)
- ZIP download (QR images)
- Results analytics

## 🐛 Troubleshooting

### Port already in use
```bash
streamlit run app/main.py --server.port 8502
```

### Database not found
```bash
python app/database/init_db.py
```

### Missing dependencies
```bash
pip install -r requirements.txt --upgrade
```

### On Windows: Missing "venv" command
```bash
python -m venv venv
```

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- See [ML_FEATURES.md](ML_FEATURES.md) for ML engine details

## 💡 Demo Ideas

**For Students:**
- Use your own personality
- See your top job matches
- Compare with friends

**For Schools:**
- Generate 100 QR codes
- Distribute to class
- Analyze student profiles

**For Companies:**
- Test team composition
- Predict role fit
- Find ideal hires

---

**Happy Testing! 🎉**

Questions? Check the [GitHub Issues](https://github.com/christianm38/personality-typing-system/issues)
