import streamlit as st
import requests
import pandas as pd
import json

# API Base URL
BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Resume Screening & Ranking", layout="wide", page_icon="📄")

st.title("🚀 AI Resume Screening & Candidate Ranking System")
st.markdown("A professional full-stack implementation using FastAPI (Backend) and NLP (TF-IDF + spaCy).")

# Sidebar - Project Overview
with st.sidebar:
    st.header("Project Overview")
    st.info("Rank candidates based on skill relevance using TF-IDF and Cosine Similarity.")
    st.subheader("How to Use:")
    st.write("1. Upload multiple resumes (PDF/DOCX).")
    st.write("2. Paste the Job Description.")
    st.write("3. Click 'Rank Candidates' to evaluate.")

# Step 1: Upload Resumes
st.subheader("1. Candidate Resumes")
uploaded_files = st.file_uploader(
    "Upload Candidate Resumes (PDF or DOCX)", 
    type=['pdf', 'docx'], 
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("Upload to Backend"):
        with st.spinner("Uploading and extracting text..."):
            files_to_send = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
            try:
                response = requests.post(f"{BASE_URL}/upload_resumes", files=files_to_send)
                if response.status_code == 200:
                    st.success(f"Successfully uploaded {len(uploaded_files)} resumes.")
                else:
                    st.error("Upload failed. Check if Backend is running.")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

# Step 2: Job Description
st.subheader("2. Job Description")
jd_text = st.text_area("Paste the actual job description here:", height=300)

# Step 3: Analysis
if st.button("Rank Candidates", type="primary"):
    if not jd_text:
        st.warning("Please provide a Job Description.")
    else:
        with st.spinner("Analyzing and Ranking..."):
            try:
                response = requests.post(
                    f"{BASE_URL}/rank_candidates", 
                    data={"job_description": jd_text}
                )
                
                if response.status_code == 200:
                    results = response.json().get("ranked_candidates", [])
                    
                    if not results:
                        st.info("No resumes found in system. Please upload some first.")
                    else:
                        st.balloons()
                        st.divider()
                        st.subheader("🏆 Ranked Results")
                        
                        # Prepare data for display
                        display_data = []
                        for res in results:
                            display_data.append({
                                "Candidate": res["candidate"],
                                "Match Score (%)": f"{res['score']:.2f}%",
                                "Score": res["score"], # For progress bar
                                "Matching Skills": ", ".join(res["matching_skills"]),
                                "Missing Skills": ", ".join(res["missing_skills"])
                            })
                        
                        df = pd.DataFrame(display_data)
                        
                        # Use Streamlit's new dataframe widget with progress bar
                        st.dataframe(
                            df,
                            column_config={
                                "Score": st.column_config.ProgressColumn(
                                    "Visual Match",
                                    help="Graphical representation of the similarity score",
                                    format="%.2f",
                                    min_value=0,
                                    max_value=100,
                                ),
                                "Candidate": st.column_config.TextColumn("Name"),
                                "Match Score (%)": st.column_config.TextColumn("Score"),
                                "Matching Skills": st.column_config.TextColumn("Skills Found"),
                                "Missing Skills": st.column_config.TextColumn("Skills Missing"),
                            },
                            hide_index=True,
                            use_container_width=True
                        )
                else:
                    st.error("Ranking failed. Ensure backend is running and resumes are uploaded.")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

st.divider()
st.caption("AI Resume Screening System - Academic Project Build - April 2026")
