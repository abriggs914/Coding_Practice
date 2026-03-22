# TELUS Maps Study Aid — Quick Start

## Install dependencies
```
pip install streamlit folium streamlit-folium geopy
```

## Run
```
streamlit run telus_map_tool.py
```

No API key, no account required — everything runs locally.

---

## Features

### Map
- Viewport center pin (blue = Fresh, orange = Stale), user pin (green), up to 6 result pins
- Enter locations as lat/lon OR text address (geocoded via OpenStreetMap/Nominatim)
- Dashed distance lines from user to each result

### Distances
- User and viewport → each result in miles + km, colour-coded
- Multi-result distance ranking table with suggested demotion levels

### Classification Check
- Flags classification vs. query mismatches (e.g. query="Taco Bell", class="Pizza") citing §6.3.2

### Quick Links
- 📍 Google Maps (coordinates), 🔍 Address in Maps, 📮 USPS Verify (opens official tool)

### Chain Locator
- 50+ chains linked to official store locators; Google search fallback for unknowns

### Rule-Based Context Blurb (free, no API key)
Set sidebar parameters:
- User inside/outside FVP, Stale viewport
- Nearby modifier / Location modifier / Few results / Address does not exist
- Distance demotion level (0–3)
- Official name + address for mismatch detection

Outputs exam-style bracketed comment with correct guideline section citations.

## USPS Note
No public API — 📮 button opens the USPS ZIP lookup tool for manual entry.
