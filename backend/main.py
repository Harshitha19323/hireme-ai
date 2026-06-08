import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from parser import extract_resume_text
from analyzer import run_analysis

load_dotenv()

app = FastAPI(title="Resume Gap Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextAnalyzeRequest(BaseModel):
    resume_text: str
    jd_text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze/text")
async def analyze_text(request: TextAnalyzeRequest):
    """Analyze when resume is pasted as plain text."""
    if len(request.resume_text.strip()) < 100:
        raise HTTPException(status_code=400, detail="Resume text too short.")
    if len(request.jd_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Job description too short.")
    try:
        result = await run_analysis(request.resume_text, request.jd_text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/upload")
async def analyze_upload(
    jd_text: str = Form(...),
    resume_file: UploadFile = File(...),
):
    """Analyze when resume is uploaded as PDF or .txt file."""
    allowed = {".pdf", ".txt"}
    ext = os.path.splitext(resume_file.filename or "")[-1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")

    file_bytes = await resume_file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max 5MB.")

    try:
        resume_text = extract_resume_text(file_bytes, resume_file.filename)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse file: {str(e)}")

    if len(resume_text.strip()) < 100:
        raise HTTPException(status_code=422, detail="Extracted text too short. Is the PDF text-based?")

    try:
        result = await run_analysis(resume_text, jd_text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
