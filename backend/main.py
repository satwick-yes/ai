from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import shutil
import json
from utils.extraction import extract_text
from utils.nlp_pipeline import clean_text, extract_skills
from utils.scoring import calculate_similarity

app = FastAPI(title="AI Resume Screening API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for research/academic demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure research data directory exists
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.post("/upload_resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload resumes and extract text.
    Saves extracted text to the data/ directory for processing.
    """
    uploaded_files = []
    for file in files:
        file_content = await file.read()
        extracted_text = extract_text(file.name, file_content)
        
        if extracted_text:
            # Save extracted text to data/ with .txt extension for persistence
            safe_name = "".join(x for x in file.name if x.isalnum() or x in "._- ")
            text_file_path = os.path.join(DATA_DIR, f"{safe_name}.txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            uploaded_files.append(file.name)
            
    return {"message": "Resumes uploaded and text extracted", "files": uploaded_files}

@app.post("/analyze")
async def analyze():
    """
    Endpoint to perform NLP cleaning and skill extraction on all saved resumes.
    """
    analysis_results = []
    if not os.path.exists(DATA_DIR):
        return {"results": []}

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()
            
            cleaned = clean_text(raw_text)
            skills = extract_skills(raw_text)
            
            analysis_results.append({
                "candidate": filename.replace(".txt", ""),
                "skills": skills,
                "cleaned_text": cleaned
            })
            
    return {"analysis": analysis_results}

@app.post("/rank_candidates")
async def rank_candidates(job_description: str = Form(...)):
    """
    Endpoint to rank candidates against a job description.
    """
    if not os.path.exists(DATA_DIR):
        raise HTTPException(status_code=400, detail="No resumes uploaded yet.")

    resumes = []
    names = []
    
    # Pre-extract JD skills
    jd_skills = set(extract_skills(job_description))
    cleaned_jd = clean_text(job_description)

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()
            
            resumes.append(clean_text(raw_text))
            names.append(filename.replace(".txt", ""))

    if not resumes:
        return {"ranked_candidates": []}

    # Similarity calculation
    scores = calculate_similarity(cleaned_jd, resumes)
    
    ranked_list = []
    for i in range(len(names)):
        # Skill Matching
        filepath = os.path.join(DATA_DIR, names[i] + ".txt")
        with open(filepath, "r", encoding="utf-8") as f:
            raw_resume_text = f.read()
            
        candidate_skills = set(extract_skills(raw_resume_text))
        matching_skills = candidate_skills.intersection(jd_skills)
        missing_skills = jd_skills.difference(candidate_skills)

        ranked_list.append({
            "candidate": names[i],
            "score": scores[i],
            "matching_skills": sorted(list(matching_skills)),
            "missing_skills": sorted(list(missing_skills))
        })

    # Sort by score descending
    ranked_list = sorted(ranked_list, key=lambda x: x['score'], reverse=True)
    
    return {"ranked_candidates": ranked_list}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
