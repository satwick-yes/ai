from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import re
import spacy
import yake
from duckduckgo_search import DDGS

print("Loading semantic models, this may take a moment...")
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    st_model = SentenceTransformer('all-MiniLM-L6-v2')
    nlp = spacy.load("en_core_web_sm")

SKILL_NORMALIZATION_MAP = {
    "Py": "Python",
    "Js": "JavaScript",
    "Ts": "TypeScript",
    "Aws": "AWS",
    "Gcp": "Google Cloud",
    "Ml": "Machine Learning",
    "Ai": "Artificial Intelligence",
    "Nlp": "Natural Language Processing"
}

# Basic Stopwords for fallback if NLTK is not available
STOPWORDS = set([
    "a", "an", "the", "and", "or", "but", "if", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", 
    "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", 
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", 
    "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", 
    "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "i", 
    "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", 
    "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", 
    "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", 
    "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing"
])

def preprocess_text(text):
    """
    Minimalist preprocessing: lowercase, remove symbols, and filter stopwords.
    Avoids heavy dependencies like spaCy/Torch to ensure compatibility.
    """
    # Lowercase and remove punctuation/special characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Tokenize by whitespace
    tokens = text.split()
    
    # Remove stopwords and short tokens
    cleaned_tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    
    return " ".join(cleaned_tokens)

def calculate_hybrid_similarity(job_description, resumes_text_list, web_skills=None):
    """
    Compute hybrid similarity: 50% Semantic (MiniLM), 30% Skill Match, 20% TF-IDF Match.
    """
    if not resumes_text_list:
        return []

    # 1. Semantic Embedding Match (50%)
    jd_embedding = st_model.encode(job_description, convert_to_tensor=True)
    res_embeddings = st_model.encode(resumes_text_list, convert_to_tensor=True)
    semantic_scores = util.cos_sim(jd_embedding, res_embeddings)[0].cpu().numpy()

    # 2. Skill Extraction (Ontology)
    jd_skills = set(extract_skills(job_description))
    if web_skills:
        jd_skills.update(web_skills)
        
    # 3. TF-IDF Keyword Match (20%)
    processed_jd = preprocess_text(job_description)
    processed_resumes = [preprocess_text(rt) for rt in resumes_text_list]
    corpus = [processed_jd] + processed_resumes
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        keyword_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    except Exception:
        keyword_scores = np.zeros(len(resumes_text_list))
        
    final_results = []
    
    for i, resume_text in enumerate(resumes_text_list):
        resume_skills = set(extract_skills(resume_text))
        
        # Semantic
        sem_score = float(max(0, semantic_scores[i]))
        
        # Keyword 
        kw_score = float(keyword_scores[i])
        
        # Skill Match
        if not jd_skills:
            skill_score = 0.0
            matched_skills = []
            missing_skills = []
            w_sem, w_skill, w_kw = 0.8, 0.0, 0.2
        else:
            matches = jd_skills.intersection(resume_skills)
            skill_score = len(matches) / len(jd_skills)
            matched_skills = list(matches)
            missing_skills = list(jd_skills - matches)
            w_sem, w_skill, w_kw = 0.5, 0.3, 0.2

        total_score = (sem_score * w_sem) + (skill_score * w_skill) + (kw_score * w_kw)
        
        final_results.append({
            "total_score": round(total_score, 4),
            "semantic_score": round(sem_score, 4),
            "skill_score": round(skill_score, 4),
            "keyword_score": round(kw_score, 4),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extracted_skills": list(resume_skills)
        })
        
    return final_results

def extract_skills(text):
    """
    A comprehensive skill extraction function using regex matching.
    """
    common_skills = [
        # Languages
        "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "HTML", "CSS", "SQL", "NoSQL", "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin", "R",
        # Web Frameworks
        "FastAPI", "Flask", "Django", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Next.js", "Sprint Boot", "Laravel", "ASP.NET",
        # Data & AI
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", "PyTorch", "Keras", "Scikit-Learn", "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "Data Analysis", "Data Science", "Statistics", "Big Data", "Hadoop", "Spark", "Tableau", "Power BI", "Excel",
        # Cloud & DevOps
        "AWS", "Azure", "Google Cloud", "DigitalOcean", "Docker", "Kubernetes", "Git", "Jenkins", "Terraform", "CI/CD", "Linux", "Nginx",
        # Databases
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Elasticsearch", "Firebase",
        # Design & Soft Skills
        "Figma", "UI/UX", "Adobe XD", "Project Management", "Agile", "Scrum", "Communication", "Leadership", "Teamwork", "Problem Solving"
    ]
    
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        # Match with word boundaries
        if re.search(rf"\b{re.escape(skill.lower())}\b", text_lower):
            found_skills.append(skill)
            
    # Universal Extraction using spaCy (NER)
    try:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"] and len(ent.text) > 2:
                kw_title = ent.text.title()
                normalized_kw = SKILL_NORMALIZATION_MAP.get(kw_title, kw_title)
                if normalized_kw.lower() not in [s.lower() for s in found_skills]:
                    found_skills.append(normalized_kw)
    except Exception as e:
        pass

    # Universal Extraction for ALL job types out there using YAKE
    try:
        kw_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=8, features=None)
        keywords = kw_extractor.extract_keywords(text)
        for kw, score in keywords:
             if len(kw) > 3:
                kw_title = kw.title()
                normalized_kw = SKILL_NORMALIZATION_MAP.get(kw_title, kw_title)
                if normalized_kw.lower() not in [s.lower() for s in found_skills]:
                    found_skills.append(normalized_kw)
    except Exception as e:
        print(f"YAKE extraction failed: {e}")
        
    return list(dict.fromkeys(found_skills))

def expand_job_with_web_skills(job_description):
    """
    Search the web for the given job description to find commonly required skills.
    Returns a list of extracted skills.
    """
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            results = DDGS().text(f"{job_description} resume required skills", max_results=3)
        
        if results:
            combined_text = " ".join([res.get("body", "") + " " + res.get("title", "") for res in results])
            return extract_skills(combined_text)
    except Exception as e:
        print(f"DDG Web search failed: {e}")
        
    # Fallback to MediaWiki API (Wikipedia) if DDG returns empty
    try:
        import urllib.request
        import urllib.parse
        import json
        
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&exlimit=1&titles={urllib.parse.quote(job_description)}&explaintext=1&format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            pages = data.get('query', {}).get('pages', {})
            extract = list(pages.values())[0].get('extract', '')
            if extract:
                return extract_skills(extract)
    except Exception as e:
        print(f"Wikipedia Fallback search failed: {e}")
        
    return []
