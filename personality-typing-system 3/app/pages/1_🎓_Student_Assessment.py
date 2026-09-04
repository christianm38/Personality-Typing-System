"""Student Personality Assessment Page"""
import streamlit as st
import pandas as pd
from app.database.connection import SessionLocal
from app.database.crud import SurveyCRUD, PersonalityProfileCRUD
from app.surveys.student_questions import STUDENT_QUESTIONS
from app.models.personality import PersonalityTyping
from app.models.job_recommendations import JobRecommendationEngine
from app.utils.qrcode import QRCodeGenerator

st.set_page_config(
    page_title="Student Assessment",
    page_icon="🎓",
    layout="wide"
)

# ============================================
# URL Parameter Processing
# ============================================
query_params = st.query_params
survey_id_param = query_params.get("survey_id", None)

# ============================================
# SIDEBAR - Survey Selection
# ============================================
st.sidebar.title("📋 Survey-Zugang")
st.sidebar.markdown("---")

# Input field for survey ID
survey_id = st.sidebar.text_input(
    "Survey ID eingeben:",
    value=survey_id_param if survey_id_param else "",
    placeholder="Paste survey ID here..."
)

if not survey_id:
    st.info("ℹ️ Bitte Survey ID eingeben (aus QR-Code oder Email)")
    st.markdown("""
    ### 🚀 Wie funktioniert's?
    
    1. **Scan** den QR-Code
    2. **Gib** die Survey ID ein
    3. **Beantworte** ~25 Fragen (5 Minuten)
    4. **Erhalte** deine Ergebnisse + Job-Empfehlungen
    """)
    st.stop()

# Validate survey
db = SessionLocal()
survey = SurveyCRUD.get_survey(db, survey_id)

if not survey:
    st.sidebar.error("❌ Survey nicht gefunden!")
    st.error("Die Survey ID ist ungültig oder existiert nicht.")
    st.stop()

if survey.is_completed:
    st.sidebar.warning("⚠️ Diese Survey wurde bereits abgeschlossen!")
    # Show existing results
    profile = PersonalityProfileCRUD.get_profile_by_survey(db, survey_id)
    if profile:
        st.info("✅ Hier sind deine gespeicherten Ergebnisse:")
        
        # Display results
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Openness", f"{profile.openness:.2f}")
        with col2:
            st.metric("Conscientiousness", f"{profile.conscientiousness:.2f}")
        with col3:
            st.metric("Extraversion", f"{profile.extraversion:.2f}")
        with col4:
            st.metric("Agreeableness", f"{profile.agreeableness:.2f}")
        with col5:
            st.metric("Emotional Stability", f"{profile.emotional_stability:.2f}")
        
        st.subheader("💼 Work Type")
        st.success(f"{profile.work_type}")
        
        st.subheader("🎯 Archetype")
        st.success(f"{profile.primary_archetype}")
    db.close()
    st.stop()

st.sidebar.success(f"✅ Survey gefunden!")
st.sidebar.info(f"**ID:** `{survey_id[:8]}...`")

# ============================================
# MAIN - Assessment Form
# ============================================
st.title("🎓 Dein Persönlichkeits-Assessment")
st.markdown("Beantworte die folgenden Fragen ehrlich und spontan (~5 Minuten)")

# Get questions
big_five_questions = STUDENT_QUESTIONS.get('big_five', [])

if not big_five_questions:
    st.error("❌ Survey-Fragen konnten nicht geladen werden!")
    st.stop()

# Survey Form
st.subheader("Persönlichkeitsfragen (1-5 Skala)")
st.markdown("*1 = Stimme nicht zu | 5 = Stimme stark zu*")

responses = {}

with st.form("personality_form"):
    for i, question in enumerate(big_five_questions):
        col1, col2 = st.columns([3, 1])
        with col1:
            responses[question['id']] = st.slider(
                f"{i+1}. {question['text']}",
                1, 5,
                value=3,
                key=f"q_{question['id']}"
            )
    
    submitted = st.form_submit_button("✅ Ergebnisse berechnen!", use_container_width=True)

