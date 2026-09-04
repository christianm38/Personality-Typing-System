"""Enterprise QR Code Generator & Admin Dashboard"""
import streamlit as st
import pandas as pd
from datetime import datetime
from app.database.connection import SessionLocal
from app.database.crud import SurveyCRUD, PersonalityProfileCRUD
from app.utils.qrcode import QRCodeGenerator
import io

st.set_page_config(
    page_title="QR Admin Dashboard",
    page_icon="🏢",
    layout="wide"
)

st.title("🎯 QR Code Generator & Admin Dashboard")
st.markdown("Erstelle Survey QR-Codes und verwalte Umfragen")

db = SessionLocal()

# ============================================
# TABS
# ============================================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔄 QR Generator", "📈 Ergebnisse"])

# ============================================
# TAB 1: Dashboard
# ============================================
with tab1:
    st.subheader("Survey Übersicht")
    
    col1, col2, col3, col4 = st.columns(4)
    
    all_surveys = SurveyCRUD.get_all_surveys(db, limit=1000)
    completed = len([s for s in all_surveys if s.is_completed])
    pending = len([s for s in all_surveys if not s.is_completed])
    
    with col1:
        st.metric("📊 Total Surveys", len(all_surveys))
    with col2:
        st.metric("✅ Abgeschlossen", completed)
    with col3:
        st.metric("⏳ Ausstehend", pending)
    with col4:
        completion_rate = (completed / len(all_surveys) * 100) if all_surveys else 0
        st.metric("📈 Completion Rate", f"{completion_rate:.1f}%")
    
    st.markdown("---")
    
    # Recent surveys
    st.subheader("Aktuelle Surveys")
    if all_surveys:
        survey_data = []
        for survey in all_surveys[-10:]:
            survey_data.append({
                'Survey ID': survey.id[:8] + "...",
                'Type': survey.survey_type,
                'Status': '✅ Completed' if survey.is_completed else '⏳ Pending',
                'Created': survey.created_at.strftime("%Y-%m-%d %H:%M") if survey.created_at else 'N/A'
            })
        
        df_surveys = pd.DataFrame(survey_data)
        st.dataframe(df_surveys, use_container_width=True)
    else:
        st.info("ℹ️ Keine Surveys erstellt. Nutze 'QR Generator' um neue zu erstellen!")

