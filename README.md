<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=180&section=header&text=HireMe%20AI&fontSize=52&fontColor=fff&animation=twinkling&fontAlignY=32&desc=Resume%20vs%20JD%20Gap%20Analyzer%20%7C%20Powered%20by%20LLaMA%203.3%2070B%20%2B%20LangChain&descAlignY=55&descSize=14)

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&pause=1000&color=EC4899&center=true&vCenter=true&width=700&lines=Know+exactly+why+you're+not+getting+the+interview.;Paste+JD+%2B+Resume+%E2%86%92+Get+Gap+Analysis+in+seconds;Match+Score+%F0%9F%8E%AF+%7C+ATS+Flags+%E2%9A%A0%EF%B8%8F+%7C+AI+Rewrites+%E2%9C%8D%EF%B8%8F;Built+with+FastAPI+%2B+LangChain+%2B+Groq+%2B+Docker)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

</div>

---

## 😤 The Problem

You've applied to 50+ jobs. You're qualified. But you're not hearing back.

Here's what's actually happening:

- **ATS systems filter you out** before a human ever reads your resume
- **You're missing keywords** the JD specifically requires
- **Your bullet points are generic** — not tailored to the role
- **You don't know what's missing** — so you keep applying with the same resume

Tools like **Jobscan, ResumeWorded, and Kickresume** exist — but they only do **keyword matching**. They give you a score. They don't tell you *why* skills matter, *how* to fix your bullets, or *what to write* to fill specific gaps.

**HireMe AI solves the full problem** — not just the score.

---

## 💡 What Makes This Different

| Feature | Jobscan / ResumeWorded | **HireMe AI** |
|---|---|---|
| Match Score | ✅ Keyword match % | ✅ LLM-reasoned 0–100 score |
| Gap Analysis | ❌ Lists missing keywords | ✅ Explains *why* each gap matters for the role |
| ATS Flags | ⚠️ Generic suggestions | ✅ Specific flags with context |
| Bullet Rewrites | ❌ Not available | ✅ Before/after with reasoning |
| New Bullets | ❌ Not available | ✅ Suggests bullets that fill specific gaps |
| Summary | ❌ Not available | ✅ Tailored professional summary for the JD |
| Privacy | ☁️ Cloud SaaS | ✅ Runs 100% locally — your resume never leaves your machine |
| Cost | 💰 Paid plans | ✅ Free — uses Groq's free API tier |
| Model | Rule-based / GPT | ✅ LLaMA 3.3 70B via Groq |

> **The core difference:** Jobscan tells you *what* is missing. HireMe AI tells you *why it matters* and *exactly how to fix it*.

---

## 📸 Screenshots

### Input — Paste JD + Upload Resume PDF
![Input Screen](screenshots/input.png)

### Results — Match Score + Gap Analysis
![Gap Analysis](screenshots/gap-analysis.png)

### ATS Flags + Strengths
![ATS and Strengths](screenshots/ats-flags.png)

---

## 🧠 How It Works — The 4-Stage LangChain Pipeline

This is not a single prompt. It's a structured multi-stage reasoning pipeline:

```
Resume (PDF / Text)  +  Job Description
              ↓
   [Stage 1]  Extract JD requirements
              → required skills, preferred skills, responsibilities, experience level

   [Stage 2]  Parse resume profile
              → candidate skills, achievements, education, years of experience

   [Stage 3]  Gap analysis  ← feeds output of Stage 1 + Stage 2
              → match score (0–100), verdict, matched skills with evidence,
                critical gaps with reasoning, ATS flags, strengths

   [Stage 4]  Rewrite suggestions  ← feeds gaps from Stage 3
              → improved bullet points (before/after), new bullets to add,
                keywords to weave in, tailored professional summary
              ↓
         Structured JSON → Clean UI
```

Each stage gets focused context — not a dump of everything. This is what makes the reasoning accurate and specific rather than generic.

---

## ✨ Features

