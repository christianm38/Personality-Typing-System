"""Main Streamlit Application Entry Point"""
import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Personality Typing System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1em;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# MAIN PAGE
# ============================================
st.markdown("<h1 class='main-header'>🧠 Personality Typing System</h1>", unsafe_allow_html=True)

st.markdown("""
Willkommen zum **Personality Typing System** – einem wissenschaftlich fundierten 
Persönlichkeits-Assessment mit Machine Learning!

---
""")

# Feature overview
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎓 Student Track
    
    **Discover your true personality and ideal career path**
    
    - Big Five Personality Assessment
    - Work Type & Social Type Classification
    - Functional Archetype Matching
    - ML-powered Job Recommendations
    - Perfect for students and career changers
    
    **Start →** Use the **Student Assessment** page in the sidebar
    """)

with col2:
    st.markdown("""
    ### 🏢 Enterprise Track
    
    **Optimize teams and hiring**
    
    - Generate QR Codes for surveys
    - Analyze individual role fit
    - Assess team compatibility
    - ML-powered recommendations
    - Bulk survey management
    
    **Start →** Use the **QR Admin** page in the sidebar
    """)

st.markdown("---")

# Quick start
st.subheader("🚀 Quick Start")

with st.expander("1. How to use this system", expanded=True):
    st.markdown("""
    #### For Students:
    1. Ask for a Survey ID or QR Code
    2. Go to **Student Assessment** page
    3. Enter Survey ID
    4. Answer ~25 questions (5 minutes)
    5. Get instant results with job recommendations!
    
    #### For Administrators:
    1. Go to **QR Admin** page
    2. Generate QR Codes for surveys
    3. Distribute to students/employees
    4. Monitor completion rates
    5. Download and analyze results
    """)

with st.expander("2. What you'll get"):
    st.markdown("""
    ### Your Results Include:
    
    - **Big Five Scores** - Personality dimensions (1-5 scale)
    - **Work Type** - How you approach work (5 types)
    - **Social Type** - Your interaction style (4 types)
    - **Functional Archetype** - Your AI-era value (4 archetypes)
    - **Top 5 Job Matches** - ML-powered career recommendations
    - **Compatibility Insights** - For team building
    """)

with st.expander("3. The Science Behind"):
    st.markdown("""
    ### Personality Model
    
    This system uses a **3-layer personality model**:
    
    1. **Layer 1: Big Five Dimensions**
       - Openness, Conscientiousness, Extraversion, Agreeableness, Emotional Stability
       - 40+ years of psychological research
    
    2. **Layer 2: Work & Social Types**
       - 5 Work Types (Denker, Analytiker, Umsetzer, Organisateur, Verkäufer)
       - 4 Social Types (Moderator, Individualist, Partner, Beobachter)
       - 20 unique personality combinations
    
    3. **Layer 3: Functional Archetypes**
       - AI-era archetypes (Slop Cannon, Stitcher, Hot Person, Grown-Up)
       - Based on Yoav Rechtman's framework
    
    ### Machine Learning Features
    
    - **NLP Processing** - Analyzes open-ended responses
    - **Job Recommendation Engine** - Cosine similarity matching (10 jobs)
    - **Team Compatibility Analysis** - Diversity, balance, complementarity scoring
    - **Role Fit Prediction** - Success probability (10 roles)
    """)

st.markdown("---")

# System status
st.subheader("📊 System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("✅ **Core System** - Fully Operational")

with col2:
    st.success("✅ **ML Engines** - All 4 Engines Ready")

with col3:
    st.warning("⏳ **Reports** - PDF Export Coming Soon")

st.markdown("---")

# Navigation hint
st.markdown("""
### 📍 Navigation
Use the **sidebar menu** to access:
- **🎓 Student Assessment** - Take the personality test
- **🏢 QR Admin** - Create and manage surveys
- **Main** - This page

### 📚 Documentation
- [GitHub Repository](https://github.com/christianm38/personality-typing-system)
- [README with Full Documentation](https://github.com/christianm38/personality-typing-system/blob/main/README.md)
- [Deployment Guide](https://github.com/christianm38/personality-typing-system/blob/main/DEPLOYMENT.md)
""")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2em; padding: 2em; border-top: 1px solid #ddd;">
    <p><strong>Made with ❤️ for Career Development & Organizational Excellence</strong></p>
    <p><small>v1.0.0 - September 2024</small></p>
</div>
""", unsafe_allow_html=True)
