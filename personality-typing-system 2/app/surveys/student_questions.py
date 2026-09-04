"""
Student Survey Questions
Questions for Student/Career Discovery Mode
25 Items, ~8 Minutes
"""

STUDENT_QUESTIONS = {
    "part_a_big_five": [
        # ==================== OPENNESS (3 Items) ====================
        {
            "id": "O1",
            "dimension": "Openness",
            "category": "Offenheit für Neues",
            "question": "Ich probiere gerne neue Dinge aus und bin offen für ungewöhnliche Ideen.",
            "reverse": False
        },
        {
            "id": "O2",
            "dimension": "Openness",
            "category": "Offenheit für Neues",
            "question": "Ich stelle gerne philosophische Fragen und denke über 'Warum?' nach.",
            "reverse": False
        },
        {
            "id": "O3",
            "dimension": "Openness",
            "category": "Offenheit für Neues",
            "question": "Routine und Vorhersehbarkeit finde ich langweilig; ich brauche Vielfalt.",
            "reverse": False
        },
        
        # ==================== CONSCIENTIOUSNESS (3 Items) ====================
        {
            "id": "C1",
            "dimension": "Conscientiousness",
            "category": "Gewissenhaftigkeit",
            "question": "Ich plane Aufgaben gerne sorgfältig und halte Deadlines ein.",
            "reverse": False
        },
        {
            "id": "C2",
            "dimension": "Conscientiousness",
            "category": "Gewissenhaftigkeit",
            "question": "Detailorientierung ist eine meiner Stärken; ich merke schnell Fehler.",
            "reverse": False
        },
        {
            "id": "C3",
            "dimension": "Conscientiousness",
            "category": "Gewissenhaftigkeit",
            "question": "Ich bevorzuge klare Regeln und Struktur; Chaos stresst mich.",
            "reverse": False
        },
        
        # ==================== EXTRAVERSION (3 Items) ====================
        {
            "id": "E1",
            "dimension": "Extraversion",
            "category": "Extraversion",
            "question": "Ich gewinne Energie aus sozialen Situationen und Teamarbeit.",
            "reverse": False
        },
        {
            "id": "E2",
            "dimension": "Extraversion",
            "category": "Extraversion",
            "question": "Ich bin energiegeladen, dynamisch und mag Aktivität.",
            "reverse": False
        },
        {
            "id": "E3",
            "dimension": "Extraversion",
            "category": "Extraversion",
            "question": "Ich rede gerne vor Gruppen und bin selbstbewusst im Rampenlicht.",
            "reverse": False
        },
        
        # ==================== AGREEABLENESS (3 Items) ====================
        {
            "id": "A1",
            "dimension": "Agreeableness",
            "category": "Verträglichkeit",
            "question": "Mir ist wichtig, dass es allen im Team gut geht; Harmonie bedeutet mir viel.",
            "reverse": False
        },
        {
            "id": "A2",
            "dimension": "Agreeableness",
            "category": "Verträglichkeit",
            "question": "Ich bin empathisch und kann mich leicht in andere hineinversetzen.",
            "reverse": False
        },
        {
            "id": "A3",
            "dimension": "Agreeableness",
            "category": "Verträglichkeit",
            "question": "Ich vermeide Konflikte und bevorzuge kooperative Lösungen.",
            "reverse": False
        },
        
        # ==================== EMOTIONAL STABILITY (3 Items) ====================
        {
            "id": "ES1",
            "dimension": "Emotional Stability",
            "category": "Emotionale Stabilität",
            "question": "Ich bleibe unter Druck ruhig und gestresst mich nicht leicht.",
            "reverse": False
        },
        {
            "id": "ES2",
            "dimension": "Emotional Stability",
            "category": "Emotionale Stabilität",
            "question": "Kritik und Misserfolge entmutigen mich nicht; ich lerne daraus.",
            "reverse": False
        },
        {
            "id": "ES3",
            "dimension": "Emotional Stability",
            "category": "Emotionale Stabilität",
            "question": "Ich bin selbstbewusst und zweifle selten an meinen Fähigkeiten.",
            "reverse": False
        },
    ],
    
    "part_b_interests": [
        # ==================== OPEN-ENDED QUESTIONS ====================
        {
            "id": "INT1",
            "type": "open_ended",
            "category": "Aktivitäten & Erfüllung",
            "question": "Beschreib einen Tag in der Schule/Studium, an dem du sehr glücklich und energiegeladen warst. Was hast du gemacht? Mit wem? Warum hat es dir Spaß gemacht? (max 300 Zeichen)",
            "instruction": "Denk an ein Moment, wo du wirklich 'im Flow' warst."
        },
        {
            "id": "INT2",
            "type": "open_ended",
            "category": "Arbeitsumgebung",
            "question": "In welcher Umgebung / welchen Bedingungen arbeitest du am besten? (z.B. allein vs. Team, strukturiert vs. flexibel, kreativ vs. analytisch) (max 200 Zeichen)",
            "instruction": "Was bringt dich in deinen besten Zustand?"
        },
        {
            "id": "INT3",
            "type": "open_ended",
            "category": "Purpose & Mission",
            "question": "Gibt es ein Problem in der Welt / deiner Schule / deiner Stadt, das du gerne lösen würdest? (max 200 Zeichen)",
            "instruction": "Was würde dich antreiben?"
        },
        {
            "id": "INT4",
            "type": "multiple_choice",
            "category": "Teamwork",
            "question": "Mit welchen Arten von Menschen arbeite ich gerne zusammen? (max 3 auswählen)",
            "options": [
                "Menschen mit Visionen (denken groß, innovativ)",
                "Menschen, die organisieren (strukturiert, verlässlich)",
                "Menschen, die hacken (schnell umsetzen, pragmatisch)",
                "Menschen, die hinterfragen (kritisch, genau)",
                "Menschen mit Empathie (unterstützend, freundlich)",
                "Menschen, die führen (motivierend, selbstsicher)"
            ]
        },
    ],
    
    "part_c_metadata": [
        {
            "id": "META1",
            "type": "text",
            "section": "Über dich",
            "question": "Dein Vorname (optional)",
            "required": False
        },
        {
            "id": "META2",
            "type": "select",
            "section": "Über dich",
            "question": "Deine aktuelle Situation",
            "options": [
                "Schüler (Gymnasium, Grade 9-10)",
                "Schüler (Gymnasium, Grade 11-12)",
                "Schüler (Realschule/Mittelstufe)",
                "Schüler (Hauptschule/Sekundarstufe)",
                "Student (Bachelor 1-2 Semester)",
                "Student (Bachelor 3+ Semester)",
                "Student (Master)",
                "Ausbildung",
                "Sonstiges"
            ],
            "required": True
        },
        {
            "id": "META3",
            "type": "text",
            "section": "Über dich",
            "question": "Geplantes Studium / Ausbildung / Karriereziel (optional)",
            "placeholder": "z.B. Informatik, Maschinenbau, BWL...",
            "required": False
        },
    ]
}