# ============================================
# TAB 2: QR Generator
# ============================================
with tab2:
    st.subheader("Neue QR Codes generieren")
    
    # Section 1: Single Survey
    st.markdown("### 1️⃣ Einzelne Survey")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        survey_type = st.selectbox(
            "Survey Typ:",
            ["student", "enterprise"],
            key="single_type"
        )
    with col2:
        if st.button("🔄 Survey erstellen", key="single_create"):
            survey = SurveyCRUD.create_survey(db, survey_type)
            st.success(f"✅ Survey erstellt!")
            
            # Generate QR
            img_io, url = QRCodeGenerator.generate_qr_code(survey.id, survey_type)
            
            col_qr, col_info = st.columns([1, 2])
            
            with col_qr:
                st.image(img_io, caption="QR Code", width=250)
            
            with col_info:
                st.markdown(f"""
                **Survey ID:**
                ```
                {survey.id}
                ```
                
                **Access Link:**
                ```
                {url}
                ```
                """)
                
                # Copy buttons
                st.code(survey.id, language="text")
    
    st.markdown("---")
    
    # Section 2: Bulk QR Generation
    st.markdown("### 2️⃣ Bulk QR Codes (für Schulen/Unternehmen)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        count = st.number_input("Anzahl Surveys:", 1, 500, 20)
    
    with col2:
        survey_type_bulk = st.selectbox(
            "Survey Typ:",
            ["student", "enterprise"],
            key="bulk_type"
        )
    
    with col3:
        if st.button("📊 Batch erstellen", key="bulk_create", use_container_width=True):
            with st.spinner(f"Erstelle {count} QR-Codes..."):
                surveys = SurveyCRUD.create_bulk_surveys(db, count, survey_type_bulk)
                st.success(f"✅ {count} Surveys erstellt!")
                
                # Prepare data
                survey_data = []
                qr_images = []
                
                for survey in surveys:
                    img_io, url = QRCodeGenerator.generate_qr_code(survey.id, survey_type_bulk)
                    qr_images.append(img_io)
                    
                    survey_data.append({
                        'Survey ID': survey.id,
                        'Type': survey.survey_type,
                        'Status': 'Pending',
                        'Created': survey.created_at.strftime("%Y-%m-%d %H:%M") if survey.created_at else 'N/A'
                    })
                
                # Show table
                df = pd.DataFrame(survey_data)
                st.dataframe(df, use_container_width=True)
                
                # Download options
                st.markdown("---")
                st.subheader("📥 Download Options")
                
                # CSV Download
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📋 Download Survey IDs (CSV)",
                    data=csv,
                    file_name=f"survey_ids_{count}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
                # Generate and save QR images as zip
                import zipfile
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for i, (survey, img_io) in enumerate(zip(surveys, qr_images)):
                        zip_file.writestr(
                            f"survey_{survey.id[:8]}.png",
                            img_io.getvalue()
                        )
                
                zip_buffer.seek(0)
                
                st.download_button(
                    label="🖼️ Download QR Codes (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"qr_codes_{count}_{datetime.now().strftime('%Y%m%d')}.zip",
                    mime="application/zip"
                )

# ============================================
# TAB 3: Results & Analytics
# ============================================
with tab3:
    st.subheader("Ergebnisse & Analytics")
    
    # Get completed surveys
    completed_surveys = SurveyCRUD.get_completed_surveys(db)
    
    if not completed_surveys:
        st.info("ℹ️ Noch keine abgeschlossenen Surveys. Teile QR-Codes und warte auf Antworten!")
    else:
        st.success(f"✅ {len(completed_surveys)} Surveys abgeschlossen")
        
        st.markdown("---")
        
        # Results table
        st.subheader("Abgeschlossene Assessments")
        
        results_data = []
        for survey in completed_surveys:
            profile = PersonalityProfileCRUD.get_profile_by_survey(db, survey.id)
            if profile:
                results_data.append({
                    'Survey ID': survey.id[:8] + "...",
                    'Work Type': profile.work_type,
                    'Archetype': profile.primary_archetype,
                    'Openness': f"{profile.openness:.2f}",
                    'Conscientiousness': f"{profile.conscientiousness:.2f}",
                    'Extraversion': f"{profile.extraversion:.2f}",
                    'Agreeableness': f"{profile.agreeableness:.2f}",
                    'Emotional Stability': f"{profile.emotional_stability:.2f}",
                    'Completed': profile.created_at.strftime("%Y-%m-%d %H:%M") if profile.created_at else 'N/A'
                })
        
        if results_data:
            df_results = pd.DataFrame(results_data)
            st.dataframe(df_results, use_container_width=True)
            
            # Download results
            csv_results = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Download Results (CSV)",
                data=csv_results,
                file_name=f"assessment_results_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Analytics
            st.markdown("---")
            st.subheader("📊 Statistiken")
            
            # Work Type distribution
            work_types = {}
            for row in results_data:
                wt = row['Work Type']
                work_types[wt] = work_types.get(wt, 0) + 1
            
            if work_types:
                st.markdown("**Work Type Verteilung:**")
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.bar_chart(pd.Series(work_types))
                with col2:
                    for wt, count in work_types.items():
                        st.write(f"- {wt}: {count}")

db.close()

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
### 📚 Dokumentation
- [Deployment Guide](https://github.com/christianm38/personality-typing-system/blob/main/DEPLOYMENT.md)
- [GitHub Repository](https://github.com/christianm38/personality-typing-system)
""")