| | Feature | Description |
|---|---|---|
| 🎯 | **Match Score** | 0–100% with verdict — Strong / Good / Partial / Weak Match |
| ❌ | **Critical Gaps** | Missing skills + explanation of why each one matters for this role |
| ✅ | **Matched Skills** | What you already have, with evidence quoted from your resume |
| ⚠️ | **ATS Flags** | Specific issues that will get you filtered before a human sees your resume |
| 💪 | **Strengths** | What makes you stand out for this specific JD |
| ✍️ | **Bullet Rewrites** | Before/after rewrites with reasoning for every change |
| ➕ | **New Bullets** | Suggested additions that directly address missing skills |
| 🔑 | **Keywords to Add** | ATS-critical keywords your resume is missing |
| 📝 | **Summary Suggestion** | A full professional summary tailored to the target role |
| 📄 | **PDF Upload** | Upload resume as PDF or paste as plain text |

---

## 🛠️ Tech Stack

```yaml
Backend:      FastAPI + Python 3.11
AI Model:     LLaMA 3.3 70B (via Groq API — free tier)
AI Framework: LangChain (4-stage chain pipeline)
PDF Parsing:  pdfplumber
Frontend:     Vanilla HTML + CSS + JS
Server:       Nginx (frontend) + Uvicorn (backend)
Deploy:       Docker + Docker Compose
```

---

## 🐳 Running with Docker (Recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A free Groq API key → [console.groq.com](https://console.groq.com) (2 min signup, no credit card)

### Step 1 — Clone the repo
```bash
git clone https://github.com/Harshitha19323/hireme-ai.git
cd hireme-ai
```

### Step 2 — Add your API key
```bash
cp .env.example .env
```
Open `.env` and fill in:
```
GROQ_API_KEY=your_groq_key_here
```

### Step 3 — Build and run
```bash
docker compose up --build
```

### Step 4 — Open in browser
```
http://localhost:3000
```

To stop: `Ctrl+C` then `docker compose down`

---

## 💻 Running Locally (Without Docker)

### Prerequisites
- Python 3.10+ installed
- Free Groq API key → [console.groq.com](https://console.groq.com)

### Step 1 — Clone the repo
```bash
git clone https://github.com/Harshitha19323/hireme-ai.git
cd hireme-ai
```

### Step 2 — Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3 — Add your API key
Create a `.env` file inside the `backend/` folder:
```
GROQ_API_KEY=your_groq_key_here
```

### Step 4 — Start the backend
```bash
cd hireme-ai/backend
uvicorn main:app --reload --port 8000
```
You should see: `Uvicorn running on http://127.0.0.1:8000`

### Step 5 — Start the frontend
Open a second terminal:
```bash
cd hireme-ai/frontend
python -m http.server 3000
```

### Step 6 — Open in browser
```
http://localhost:3000
```

---

## 📁 Project Structure

```
hireme-ai/
├── docker-compose.yml       # Orchestrates backend + frontend containers
├── .env.example             # Template for environment variables
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── main.py              # FastAPI routes (/analyze/text, /analyze/upload)
│   ├── analyzer.py          # 4-stage LangChain pipeline
│   ├── parser.py            # PDF + text extraction via pdfplumber
│   └── requirements.txt
└── frontend/
    ├── Dockerfile
    ├── index.html           # Single-page UI
    └── nginx.conf
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check — returns `{"status": "ok"}` |
| POST | `/analyze/text` | Analyze with plain text resume + JD |
| POST | `/analyze/upload` | Analyze with uploaded PDF/TXT resume + JD |

**Test via curl:**
```bash
curl -X POST http://localhost:8000/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Your resume...", "jd_text": "Job description..."}'
```

Full interactive docs at: `http://localhost:8000/docs`

---

## 🌐 Connect

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/Harshitha19323)
[![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Harshitha19323)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:harshithapulipakala@gmail.com)

</div>

---

<div align="center">

![footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=120&section=footer)

</div>
