# ResumeGap — AI Resume Gap Analyzer

Paste a job description + your resume → get a structured gap analysis, ATS flags, match score, and AI-rewritten bullet points.

## Stack

- **Backend**: FastAPI + LangChain (3-stage LLM pipeline) + pdfplumber
- **Frontend**: Vanilla HTML/CSS/JS served via Nginx
- **LLM**: Claude 3.5 Sonnet (Anthropic) or GPT-4o (OpenAI)
- **Deploy**: Docker Compose

## How it works

```
Resume (PDF/text) + Job Description
        ↓
  [Stage 1] Extract JD requirements  →  required skills, experience, responsibilities
  [Stage 2] Extract resume profile    →  candidate skills, experience, achievements
  [Stage 3] Gap analysis              →  match score, missing skills, ATS flags
  [Stage 4] Rewrite suggestions       →  improved bullets, new bullets, keywords
        ↓
  Structured JSON → Frontend renders results
```

## Quick Start

### 1. Clone and set up env
```bash
git clone <your-repo>
cd resume-gap-analyzer
cp .env.example .env
# Edit .env and add your API key
```

### 2. Build and run
```bash
docker compose up --build
```

### 3. Open in browser
```
http://localhost:3000
```

API docs available at: `http://localhost:8000/docs`

## Project Structure

```
resume-gap-analyzer/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── main.py          # FastAPI routes
│   ├── analyzer.py      # LangChain 3-stage pipeline
│   ├── parser.py        # PDF + text extraction
│   └── requirements.txt
└── frontend/
    ├── Dockerfile
    ├── index.html        # Single-page UI
    └── nginx.conf
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/analyze/text` | Analyze with plain text resume |
| POST | `/analyze/upload` | Analyze with uploaded PDF/TXT |

### Example: Text analysis
```bash
curl -X POST http://localhost:8000/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "...", "jd_text": "..."}'
```

### Example: PDF upload
```bash
curl -X POST http://localhost:8000/analyze/upload \
  -F "jd_text=We are looking for..." \
  -F "resume_file=@my_resume.pdf"
```

## Extending this project

- Add a **vector DB** (ChromaDB/Qdrant) to store past analyses and spot patterns across applications
- Add **job scraping** via Apify to auto-fetch JDs from LinkedIn/Naukri
- Add a **cover letter generator** as a 5th LangChain stage
- Add **auth + history** so users can track improvements over time
- Switch to **LangGraph** for a proper stateful multi-agent flow with retry logic

## Notes

- Only text-based PDFs are supported (not scanned/image PDFs)
- Analysis takes ~15–30 seconds depending on resume length
- The LLM is auto-selected: Anthropic key → Claude 3.5 Sonnet; OpenAI key → GPT-4o