# ==================== SCALE DEFINITION ====================

LIKERT_SCALE = {
    "labels": [
        "Stimme gar nicht zu",
        "Stimme nicht zu",
        "Neutral",
        "Stimme zu",
        "Stimme stark zu"
    ],
    "values": [1, 2, 3, 4, 5],
    "icons": ["☐", "☐", "◐", "☑", "☑"],
    "colors": ["#ff4444", "#ff9999", "#cccccc", "#99ff99", "#00cc00"]
}

# ==================== SURVEY METADATA ====================

SURVEY_METADATA = {
    "title": "🎓 Persönlichkeits-Assessment für Schüler & Studenten",
    "subtitle": "Finde heraus, wer du wirklich bist und wie du deine beste Version wirst",
    "duration_minutes": 8,
    "total_items": 25,
    "introduction": """
## Willkommen! 👋

Dieses Assessment hilft dir zu verstehen:
- **Wer du wirklich bist** - nicht nur deine Interessen, sondern deine Persönlichkeit
- **Welche Karrieren zu dir passen** - basierend auf deinem echten Profil
- **Wie du deine beste Version wirst** - personalisierte Entwicklungspläne
- **Mit wem du gerne zusammenarbeitest** - ideale Teams für dich

### Wichtig:
✅ **Es gibt keine "richtigen" Antworten** - Ehrlichkeit ist wichtig
✅ **Keine Bewertung** - Es geht um Selbsterkenntnis, nicht um Punkte
✅ **Schnell** - Nur 8 Minuten
✅ **Anonym** - Dein Name ist optional

Los geht's! 🚀
    """,
    "conclusion": """
## 🎉 Fertig!

Dein Assessment wurde berechnet. Klick auf "Show Results" um:
- Deinen Work Type zu sehen
- Deinen Social Type zu sehen
- Deine funktionale Archetype
- Empfohlene Karrieren
- Deine Development-Roadmap

Viel Erfolg auf deinem Weg! 🌟
    """
}

# ==================== HELPER FUNCTIONS ====================

def get_all_questions() -> list:
    """Get all questions in flat list"""
    all_qs = []
    for part in ["part_a_big_five", "part_b_interests", "part_c_metadata"]:
        all_qs.extend(STUDENT_QUESTIONS[part])
    return all_qs


def get_questions_by_dimension(dimension: str) -> list:
    """Get questions for specific Big Five dimension"""
    return [
        q for q in STUDENT_QUESTIONS["part_a_big_five"]
        if q.get("dimension") == dimension
    ]


def get_total_items() -> int:
    """Get total number of items"""
    return sum(len(STUDENT_QUESTIONS[part]) for part in STUDENT_QUESTIONS)


def get_likert_options() -> tuple:
    """Get Likert scale options"""
    return tuple(zip(
        LIKERT_SCALE["labels"],
        LIKERT_SCALE["values"],
        LIKERT_SCALE["icons"]
    ))
