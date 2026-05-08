# AI Request Triage Tool

Mini-MVP für eine AI-Enablement-Rolle: Das Tool analysiert eingehende Geschäftsanfragen, strukturiert sie, priorisiert sie und erzeugt einen Antwortvorschlag.

## Was das Tool zeigt

- Identifikation und Strukturierung eines AI-Use-Cases
- Schneller MVP-Ansatz statt langer Konzeptphase
- KI-gestützte Analyse, Priorisierung und Reaktionslogik
- Grundlage für interne Workflows, Prompt-Bibliotheken und Enablement

## Use Case

Viele interne und externe Anfragen kommen unstrukturiert an. Teams müssen Inhalte lesen, einordnen, priorisieren und manuell beantworten.

Dieses MVP zeigt, wie ein AI Agent diese Schritte vorbereiten kann:

1. Anfrage verstehen
2. Kategorie und Priorität bestimmen
3. Geschäftsproblem erkennen
4. nächste Schritte vorschlagen
5. Antwortentwurf generieren
6. Automatisierungspotenzial bewerten

## Tech Stack

- Python
- Streamlit
- OpenAI API optional
- Fallback-Regel-Logik ohne API-Key

## Installation

```bash
pip install -r requirements.txt
```

## Start

```bash
streamlit run app.py
```

Optional mit OpenAI API Key:

```bash
export OPENAI_API_KEY="dein-key"
streamlit run app.py
```

Alternativ kann der API-Key direkt in der Sidebar eingegeben werden.

## Beispielinput

```text
Guten Tag,

wir möchten unsere internen Dokumentenprozesse effizienter gestalten.
Aktuell bearbeiten mehrere Teams dieselben Informationen parallel, wodurch Verzögerungen entstehen.
Besonders bei Kundenanfragen, Freigaben und Angebotsvorbereitungen verlieren wir viel Zeit.

Können Sie uns hierzu einen Vorschlag machen?

Beste Grüße
Anna Schmidt
Schmidt Solutions GmbH
```

## Beispieloutput

Das Tool erzeugt unter anderem:

- Kurzfassung
- Kategorie
- Priorität
- Dringlichkeitsscore
- Geschäftsproblem
- nächste Schritte
- Antwortvorschlag
- Workflow-Vorschlag
- JSON Export

## Weiterentwicklung

Mögliche nächste Schritte:

- Anschluss an E-Mail-Postfach
- Speicherung in Airtable, Notion oder Datenbank
- Rollenbasierte Routing-Logik
- Prompt-Bibliothek für verschiedene Fachbereiche
- Guardrails für Datenschutz und Qualitätssicherung
- Übergabe produktionsreifer Use Cases an Entwicklung / IT

## Rolle im AI Center of Excellence

Dieses MVP ist bewusst klein gehalten. Es zeigt nicht maximale technische Tiefe, sondern die Fähigkeit, ein reales Problem schnell in einen testbaren Prototyp zu übersetzen.
