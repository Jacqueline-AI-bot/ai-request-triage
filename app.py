import json
import os
import re
from datetime import datetime
from typing import Dict, Any

import streamlit as st

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

APP_TITLE = "AI Request Triage Tool"

SYSTEM_PROMPT = """
Du bist ein AI Enablement Agent für interne Geschäftsprozesse.
Deine Aufgabe ist es, eingehende Anfragen zu analysieren, sinnvoll zu strukturieren
und einen pragmatischen nächsten Schritt vorzuschlagen.

Antworte ausschließlich als valides JSON mit folgender Struktur:
{
  "summary": "Kurze Zusammenfassung in einem Satz",
  "category": "Eine passende Kategorie",
  "priority": "hoch | mittel | niedrig",
  "urgency_score": 1-10,
  "business_problem": "Welches Geschäftsproblem steckt dahinter?",
  "recommended_next_steps": ["Schritt 1", "Schritt 2", "Schritt 3"],
  "draft_reply": "Kurzer professioneller Antwortvorschlag",
  "automation_potential": "niedrig | mittel | hoch",
  "suggested_workflow": "Wie könnte daraus ein wiederholbarer Workflow entstehen?"
}
"""


def fallback_rule_based_analysis(text: str) -> Dict[str, Any]:
    """Fallback ohne API-Key: einfache Regel-Logik für Demo-Zwecke."""
    lowered = text.lower()

    if any(word in lowered for word in ["dringend", "sofort", "heute", "problem", "fehler", "ausfall"]):
        priority = "hoch"
        score = 8
    elif any(word in lowered for word in ["bitte", "anfrage", "angebot", "beratung", "termin"]):
        priority = "mittel"
        score = 5
    else:
        priority = "niedrig"
        score = 3

    if any(word in lowered for word in ["angebot", "beratung", "kunde", "vertrieb"]):
        category = "Sales / Anfrage"
    elif any(word in lowered for word in ["fehler", "bug", "support", "funktioniert nicht"]):
        category = "Support / Problem"
    elif any(word in lowered for word in ["rechnung", "zahlung", "budget", "kosten"]):
        category = "Finance"
    elif any(word in lowered for word in ["bewerbung", "mitarbeiter", "onboarding", "hr"]):
        category = "HR / People"
    else:
        category = "Operations"

    return {
        "summary": "Die Anfrage wurde strukturiert analysiert und in einen nächsten Handlungsschritt übersetzt.",
        "category": category,
        "priority": priority,
        "urgency_score": score,
        "business_problem": "Unstrukturierte Anfrage mit Koordinations- oder Automatisierungsbedarf.",
        "recommended_next_steps": [
            "Anfrage fachlich prüfen und Verantwortlichkeit klären",
            "fehlende Informationen gezielt nachfordern",
            "bei wiederkehrendem Muster als potenziellen KI-Use-Case aufnehmen",
        ],
        "draft_reply": "Hallo, danke für die Anfrage. Ich schaue mir das Thema an und melde mich mit einem konkreten Vorschlag für die nächsten Schritte.",
        "automation_potential": "mittel",
        "suggested_workflow": "Eingehende Anfragen können automatisch kategorisiert, priorisiert und mit einem Antwortentwurf versehen werden.",
    }


def extract_json(raw: str) -> Dict[str, Any]:
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def analyze_with_openai(text: str, api_key: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    if OpenAI is None:
        raise RuntimeError("OpenAI package is not installed.")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    return extract_json(response.choices[0].message.content)


def render_result(result: Dict[str, Any]):
    col1, col2, col3 = st.columns(3)
    col1.metric("Priorität", result.get("priority", "-"))
    col2.metric("Dringlichkeit", result.get("urgency_score", "-"))
    col3.metric("Automation", result.get("automation_potential", "-"))

    st.subheader("Kurzfassung")
    st.write(result.get("summary", "-"))

    st.subheader("Kategorie")
    st.write(result.get("category", "-"))

    st.subheader("Geschäftsproblem")
    st.write(result.get("business_problem", "-"))

    st.subheader("Empfohlene nächste Schritte")
    steps = result.get("recommended_next_steps", [])
    if isinstance(steps, list):
        for step in steps:
            st.markdown(f"- {step}")
    else:
        st.write(steps)

    st.subheader("Antwortvorschlag")
    st.info(result.get("draft_reply", "-"))

    st.subheader("Vorschlag für Workflow")
    st.write(result.get("suggested_workflow", "-"))

    st.subheader("JSON Output")
    st.code(json.dumps(result, ensure_ascii=False, indent=2), language="json")


def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="🤖", layout="wide")
    st.title("🤖 AI Request Triage Tool")
    st.caption("Mini-MVP zur Analyse, Priorisierung und Strukturierung eingehender Geschäftsanforderungen.")

    with st.sidebar:
        st.header("Setup")
        st.write("Funktioniert auch ohne API-Key mit einfacher Regel-Logik.")
        api_key = st.text_input("OpenAI API Key optional", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        model = st.text_input("Model", value="gpt-4o-mini")
        st.divider()
        st.write("Ziel: Use Cases schnell greifbar machen, testen und in Workflow-Logiken übersetzen.")

    sample = """Guten Tag,

wir möchten unsere internen Dokumentenprozesse effizienter gestalten.
Aktuell bearbeiten mehrere Teams dieselben Informationen parallel, wodurch Verzögerungen entstehen.
Besonders bei Kundenanfragen, Freigaben und Angebotsvorbereitungen verlieren wir viel Zeit.

Können Sie uns hierzu einen Vorschlag machen?

Beste Grüße
Anna Schmidt
Schmidt Solutions GmbH
"""

    text = st.text_area("Anfrage / Dokument / Notiz eingeben", value=sample, height=260)

    if st.button("Anfrage analysieren", type="primary"):
        if not text.strip():
            st.warning("Bitte zuerst einen Text eingeben.")
            return
        with st.spinner("Analyse läuft..."):
            try:
                if api_key:
                    result = analyze_with_openai(text, api_key=api_key, model=model)
                    source = "OpenAI"
                else:
                    result = fallback_rule_based_analysis(text)
                    source = "Fallback-Regel-Logik"
            except Exception as exc:
                st.error(f"OpenAI-Analyse fehlgeschlagen. Fallback wird genutzt. Fehler: {exc}")
                result = fallback_rule_based_analysis(text)
                source = "Fallback-Regel-Logik"

        st.success(f"Analyse abgeschlossen über: {source}")
        render_result(result)

        export = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "input": text,
            "result": result,
            "source": source,
        }
        st.download_button(
            label="Analyse als JSON herunterladen",
            data=json.dumps(export, ensure_ascii=False, indent=2),
            file_name="ai_request_triage_result.json",
            mime="application/json",
        )


if __name__ == "__main__":
    main()
