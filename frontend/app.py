import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page Config for a premium look
st.set_page_config(
    page_title="ResumeAI - Smart Screening",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional, corporate feel
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1 {
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/resume.png")
    st.title("ResumeAI")
    st.markdown("---")
    st.info("Upload your candidate resumes and specify the job role to find the best match.")
    api_url = st.text_input("API URL", value="http://localhost:8000/rank-resumes")

# Main Content
st.title("🚀 Smart Resume Screening & Ranking")
st.write("Leverage AI to identify the most relevant talent instantly.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Job Requirements")
    job_description = st.text_area(
        "Paste the Job Description here:", 
        placeholder="We are looking for a Senior Python Developer with experience in FastAPI and React...",
        height=300
    )

with col2:
    st.subheader("📂 Candidate Resumes")
    uploaded_files = st.file_uploader(
        "Upload one or more Resume files (PDF/DOCX):", 
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

if st.button("Analyze & Rank Candidates"):
    if not job_description:
        st.error("Please provide a job description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        with st.spinner("Analyzing resumes..."):
            try:
                # Prepare the request
                files = [("resumes", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
                data = {"job_description": job_description}
                
                # Call the FastAPI backend
                response = requests.post(api_url, data=data, files=files)
                
                if response.status_code == 200:
                    response_data = response.json()
                    results = response_data.get("candidates", [])
                    web_skills = response_data.get("web_skills", [])
                    
                    if not results:
                        st.warning("No results returned. Ensure the resumes include extractable text.")
                    else:
                        st.success(f"Analysed {len(results)} resumes successfully!")
                        
                        if web_skills:
                            st.info(f"**AI Detected Required Skills for this Role:** {', '.join(web_skills)}")
                        
                        # Display Results in a Table
                        df = pd.DataFrame(results)
                        
                        # 1. Ranking Overview
                        st.subheader("📊 Candidate Ranking Table")
                        st.dataframe(df[["name", "score", "relevance", "semantic_score", "skill_score", "keyword_score"]].style.background_gradient(subset=['score'], cmap='Greens'))
                        
                        # 2. Visualizations
                        st.subheader("📈 Score Distribution")
                        plt.figure(figsize=(10, 5))
                        sns.barplot(x="score", y="name", data=df, palette="viridis")
                        plt.xlabel("Match Score (%)")
                        plt.ylabel("Candidate Name")
                        st.pyplot(plt)
                        
                        # 3. Detailed View
                        st.subheader("🔍 Detailed Insights")
                        for _, row in df.iterrows():
                            with st.expander(f"Candidate: {row['name']} Details ({row['score']}%)"):
                                col_a, col_b, col_c = st.columns([1, 1, 2])
                                with col_a:
                                    st.write(f"**Semantic (50%):** {row['semantic_score']}%")
                                    st.write(f"**Skills (30%):** {row['skill_score']}%")
                                    st.write(f"**Keywords (20%):** {row['keyword_score']}%")
                                with col_b:
                                    st.write(f"**Relevance:** {row['relevance']}")
                                    st.write("**Extracted Skills:**")
                                    st.write(", ".join(row['skills']) if row['skills'] else "None found")
                                with col_c:
                                    st.write("**Missing Demanded Skills:**")
                                    if len(row.get('missing_skills', [])) > 0:
                                        for ms in row['missing_skills']:
                                            st.error(f"❌ {ms}")
                                    else:
                                        st.success("✅ Perfect Match with Demanded Skills!")
                                    
                else:
                    st.error(f"Backend Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Failed to connect to the backend: {str(e)}")
                st.info("Hint: Make sure the FastAPI backend is running at http://localhost:8000")

# Footer
st.markdown("---")
st.caption("AI Resume Screening System - Built with FastAPI & Streamlit")
