# Resume Analyzer & Job Matcher

A FastAPI-based web service for extracting skills from resumes (PDF or text) and matching them against job descriptions. Utilizes spaCy for NLP and PyMuPDF for PDF parsing.

## Features
- Extracts technical and soft skills from uploaded resumes (PDF or text)
- Matches extracted skills against a provided job description (JSON)
- Returns matched, missing skills, and match percentage
- Simple REST API endpoints

## Requirements
- Python 3.8+
- pip (Python package manager)

### Python Dependencies
- fastapi
- uvicorn
- spacy
- pymupdf (fitz)

## Setup Instructions

1. **Clone or Download the Repository**

2. **Install Python dependencies:**
   ```sh
   pip install fastapi uvicorn spacy pymupdf
   ```

3. **Download spaCy English Model:**
   ```sh
   python -m spacy download en_core_web_sm
   ```

4. **Run the FastAPI server:**
   ```sh
   uvicorn main:app --reload
   ```
   The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Usage

### 1. Analyze Resume
- **Endpoint:** `/analyze_resume/`
- **Method:** POST
- **Body:** Multipart form with a file (PDF or .txt)
- **Response:**
  ```json
  { "skills": ["python", "machine learning", ...] }
  ```

### 2. Match Resume to Job
- **Endpoint:** `/match_job/`
- **Method:** POST
- **Body:** Multipart form with two files:
  - `resume_file`: Resume (PDF or .txt)
  - `job_file`: Job description JSON file, e.g. `{ "skills": ["python", "aws", ...] }`
- **Response:**
  ```json
  {
    "resume_skills": ["python", ...],
    "job_skills": ["python", ...],
    "matched_skills": ["python"],
    "missing_skills": ["aws"],
    "match_percent": 50.0
  }
  ```

## Example Job Description JSON
```json
{
  "skills": ["python", "aws", "docker"]
}
```

## Troubleshooting
- **PyMuPDF install issues on Windows:**
  - Ensure you have a compatible Python version (3.8+ recommended)
  - If you encounter build errors, try upgrading pip: `python -m pip install --upgrade pip`
- **spaCy model not found:**
  - Run `python -m spacy download en_core_web_sm`
- **CORS errors:**
  - For frontend integration, consider adding CORS middleware to FastAPI.

## License
MIT
