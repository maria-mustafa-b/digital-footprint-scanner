<div align="center">

# 🔍 Digital Footprint Scanner

**An open-source OSINT tool that builds a full digital identity report from a username or email address.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange?style=flat-square)]()

[Features](#features) · [Architecture](#architecture) · [Getting Started](#getting-started) · [API Reference](#api-reference) · [Roadmap](#roadmap) · [Ethics](#ethics--legal)

</div>

---

## Overview

Digital Footprint Scanner is a portfolio-grade OSINT (Open Source Intelligence) tool that accepts a username or email address and produces a comprehensive public identity report. It fans out across dozens of public data sources in parallel, aggregates the results, identifies cross-platform patterns, and outputs an interactive dashboard, a PDF cyber report, and a graph-based identity map.

> **Intended use:** Self-assessment, security research, and educational purposes only. See [Ethics & Legal](#ethics--legal) before using.

---

## Features

### Core scanning
- **Username footprint search** — checks 300+ platforms via Sherlock/WhatsMyName
- **Email breach detection** — queries HaveIBeenPwned and similar breach databases
- **Cross-platform identity mapping** — links accounts by shared email, username variants, bio cross-references, and profile photo hashing
- **Search engine dorking** — automated Google/Bing queries to surface indexed mentions

### Intelligence layer
- **Risk scoring engine** — weighted 0–100 exposure score based on breach severity, platform count, data type exposed, and username reuse patterns
- **Identity clustering** — graph-based algorithm that groups accounts likely belonging to the same person using NetworkX connected components
- **Pattern detection** — flags username reuse, credential reuse across breaches, and linked bios

### Output
- **Interactive React dashboard** — live scan progress, filterable results table, risk gauge
- **PDF cyber report** — exportable one-page summary with exposure score, platform list, and recommendations
- **D3.js identity graph** — force-directed visualization of account relationships and signal edges
- **JSON export** — machine-readable output for use with other security tools

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                          │
│            Username  ·  Email  ·  Phone (optional)          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                    Input normalizer
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
  ┌─────────────┐   ┌──────────────┐   ┌─────────────────┐
  │  Username   │   │   Breach     │   │  Social mapper  │
  │  checker    │   │   scanner    │   │  + dork engine  │
  │ (Sherlock)  │   │   (HIBP)     │   │  (platform APIs)│
  └──────┬──────┘   └──────┬───────┘   └────────┬────────┘
         └──────────────── ▼ ───────────────────┘
                   Data aggregator
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   Risk scorer     Identity clusterer    Pattern detector
         └─────────────────┼─────────────────┘
                    Report builder
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    Dashboard           PDF report      Identity graph
```

The backend is fully async — all collectors run concurrently via `asyncio` and `aiohttp`, keeping scan time under 30 seconds for most targets.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Redis (for job queueing)
- A [HaveIBeenPwned API key](https://haveibeenpwned.com/API/Key)

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/digital-footprint-scanner.git
cd digital-footprint-scanner

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Add your API keys to .env

# Frontend setup
cd ../frontend
npm install
```

### Configuration

Edit `backend/.env`:

```env
HIBP_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
GOOGLE_CSE_ID=your_cse_id_here
REDIS_URL=redis://localhost:6379
```

### Running

```bash
# Start Redis
redis-server

# Start the backend API (from /backend)
uvicorn main:app --reload --port 8000

# Start the frontend (from /frontend)
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Project Structure

```
digital-footprint-scanner/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── collectors/
│   │   ├── username_checker.py  # Sherlock integration
│   │   ├── breach_scanner.py    # HIBP + breach DB queries
│   │   ├── social_mapper.py     # Platform profile fetcher
│   │   └── dork_engine.py       # Search engine automation
│   ├── processing/
│   │   ├── risk_scorer.py       # Weighted exposure scoring
│   │   ├── identity_clusterer.py# NetworkX graph clustering
│   │   └── pattern_detector.py  # Username/credential reuse
│   ├── output/
│   │   ├── report_builder.py    # PDF generation (WeasyPrint)
│   │   └── graph_exporter.py    # D3-ready JSON graph format
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx    # Main scan UI
│   │   │   ├── RiskGauge.jsx    # Score visualizer
│   │   │   ├── IdentityGraph.jsx# D3 force graph
│   │   │   └── ReportExport.jsx # PDF download
│   │   └── App.jsx
│   └── package.json
├── tests/
│   ├── test_collectors.py
│   ├── test_clustering.py
│   └── test_risk_scorer.py
├── docs/
│   └── architecture.md
├── .env.example
└── README.md
```

---

## API Reference

### `POST /api/scan`

Start a new scan.

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "options": {
    "include_breach_scan": true,
    "include_social_map": true,
    "min_confidence": 0.5
  }
}
```

**Response:**

```json
{
  "scan_id": "abc123",
  "status": "queued"
}
```

### `GET /api/scan/{scan_id}`

Poll for scan progress and results.

### `GET /api/scan/{scan_id}/report`

Download the PDF report.

### `GET /api/scan/{scan_id}/graph`

Get the identity graph as D3-compatible JSON.

Full API docs available at `http://localhost:8000/docs` (Swagger UI) when running locally.

---

## Risk Scoring

Exposure scores are calculated on a 0–100 scale using a weighted signal model:

| Signal | Points |
|---|---|
| Platform found (per platform) | +5 |
| Email found in breach | +20 |
| Password hash exposed | +30 |
| Username reused across 5+ sites | +15 |
| Real name + photo publicly linked | +10 |
| Location or employer exposed | +10 |
| Dark web mention (API) | +35 |

| Score | Risk Level |
|---|---|
| 0–25 | 🟢 Low |
| 26–50 | 🟡 Moderate |
| 51–75 | 🟠 High |
| 76–100 | 🔴 Critical |

---

## Roadmap

- [x] Username search (Sherlock integration)
- [x] Email breach detection (HIBP)
- [x] Risk scoring engine
- [x] Identity clustering (graph-based)
- [x] React dashboard
- [x] PDF report export
- [ ] D3.js identity graph visualization
- [ ] Change detection & alerting (re-scan and diff)
- [ ] AI-based fake profile detection
- [ ] ML risk scoring model (replaces weighted formula)
- [ ] Chrome extension
- [ ] Dark web monitoring (API-based)
- [ ] Timeline view (account creation history)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, Python 3.11 |
| Async I/O | asyncio, aiohttp |
| Job queue | Celery + Redis |
| Graph analysis | NetworkX |
| Username search | Sherlock, WhatsMyName |
| Breach data | HaveIBeenPwned API |
| Image hashing | imagehash (perceptual) |
| PDF generation | WeasyPrint |
| Frontend | React 18, Vite |
| Graph viz | D3.js / Cytoscape.js |
| Charts | Recharts |
| String similarity | python-Levenshtein |

---

## Ethics & Legal

This tool queries **publicly available data only**. It does not scrape login-protected pages, bypass authentication, or access private data.

**Responsible use guidelines:**

- Only scan yourself, or individuals who have given explicit consent
- Respect platform `robots.txt` and rate limits — the tool enforces delays between requests
- Do not use results to harass, dox, stalk, or harm individuals
- Comply with GDPR, CCPA, and any applicable data protection laws in your jurisdiction
- The tool stores no scan results beyond your local session unless you explicitly save them

Misuse of this tool may violate computer fraud laws, platform terms of service, and privacy regulations. The author assumes no liability for misuse.

---

## Contributing

Contributions are welcome. Please open an issue before submitting a large PR so we can discuss the approach.

```bash
# Run tests
cd backend && pytest tests/

# Lint
flake8 . && black --check .
```

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built for educational and security research purposes · Star the repo if you found it useful
</div>
