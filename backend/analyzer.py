import os
import json
import re
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

from langchain_groq import ChatGroq

def get_llm():
    if os.getenv("GROQ_API_KEY"):
        return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
    else:
        raise ValueError("No API key found. Set GROQ_API_KEY.")


def safe_parse_json(text: str) -> dict:
    """Extract and parse JSON from LLM response, stripping markdown fences."""
    cleaned = re.sub(r"```(?:json)?", "", text).replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse JSON from LLM response: {text[:300]}")


EXTRACT_SKILLS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a technical recruiter and skills analyst. Extract structured information from job descriptions and resumes.
Always respond with valid JSON only. No markdown, no explanation."""),
    ("user", """Extract skills and requirements from this JOB DESCRIPTION:

{jd_text}

Return JSON with this exact structure:
{{
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill1", "skill2"],
  "role_title": "string",
  "experience_years": "string (e.g. '2-4 years' or 'not specified')",
  "key_responsibilities": ["responsibility1", "responsibility2", "responsibility3"]
}}""")
])

EXTRACT_RESUME_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a technical recruiter. Extract structured information from resumes.
Always respond with valid JSON only. No markdown, no explanation."""),
    ("user", """Extract skills and experience from this RESUME:

{resume_text}

Return JSON with this exact structure:
{{
  "candidate_name": "string",
  "current_role": "string",
  "years_experience": "string",
  "technical_skills": ["skill1", "skill2"],
  "soft_skills": ["skill1", "skill2"],
  "education": "string",
  "notable_achievements": ["achievement1", "achievement2"]
}}""")
])

GAP_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior technical recruiter performing a detailed gap analysis between a job description and a resume.
Be honest, specific, and constructive. Always respond with valid JSON only."""),
    ("user", """Perform a gap analysis.

JOB REQUIREMENTS:
{jd_skills}

CANDIDATE PROFILE:
{resume_skills}

ORIGINAL RESUME TEXT:
{resume_text}

Return JSON with this exact structure:
{{
  "match_score": <integer 0-100>,
  "match_verdict": "<one of: Strong Match | Good Match | Partial Match | Weak Match>",
  "matched_skills": [
    {{"skill": "string", "evidence": "brief quote or note from resume"}}
  ],
  "missing_critical": [
    {{"skill": "string", "why_critical": "why this matters for the role"}}
  ],
  "missing_preferred": ["skill1", "skill2"],
  "strengths": ["strength1", "strength2", "strength3"],
  "ats_flags": ["potential ATS issue 1", "potential ATS issue 2"],
  "overall_assessment": "2-3 sentence honest assessment"
}}""")
])

REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert resume writer who specializes in tailoring resumes for specific job descriptions.
Rewrite bullet points to be stronger, more quantified, and better aligned to the target role.
Always respond with valid JSON only."""),
    ("user", """Given this job description context and resume, suggest improved bullet points.

TARGET ROLE: {role_title}
KEY JD REQUIREMENTS: {key_requirements}
MISSING SKILLS TO ADDRESS: {missing_skills}

ORIGINAL RESUME TEXT:
{resume_text}

Return JSON with this exact structure:
{{
  "rewritten_bullets": [
    {{
      "original": "original bullet or section text",
      "rewritten": "improved version",
      "reason": "why this change helps"
    }}
  ],
  "new_bullets_to_add": [
    {{
      "bullet": "suggested new bullet point",
      "where_to_add": "which section/role to add it under",
      "addresses": "which gap this fills"
    }}
  ],
  "keywords_to_add": ["keyword1", "keyword2", "keyword3"],
  "summary_suggestion": "A suggested professional summary tailored to this JD"
}}""")
])


async def run_analysis(resume_text: str, jd_text: str) -> dict:
    """
    Full 3-stage LangChain pipeline:
    1. Extract JD requirements
    2. Extract resume skills
    3. Gap analysis + rewrite suggestions
    """
    llm = get_llm()
    parser = StrOutputParser()

    chain_jd = EXTRACT_SKILLS_PROMPT | llm | parser
    chain_resume = EXTRACT_RESUME_PROMPT | llm | parser
    chain_gap = GAP_ANALYSIS_PROMPT | llm | parser
    chain_rewrite = REWRITE_PROMPT | llm | parser

    jd_raw = await chain_jd.ainvoke({"jd_text": jd_text})
    jd_skills = safe_parse_json(jd_raw)

    resume_raw = await chain_resume.ainvoke({"resume_text": resume_text})
    resume_skills = safe_parse_json(resume_raw)

    gap_raw = await chain_gap.ainvoke({
        "jd_skills": json.dumps(jd_skills, indent=2),
        "resume_skills": json.dumps(resume_skills, indent=2),
        "resume_text": resume_text[:3000],
    })
    gap_analysis = safe_parse_json(gap_raw)

    missing_skills = [s["skill"] for s in gap_analysis.get("missing_critical", [])]
    rewrite_raw = await chain_rewrite.ainvoke({
        "role_title": jd_skills.get("role_title", ""),
        "key_requirements": ", ".join(jd_skills.get("required_skills", [])[:8]),
        "missing_skills": ", ".join(missing_skills[:5]),
        "resume_text": resume_text[:3000],
    })
    rewrite_suggestions = safe_parse_json(rewrite_raw)

    return {
        "jd_analysis": jd_skills,
        "resume_analysis": resume_skills,
        "gap_analysis": gap_analysis,
        "rewrite_suggestions": rewrite_suggestions,
    }
