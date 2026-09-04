"""
Enterprise Survey Questions
Questions for Employee Personality Assessment & Team Analysis
50 Items, ~12 Minutes
"""

ENTERPRISE_QUESTIONS = {
    "part_a_big_five": [
        # ==================== OPENNESS (3 Items) ====================
        {
            "id": "O1",
            "dimension": "Openness",
            "category": "Offenheit für Neues",
            "question": "Ich bin offen für neue Technologien und Arbeitsmethoden, auch wenn sie außerhalb meiner Komfortzone liegen.",
            "reverse": False
        },
        {
            "id": "O2",
            "dimension": "Openness",
            "category": "Offenheit für Neues",
            "question": "Ich hinterfrage gerne Status Quo und denke über alternative Lösungen nach.",
            "reverse": False
        },
        {
            "id": "O3",
            "dimension": "Openness",
            "category": "Offenheit für Neues",
            "question": "Routine und repetitive Aufgaben demotivieren mich; ich brauche Herausforderung und Abwechslung.",
            "reverse": False
        },
        
        # ==================== CONSCIENTIOUSNESS (3 Items) ====================
        {
            "id": "C1",
            "dimension": "Conscientiousness",
            "category": "Gewissenhaftigkeit",
            "question": "Ich halte Deadlines ein und halte hohe Standards bei meiner Arbeit.",
            "reverse": False
        },
        {
            "id": "C2",
            "dimension": "Conscientiousness",
            "category": "Gewissenhaftigkeit",
            "question": "Detailorientierung ist eine meiner größten Stärken; Fehler fallen mir schnell auf.",
            "reverse": False
        },
        {
            "id": "C3",
            "dimension": "Conscientiousness",
            "category": "Gewissenhaftigkeit",
            "question": "Ich bevorzuge klare Prozesse und Verantwortlichkeiten; Unklarheit stresst mich.",
            "reverse": False
        },
        
        # ==================== EXTRAVERSION (3 Items) ====================
        {
            "id": "E1",
            "dimension": "Extraversion",
            "category": "Extraversion",
            "question": "Ich ziehe Energie aus Zusammenarbeit und Interaktion mit Kollegen.",
            "reverse": False
        },
        {
            "id": "E2",
            "dimension": "Extraversion",
            "category": "Extraversion",
            "question": "Ich bin energiegeladen, mag schnelle Entscheidungen und bin immer in Bewegung.",
            "reverse": False
        },
        {
            "id": "E3",
            "dimension": "Extraversion",
            "category": "Extraversion",
            "question": "Ich bin gerne präsent in Meetings, präsentiere gerne und bin sichtbar im Team.",
            "reverse": False
        },
        
        # ==================== AGREEABLENESS (3 Items) ====================
        {
            "id": "A1",
            "dimension": "Agreeableness",
            "category": "Verträglichkeit",
            "question": "Das Wohlbefinden meines Teams ist mir wichtig; ich unterstütze Kollegen gerne.",
            "reverse": False
        },
        {
            "id": "A2",
            "dimension": "Agreeableness",
            "category": "Verträglichkeit",
            "question": "Ich bin empathisch und kann mich gut in die Perspektive anderer hineinversetzen.",
            "reverse": False
        },
        {
            "id": "A3",
            "dimension": "Agreeableness",
            "category": "Verträglichkeit",
            "question": "Bei Konflikten suche ich Harmonie und kooperative Lösungen (statt Konfrontation).",
            "reverse": False
        },
        
        # ==================== EMOTIONAL STABILITY (3 Items) ====================
        {
            "id": "ES1",
            "dimension": "Emotional Stability",
            "category": "Emotionale Stabilität",
            "question": "Unter Druck bleibe ich ruhig und gelassen; ich handle strukturiert statt emotional.",
            "reverse": False
        },
        {
            "id": "ES2",
            "dimension": "Emotional Stability",
            "category": "Emotionale Stabilität",
            "question": "Kritik und Misserfolge motivieren mich zum Lernen, anstatt mich zu entmutigen.",
            "reverse": False
        },
        {
            "id": "ES3",
            "dimension": "Emotional Stability",
            "category": "Emotionale Stabilität",
            "question": "Ich bin selbstbewusst bezüglich meiner Fähigkeiten und meinem Wert.",
            "reverse": False
        },
    ],
    
    "part_b_current_role": [
        # ==================== CURRENT ROLE (10 Items) ====================
        {
            "id": "ROLE1",
            "type": "text",
            "category": "Aktuelle Rolle",
            "question": "Dein aktueller Job Title",
            "required": True
        },
        {
            "id": "ROLE2",
            "type": "select",
            "category": "Aktuelle Rolle",
            "question": "Dein Departement / Team",
            "options": [
                "Engineering / Entwicklung",
                "Product / Produktmanagement",
                "Sales",
                "Customer Success / Support",
                "Marketing",
                "Operations / Infrastructure",
                "Finance / Accounting",
                "HR / People",
                "Legal / Compliance",
                "Executive / Management",
                "Sonstiges"
            ],
            "required": True
        },
        {
            "id": "ROLE3",
            "type": "select",
            "category": "Aktuelle Rolle",
            "question": "Deine Seniority",
            "options": [
                "Junior (0-2 Jahre Erfahrung)",
                "Mid-Level (2-5 Jahre)",
                "Senior (5-10 Jahre)",
                "Lead / Manager (10+ Jahre oder Leadership)",
                "Executive (C-Level, Director+)"
            ],
            "required": True
        },
        {
            "id": "ROLE4",
            "type": "scale",
            "category": "Aktuelle Rolle",
            "question": "Wie zufrieden bist du in deiner aktuellen Rolle? (1=sehr unzufrieden, 5=sehr zufrieden)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "ROLE5",
            "type": "scale",
            "category": "Aktuelle Rolle",
            "question": "Ich passe gut zu meiner aktuellen Rolle. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "ROLE6",
            "type": "scale",
            "category": "Aktuelle Rolle",
            "question": "Ich erbring gute Ergebnisse in meiner Rolle. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "ROLE7",
            "type": "select",
            "category": "Aktuelle Rolle",
            "question": "Meine ideale Arbeitsumgebung ist...",
            "options": [
                "Highly structured & predictable",
                "Structured but with flexibility",
                "Balanced (mix of structure & autonomy)",
                "Flexible & autonomous",
                "Chaotic & fast-moving (love the chaos)"
            ],
            "required": True
        },
        {
            "id": "ROLE8",
            "type": "scale",
            "category": "Aktuelle Rolle",
            "question": "Ich mag schnelle, iterative Arbeitsweisen (auch wenn nicht perfekt). (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "ROLE9",
            "type": "scale",
            "category": "Aktuelle Rolle",
            "question": "Mir ist tiefe, gründliche Arbeit wichtiger als schnelle Ergebnisse. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "ROLE10",
            "type": "multiple_choice",
            "category": "Aktuelle Rolle",
            "question": "Welche Arten von Aufgaben erfüllen dich am meisten? (max 3)",
            "options": [
                "Schnelle Umsetzung / Building (Slop Cannon-Energie)",
                "Systeme stabil & sicher halten (Stitcher-Energie)",
                "Menschen verbinden / Vertrauen aufbauen (Hot Person-Energie)",
                "Strategische Entscheidungen / Governance (Grown-Up-Energie)",
                "Etwas Neues erfinden (Innovation)",
                "Prozesse optimieren / Effizienz steigern"
            ],
            "required": True,
            "max_selections": 3
        },
    ],
    
    "part_c_skills": [
        # ==================== SKILLS & COMPETENCIES (7 Items) ====================
        {
            "id": "SKILL1",
            "type": "scale",
            "category": "Fähigkeiten",
            "question": "Meine technischen Fähigkeiten sind aktuell auf einem hohen Niveau. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": False,
            "context": "Nur relevant für technical roles"
        },
        {
            "id": "SKILL2",
            "type": "scale",
            "category": "Fähigkeiten",
            "question": "Ich bin schnell darin, mich in neue Technologien/Tools einzuarbeiten. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "SKILL3",
            "type": "scale",
            "category": "Fähigkeiten",
            "question": "Meine Kommunikationsfähigkeiten sind eine Stärke. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "SKILL4",
            "type": "scale",
            "category": "Fähigkeiten",
            "question": "Ich bin ein guter Mentor / ich kann anderen helfen zu wachsen. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "SKILL5",
            "type": "scale",
            "category": "Fähigkeiten",
            "question": "Ich bin gut darin, Systeme/Prozesse zu verstehen und zu verbessern. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "SKILL6",
            "type": "scale",
            "category": "Fähigkeiten",
            "question": "Ich bin belastbar und kann mit Ambiguität / Unsicherheit gut umgehen. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "SKILL7",
            "type": "multiple_choice",
            "category": "Fähigkeiten",
            "question": "In welchen Bereichen möchtest du dich entwickeln? (max 3)",
            "options": [
                "Technische Tiefe / Expertise",
                "Leadership & People Skills",
                "Strategic Thinking",
                "Business Acumen",
                "Sales / Stakeholder Management",
                "Innovation & Creativity",
                "Project Management",
                "Cross-functional Collaboration"
            ],
            "required": True,
            "max_selections": 3
        },
    ],
    
    "part_d_team": [
        # ==================== TEAM DYNAMICS (7 Items) ====================
        {
            "id": "TEAM1",
            "type": "scale",
            "category": "Team & Zusammenarbeit",
            "question": "Ich arbeite gerne in meinem aktuellen Team zusammen. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "TEAM2",
            "type": "scale",
            "category": "Team & Zusammenarbeit",
            "question": "Mein Team hat die richtige Vielfalt (unterschiedliche Persönlichkeiten/Perspektiven). (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "TEAM3",
            "type": "select",
            "category": "Team & Zusammenarbeit",
            "question": "Mein bevorzugter Kollaborations-Stil ist...",
            "options": [
                "Synchron (Meetings, Real-time Collaboration)",
                "Asynchron (schriftliche Dokumentation, Autonomie)",
                "Hybrid (Mix aus beiden)",
                "Flexibel je nach Situation"
            ],
            "required": True
        },
        {
            "id": "TEAM4",
            "type": "scale",
            "category": "Team & Zusammenarbeit",
            "question": "Ich bin ein guter Team Player und kann meine Agenda zurückstellen für Team-Ziele. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "TEAM5",
            "type": "scale",
            "category": "Team & Zusammenarbeit",
            "question": "Ich bin selbstständig und brauche wenig Oversight / Mikromanagement. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "TEAM6",
            "type": "scale",
            "category": "Team & Zusammenarbeit",
            "question": "Ich handle gerne Konflikte direkt an statt sie zu vermeiden. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
        {
            "id": "TEAM7",
            "type": "scale",
            "category": "Team & Zusammenarbeit",
            "question": "Ich könnte mir vorstellen, eine Führungsposition zu übernehmen. (1=stimme gar nicht zu, 5=stimme stark zu)",
            "scale_min": 1,
            "scale_max": 5,
            "required": True
        },
    ],
    
    "part_e_open_ended": [
        # ==================== OPEN-ENDED QUESTIONS (3 Items) ====================
        {
            "id": "OPEN1",
            "type": "open_ended",
            "category": "Erfahrungen & Feedback",
            "question": "Beschreib einen Tag oder ein Projekt, an dem du dich am engagiertesten und produktivsten gefühlt hast. Was hast du gemacht? Mit wem? Warum war es erfüllend? (max 400 Zeichen)",
            "instruction": "Denk an einen Peak-Performance Moment",
            "required": True
        },
        {
            "id": "OPEN2",
            "type": "open_ended",
            "category": "Erfahrungen & Feedback",
            "question": "Was frustriert dich am meisten in deinem aktuellen Job oder Team? (max 300 Zeichen)",
            "instruction": "Sei ehrlich - das hilft dir und dem Unternehmen",
            "required": True
        },
        {
            "id": "OPEN3",
            "type": "open_ended",
            "category": "Erfahrungen & Feedback",
            "question": "Welche Position oder Rolle würde dich reizen / wo siehst du dich in 3 Jahren? (max 300 Zeichen)",
            "instruction": "Deine Karriere-Vision",
            "required": False
        },
    ],
    
    "part_f_metadata": [
        # ==================== METADATA (2 Items) ====================
        {
            "id": "META1",
            "type": "text",
            "section": "Über dich",
            "question": "Dein Name",
            "required": True
        },
        {
            "id": "META2",
            "type": "text",
            "section": "Über dich",
            "question": "Name deines Managers / Lead (optional, für HR Analytics)",
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
}

# ==================== SURVEY METADATA ====================

SURVEY_METADATA = {
    "title": "🏢 Team Personality Assessment",
    "subtitle": "Verstehe deine Persönlichkeit und finde deinen Platz in der Organisation",
    "duration_minutes": 12,
    "total_items": 50,
    "introduction": """
## Willkommen zum Team Assessment! 👋

Dieses Assessment hilft deinem Unternehmen und dir zu verstehen:
- **Deine echte Persönlichkeit** - Work Type, Social Type, Functional Archetype
- **Passt deine Rolle zu dir?** - Individuelle Role-Fit Analyse
- **Wie ist dein Team zusammengesetzt?** - Team Diversity & Compatibility
- **Wo kannst du wachsen?** - Development Recommendations

### Wichtig:
✅ **Es gibt keine "richtigen" Antworten**
✅ **Vertraulich** - Deine Ergebnisse werden nur mit dir geteilt
✅ **Konstruktiv** - Ziel ist gegenseitliches Verständnis
✅ **Schnell** - Nur 12 Minuten

Los geht's! 🚀
    """,
    "conclusion": """
## ✅ Vielen Dank!

Dein Assessment wurde eingereicht. HR wird:
1. Individuelle Berichte generieren
2. Team-Analysen durchführen
3. Empfehlungen für Organisationsoptimierung erstellen

Du erhältst bald deinen persönlichen Report mit:
- Deinem Work/Social Type
- Funktionaler Archetype
- Feedback zu deiner Rolle-Fit
- Development Recommendations
- Ideal Teammates

Danke für deine Teilnahme! 🌟
    """
}

# ==================== HELPER FUNCTIONS ====================

def get_all_questions() -> list:
    """Get all questions in flat list"""
    all_qs = []
    for part in ["part_a_big_five", "part_b_current_role", "part_c_skills", 
                 "part_d_team", "part_e_open_ended", "part_f_metadata"]:
        all_qs.extend(ENTERPRISE_QUESTIONS[part])
    return all_qs


def get_questions_by_dimension(dimension: str) -> list:
    """Get questions for specific Big Five dimension"""
    return [
        q for q in ENTERPRISE_QUESTIONS["part_a_big_five"]
        if q.get("dimension") == dimension
    ]


def get_total_items() -> int:
    """Get total number of items"""
    return sum(len(ENTERPRISE_QUESTIONS[part]) for part in ENTERPRISE_QUESTIONS)


def get_likert_options() -> tuple:
    """Get Likert scale options"""
    return tuple(zip(LIKERT_SCALE["labels"], LIKERT_SCALE["values"]))
