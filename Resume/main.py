from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
import spacy
import fitz  # PyMuPDF for PDF parsing
import io
import json

app = FastAPI()

# Load spaCy model for NLP (en_core_web_sm is lightweight, can be replaced with a larger model)
nlp = spacy.load("en_core_web_sm")

# Example skill set for demo purposes
SKILL_SET = [
    "python", "java", "c++", "machine learning", "deep learning", "nlp", "data analysis",
    "react", "flask", "fastapi", "django", "sql", "aws", "docker", "kubernetes"
]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text: str) -> List[str]:
    doc = nlp(text.lower())
    found_skills = set()
    for token in doc:
        if token.text in SKILL_SET:
            found_skills.add(token.text)
    # Also check for multi-word skills
    for skill in SKILL_SET:
        if " " in skill and skill in text.lower():
            found_skills.add(skill)
    return list(found_skills)

def match_skills(resume_skills: List[str], job_skills: List[str]) -> dict:
    matched = set(resume_skills) & set(job_skills)
    missing = set(job_skills) - set(resume_skills)
    match_percent = round(len(matched) / len(job_skills) * 100, 2) if job_skills else 0.0
    return {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "match_percent": match_percent
    }

@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        contents = await file.read()
        text = extract_text_from_pdf(contents)
    else:
        contents = await file.read()
        text = contents.decode("utf-8")
    skills = extract_skills(text)
    return JSONResponse({"skills": skills})

@app.post("/match_job/")
async def match_job(resume_file: UploadFile = File(...), job_file: UploadFile = File(...)):
    # Parse resume
    if resume_file.filename.endswith(".pdf"):
        resume_contents = await resume_file.read()
        resume_text = extract_text_from_pdf(resume_contents)
    else:
        resume_contents = await resume_file.read()
        resume_text = resume_contents.decode("utf-8")
    resume_skills = extract_skills(resume_text)
    # Parse job description JSON
    job_contents = await job_file.read()
    try:
        job_json = json.loads(job_contents.decode("utf-8"))
        job_skills = job_json.get("skills", [])
        if not isinstance(job_skills, list):
            job_skills = []
    except Exception:
        return JSONResponse({"error": "Invalid job description JSON."}, status_code=400)
    result = match_skills(resume_skills, job_skills)
    return JSONResponse({
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "match_percent": result["match_percent"]
    })