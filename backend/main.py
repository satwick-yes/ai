from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

# Import utility functions
from utils.extraction import get_text_from_file
from utils.nlp_pipeline import calculate_hybrid_similarity, extract_skills, expand_job_with_web_skills

app = FastAPI(title="AI Resume Screening System")

# CORS Setup for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/rank-resumes")
async def rank_resumes(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    """
    Endpoint to receive job description and multiple resume files.
    Returns a ranked list of candidates with scores and extracted skills.
    """
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
        
    if not resumes or len(resumes) == 0:
        raise HTTPException(status_code=400, detail="No resumes uploaded.")

    # List to store results
    candidates = []

    # Iterate through all uploaded resumes
    for resume in resumes:
        try:
            filename = resume.filename
            content = await resume.read()
            
            # 1. Text Extraction
            text = get_text_from_file(filename, content)
            if not text or len(text.strip()) < 50:
                print(f"Skipping {filename}: Insufficient text extracted.")
                continue 
                
            # 2. Skill Extraction (Bonus)
            skills = extract_skills(text)
            
            # 3. Store in list for batch similarity calculation
            candidates.append({
                "name": filename,
                "text": text,
                "skills": skills
            })
        except Exception as e:
            print(f"Error processing {resume.filename}: {e}")
            continue

    if not candidates:
        raise HTTPException(status_code=400, detail="Could not extract valid text from any of the uploaded resumes.")

    try:
        # 4. Web skill expansion
        web_skills = expand_job_with_web_skills(job_description)

        # 5. Extract text only for similarity computation
        resumes_text_list = [c["text"] for c in candidates]
        
        # 6. Compute scores
        detailed_scores = calculate_hybrid_similarity(job_description, resumes_text_list, web_skills=web_skills)
        
        # 7. Build final response
        results = []
        for i, candidate in enumerate(candidates):
            scoring_detail = detailed_scores[i]
            score = scoring_detail["total_score"]
            results.append({
                "name": candidate["name"],
                "score": round(score * 100, 2),
                "skills": scoring_detail["extracted_skills"],  # Override with deeply extracted skills
                "relevance": "High" if score > 0.6 else ("Medium" if score > 0.3 else "Low"),
                "semantic_score": round(scoring_detail["semantic_score"] * 100, 2),
                "skill_score": round(scoring_detail["skill_score"] * 100, 2),
                "keyword_score": round(scoring_detail["keyword_score"] * 100, 2),
                "matched_skills": scoring_detail["matched_skills"],
                "missing_skills": scoring_detail["missing_skills"]
            })

        # 8. Rank by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "candidates": results,
            "web_skills": web_skills
        }
    except Exception as e:
        print(f"Error during ranking: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during the ranking process.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
