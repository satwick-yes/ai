# AI Resume Screening & Candidate Ranking System

## 📌 Project Overview
The **AI Resume Screening & Candidate Ranking System** is an automated tool designed to evaluate and rank candidate resumes against a specific job description. This full-stack application uses Natural Language Processing (NLP) to extract text, clean data (lemmatization & stopword removal), and calculate a match score using TF-IDF vectorization and Cosine Similarity.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **NLP Models**: spaCy (Preprocessing), Scikit-Learn (TF-IDF & Cosine Similarity)
- **File Parsing**: PyPDF2, python-docx
- **Analysis**: Pandas, Matplotlib, Seaborn

## 📂 Project Structure
- `/data`: Stores sample and uploaded resumes for processing.
- `/backend`: Contains the FastAPI application (`main.py`).
- `/frontend`: Contains the Streamlit user interface (`ui.py`).
- `/notebooks`: Development and evaluation notebook.
- `/utils`: Core logic for text extraction, NLP pipeline, and scoring.
- `requirements.txt`: Project dependencies.

## 🚀 Setup & Execution

### 1. Installation
Ensure you have Python 3.9+ installed. Run the following command to install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Running the Backend (FastAPI)
Navigate to the root directory and start the API:
```bash
python -m backend.main
```
The backend will run on `http://localhost:8000`. You can visit `http://localhost:18000/docs` for API documentation.

### 3. Running the Frontend (Streamlit)
Open a new terminal window and start the UI:
```bash
streamlit run frontend/ui.py
```
The dashboard will open in your default browser at `http://localhost:8501`.

## 📊 Key Features
- **Multi-Format Support**: Upload PDF and DOCX files.
- **Advanced Preprocessing**: Uses spaCy for tokenization and lemmatization.
- **Skill Extraction**: Automatically identifies matching and missing skills based on a predefined database.
- **Interactive Ranking**: Visualize candidate scores in a clean table with progress bars.

---
**Academic Project Build - AI Resume Screening System - 2026**