if submitted:
    # ============================================
    # CALCULATE PERSONALITY
    # ============================================
    with st.spinner("🔄 Analysiere deine Antworten..."):
        try:
            # Calculate Personality Scores
            typing = PersonalityTyping(responses)
            big_five = typing.calculate_big_five()
            work_type = typing.calculate_work_type()
            social_type = typing.calculate_social_type()
            archetype = typing.calculate_archetype()
            
            # Save to Database
            profile = PersonalityProfileCRUD.create_profile(
                db=db,
                survey_id=survey_id,
                scores=big_five.scores,
                work_type=work_type.type,
                social_type=social_type.type,
                archetype=archetype.name,
                user_id=survey.user_id
            )
            
            # Mark survey complete
            SurveyCRUD.mark_survey_complete(db, survey_id)
            db.close()
            
            st.success("✅ Assessment abgeschlossen!")
            
            # ============================================
            # RESULTS
            # ============================================
            st.markdown("---")
            
            # 1. Big Five Scores
            st.subheader("📊 Deine Big Five Scores")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("📖 Openness", f"{big_five.scores['O']:.2f}", "Kreativität")
            with col2:
                st.metric("✅ Conscientiousness", f"{big_five.scores['C']:.2f}", "Zuverlässigkeit")
            with col3:
                st.metric("🤝 Extraversion", f"{big_five.scores['E']:.2f}", "Geselligkeit")
            with col4:
                st.metric("💚 Agreeableness", f"{big_five.scores['A']:.2f}", "Verträglichkeit")
            with col5:
                st.metric("🧠 Emotional Stability", f"{big_five.scores['ES']:.2f}", "Stabilität")
            
            st.markdown("---")
            
            # 2. Work Type
            st.subheader("💼 Dein Work Type")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.info(f"""
                ### {work_type.type}
                
                **Konfidenz:** {work_type.confidence:.0%}
                
                {work_type.description}
                """)
            
            st.markdown("---")
            
            # 3. Social Type
            st.subheader("🤝 Dein Social Type")
            st.info(f"""
            ### {social_type.type}
            
            **Konfidenz:** {social_type.confidence:.0%}
            
            {social_type.description}
            """)
            
            st.markdown("---")
            
            # 4. Archetype
            st.subheader("🎯 Dein Functional Archetype")
            st.success(f"""
            ### {archetype.name}
            
            **Match Score:** {archetype.value:.0%}
            
            {archetype.description}
            
            **Stärken für die AI-Ära:**
            - {archetype.ai_strengths[0] if len(archetype.ai_strengths) > 0 else ''}
            - {archetype.ai_strengths[1] if len(archetype.ai_strengths) > 1 else ''}
            """)
            
            st.markdown("---")
            
            # 5. Job Recommendations (ML!)
            st.subheader("💡 Top 5 Karriere-Empfehlungen")
            st.markdown("*Basierend auf ML-Matching mit deinem Profil*")
            
            jobs = JobRecommendationEngine.get_top_jobs(
                big_five.scores,
                work_type.type,
                archetype.name,
                top_n=5
            )
            
            if jobs:
                for i, job in enumerate(jobs, 1):
                    with st.expander(
                        f"{i}. **{job['title']}** - {job['fit_score']:.0%} Match",
                        expanded=(i == 1)
                    ):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Fit Score", f"{job['fit_score']:.0%}")
                        with col2:
                            st.metric("Salary", job['salary_range'])
                        with col3:
                            st.metric("Growth", job['growth_rate'])
                        
                        st.write(f"**Description:** {job['description']}")
                        st.write(f"**Work-Life Balance:** {job['work_life_balance']}/10")
            else:
                st.warning("⚠️ Keine Job-Empfehlungen verfügbar")
            
            st.markdown("---")
            
            # 6. Summary Card
            st.subheader("📋 Dein Profil-Summary")
            
            summary = f"""
            | Kategorie | Ergebnis |
            |-----------|----------|
            | **Work Type** | {work_type.type} ({work_type.confidence:.0%}) |
            | **Social Type** | {social_type.type} ({social_type.confidence:.0%}) |
            | **Archetype** | {archetype.name} ({archetype.value:.0%}) |
            | **Top Job Match** | {jobs[0]['title'] if jobs else 'N/A'} ({jobs[0]['fit_score']:.0%}) |
            | **Openness** | {big_five.scores['O']:.2f}/5 |
            | **Conscientiousness** | {big_five.scores['C']:.2f}/5 |
            | **Extraversion** | {big_five.scores['E']:.2f}/5 |
            | **Agreeableness** | {big_five.scores['A']:.2f}/5 |
            | **Emotional Stability** | {big_five.scores['ES']:.2f}/5 |
            """
            
            st.markdown(summary)
            
            st.markdown("---")
            st.info("✅ Deine Ergebnisse wurden gespeichert. Du kannst diese Seite jederzeit mit derselben Survey ID wieder öffnen!")
            
        except Exception as e:
            st.error(f"❌ Fehler bei der Berechnung: {str(e)}")
            db.close()
