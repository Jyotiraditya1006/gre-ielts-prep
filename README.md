# 🎓 ApexPrep AI (ApexPrep.ai) — GRE® & IELTS™ Comprehensive Prep Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Cloudflare%20Public%20Tunnel-blue?style=for-the-badge&logo=cloudflare)](https://eric-lectures-consists-comprehensive.trycloudflare.com)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> A production-grade, state-of-the-art preparation platform modeled after **Exambank AI** for **ETS GRE® General Test** and **IDP / British Council Computer-Delivered IELTS™**. Features authentic testing interfaces, real-time radial score forecasting, dual Dark/Light mode theme system, official diagnostic scoring, a 2.58M+ word morphological vocabulary lexicon, and phone OTP authentication.

---

## 🌟 Key Features

### 🏛️ Official ETS GRE® Full Mock Exam Simulation
- **Current Shorter GRE Format (Post-Sept 2023)**:
  - **Section 1**: Analytical Writing (Analyze an Issue · 30 min)
  - **Section 2**: Verbal Reasoning Section 1 (12 Qs · 18 min)
  - **Section 3**: Quantitative Reasoning Section 1 (12 Qs · 21 min · Calculator Enabled)
  - **Section 4**: Verbal Reasoning Section 2 (15 Qs · 23 min)
  - **Section 5**: Quantitative Reasoning Section 2 (15 Qs · 26 min · Calculator Enabled)
- **Authentic ETS Test-Taker Tools**:
  - **On-Screen Calculator**: 4-function with square root (`√`), memory (`MC`, `MR`, `MS`, `M+`), and official **"Transfer Display"** into numeric entry fields.
  - **Section Review Table**: Real-time status tracking (**Answered** vs. **Incomplete**) and marked questions (**✓**) with direct jump navigation.
  - **Official Timer**: "Hide Time" / "Show Time" toggle with critical 2-minute alerts.
- **ETS Scaled Scoring Diagnostic**:
  - Verbal Reasoning: **130 – 170**
  - Quantitative Reasoning: **130 – 170**
  - Total Scaled Score: **260 – 340**
  - Analytical Writing Assessment: **0.0 – 6.0**

---

### 🇬🇧 Official Computer-Delivered IELTS™ Simulation
- **All 3 Academic Modules**:
  - **Academic Reading**: 3 Passages · 40 Questions · 60 minutes with **authentic split-screen passage reading & text highlight**.
  - **40-Question Bottom Ribbon**: 1-click question tabs grouped into Passage 1 (1–13), Passage 2 (14–26), and Passage 3 (27–40) with color-coded answered and review indicators.
  - **Academic Writing**: Task 1 (Report/Chart, 150w min) & Task 2 (Essay, 250w min) with **real-time word count tracking**.
  - **Speaking Interview**: Face-to-face examiner simulator with Parts 1, 2 (Cue Card with 1-min preparation countdown), and Part 3.
- **IELTS 9-Band Test Report Form (TRF)**:
  - Individual band scores (0.0 – 9.0 in 0.5 increments) for Reading, Writing, Speaking, and Overall Band with CEFR level mapping (B2, C1, C2).

---

### ♾️ Zero-Latency Infinite Practice Questions
- **Procedural Mathematical Engine**: Combinatorial quantitative comparison, rate/work problems, and geometry problems generated in < 1ms.
- **Sentence Equivalence & Text Completion**: Authentic GRE verbal question variations with subtle tone and semantic contrasts.
- **Background Prefetch Queue**: Questions transition in **0ms** (zero waiting time) while subsequent questions replenish quietly in the background.

---

### 🃏 Multi-Million Word Vocabulary Engine (2,584,320+ Words)
- **Morphological Root Index**: Combines 47 classical prefixes, 43 Greek & Latin roots (e.g. *chron*, *bell*, *loqu*, *morph*, *phil*), and 24 academic suffixes.
- **Live Search & Root Decomposition**: Instant lookup of any English word or classical root with grammatical classification, academic definitions, context sentences, and etymological mnemonics.
- **Infinite Word Stream**: Continuous procedural flashcard feed with interactive 3D card flips.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: Python 3.11+, FastAPI (Async), SQLAlchemy 2.0, SQLite / PostgreSQL, JWT Authentication, Passlib/Bcrypt.
- **Frontend**: Vanilla ES6+ JavaScript, Responsive CSS3 (Glassmorphism & dark/light design system), HTML5 Semantic Architecture.
- **Procedural Engines**: Combinatorial mathematical question generator (`InfiniteQuestionEngine`) and etymological morphological lexicon (`InfiniteVocabEngine`).

---

## 🚀 Quickstart & Local Setup

```bash
# 1. Clone repository
git clone https://github.com/Jyotiraditya1006/gre-ielts-prep.git
cd gre-ielts-prep

# 2. Create virtual environment & install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Launch application
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at **`http://localhost:8000`**.

---

## 🐳 Docker & Cloud Deployment

### Docker
```bash
docker build -t gre-ielts-prep .
docker run -p 8000:8000 gre-ielts-prep
```

### 1-Click Cloud Deployment (Render / Railway)
- **Render**: Connect this repository to [Render](https://render.com) — `render.yaml` and `Procfile` are pre-configured.
- **Railway**: Connect this repository to [Railway](https://railway.app) for instant zero-config containerized deployment.

---

## 📄 License
MIT License © 2026 Jyotiraditya Patankar.
