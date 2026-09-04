"""
Main Streamlit Application
Entry point for the Personality Typing System
"""

import streamlit as st
import sys
from pathlib import Path

# Setup page configuration
st.set_page_config(
    page_title="Personality Typing System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings


# ==================== CSS STYLING ====================

st.markdown("""
<style>
    :root {
        --primary: #0066ff;
        --success: #00cc00;
        --warning: #ff9999;
        --error: #ff4444;
    }
    
    .main {
        padding-top: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 18px;
        padding: 10px 20px;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary);
        margin: 0.5rem 0;
    }
    
    .success-card {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--success);
    }
    
    .warning-card {
        background-color: #fff3e0;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--warning);
    }
    
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .section-title {
        color: var(--primary);
        border-bottom: 2px solid var(--primary);
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ==================== SESSION STATE INITIALIZATION ====================

if "user_type" not in st.session_state:
    st.session_state.user_type = None  # "student" or "enterprise"

if "survey_responses" not in st.session_state:
    st.session_state.survey_responses = {}

if "personality_profile" not in st.session_state:
    st.session_state.personality_profile = None


# ==================== SIDEBAR NAVIGATION ====================

st.sidebar.title("🧠 Personality Typing System")
st.sidebar.markdown(f"**Version:** {settings.APP_VERSION}")
st.sidebar.markdown("---")

# Navigation
nav_page = st.sidebar.radio(
    "Wähle deine Option:",
    ["🏠 Home", "🎓 Student Assessment", "🏢 Enterprise Team", "⚙️ Admin"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Quick info
with st.sidebar.expander("📚 Über dieses System"):
    st.markdown("""
    ### Personality Typing System
    
    Ein wissenschaftlich fundiertes System für:
    - **Schüler/Studenten:** Karriere-Discovery
    - **Unternehmen:** Team-Optimierung
    
    **Basis:**
    - Big Five Personality Model
    - Work/Social Type Classification
    - Functional Archetypes (AI-Era)
    """)

# Settings
with st.sidebar.expander("⚙️ Einstellungen"):
    debug_mode = st.checkbox("Debug Mode", value=settings.DEBUG)
    if debug_mode:
        st.caption("Debug mode enabled")


# ==================== PAGE ROUTING ====================

if nav_page == "🏠 Home":
    show_home_page()
    
elif nav_page == "🎓 Student Assessment":
    st.switch_page("pages/1_🎓_Student_Assessment.py")
    
elif nav_page == "🏢 Enterprise Team":
    st.switch_page("pages/2_🏢_Enterprise_Team.py")
    
elif nav_page == "⚙️ Admin":
    st.switch_page("pages/3_⚙️_Admin.py")


# ==================== HOME PAGE ====================

def show_home_page():
    """Display home page"""
    
    st.markdown("""
    <div class="header-container">
        <h1>🧠 Personality Typing System</h1>
        <p><em>Ein System für die AI-Ära</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Willkommen zu einem wissenschaftlich fundierten System für 
    **Persönlichkeitsentwicklung** und **Organisationsoptimierung**.
    """)
    
    st.markdown("---")
    
    # Two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        
        ### 🎓 Student / Career Discovery
        
        **Frage:** Wer bin ich und wie werde ich die beste Version meiner selbst?
        
        #### Für wen?
        - Schüler & Studenten
        - Menschen in Karriere-Übergang
        - Alle, die sich selbst besser verstehen wollen
        
        #### Was lernst du?
        ✅ Deine echte Persönlichkeit (nicht nur Interessen)
        ✅ Top 5 passende Karrieren
        ✅ Ideal Industries
        ✅ Skill Gaps & Development Plan
        ✅ Ideal Teammates
        
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎓 Zum Student Mode →", use_container_width=True, key="student_btn"):
            st.switch_page("pages/1_🎓_Student_Assessment.py")
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        
        ### 🏢 Enterprise / Team Optimization
        
        **Frage:** Wie strukturieren wir unsere Organisation optimal?
        
        #### Für wen?
        - HR Teams & Leadership
        - Managers & Operators
        - Organisationen in Transformation
        
        #### Was erfährst du?
        ✅ Sind Mitarbeiter in richtigen Rollen?
        ✅ Sind Teams optimal zusammengesetzt?
        ✅ Welche Archetypes brauchen wir?
        ✅ Restructuring Recommendations
        ✅ Talent Development Plans
        
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏢 Zum Enterprise Mode →", use_container_width=True, key="enterprise_btn"):
            st.switch_page("pages/2_🏢_Enterprise_Team.py")
    
    st.markdown("---")
    
    # Key Information
    st.markdown("### 🎯 Das System in 3 Schichten")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### Layer 1: Big Five
        
        Wissenschaftliche Basis
        - Openness
        - Conscientiousness
        - Extraversion
        - Agreeableness
        - Emotional Stability
        """)
    
    with col2:
        st.markdown("""
        #### Layer 2: Type Classification
        
        5 Work Types × 4 Social Types
        - **Work:** Denker, Analytiker, Umsetzer, Organisateur, Verkäufer
        - **Social:** Moderator, Individualist, Partner, Beobachter
        """)
    
    with col3:
        st.markdown("""
        #### Layer 3: Functional Archetypes
        
        Yoav Rechtman's AI-Era Framework
        - 🚀 Slop Cannon (Speed)
        - 🧵 Stitcher (Stability)
        - 🔥 Hot Person (Relations)
        - 🧑‍⚖️ Grown-Up (Governance)
        """)
    
    st.markdown("---")
    
    # Features
    with st.expander("✨ Features"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Student App:**
            - ✅ 18 Big Five Items + 4 Interest Questions
            - ✅ 8 Minuten Assessment
            - ✅ Instant Personality Report
            - ✅ Career Recommendations (Top 5)
            - ✅ Industry Analysis
            - ✅ Skill Gaps & Development Plan
            - ✅ PDF Export
            - ✅ Zero Account Required
            """)
        
        with col2:
            st.markdown("""
            **Enterprise App:**
            - ✅ Employee Personality Profiling
            - ✅ Individual Role Fit Analysis
            - ✅ Team Compatibility Matrix
            - ✅ Recruitment Gap Analysis
            - ✅ Organizational Optimization
            - ✅ Performance Prediction
            - ✅ Talent Development Plans
            - ✅ Admin Dashboard & Analytics
            """)
    
    st.markdown("---")
    
    # FAQ
    with st.expander("❓ Häufig gestellte Fragen"):
        st.markdown("""
        **Q: Wie lange dauert das Assessment?**
        - A: Student Mode ~8 Min, Enterprise ~12 Min
        
        **Q: Brauch ich einen Account?**
        - A: Student Mode: Nein! Enterprise Mode: Ja (HR/Admin)
        
        **Q: Wie genau ist das System?**
        - A: Big Five ist 40+ Jahre Forschung. Work/Social Types sind davon abgeleitet. Functional Archetypes sind modern (Yoav Rechtman Framework)
        
        **Q: Was passiert mit meinen Daten?**
        - A: Deine Daten sind sicher und verschlüsselt. Keine Weitergabe an Dritte.
        
        **Q: Kann ich PDF exportieren?**
        - A: Ja! Student Reports und Enterprise Reports können als PDF exportiert werden.
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>Made with ❤️ for Career Development & Organizational Excellence</p>
        <p><small>Version """ + settings.APP_VERSION + """ | MIT License</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show_home_page()
