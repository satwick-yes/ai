import spacy
import re
import string
import logging

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logging.warning("spaCy model 'en_core_web_sm' not found. Installing now...")
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Predefined skills list for academic submission
SKILL_DB = {
    "python", "java", "c++", "c#", "javascript", "react", "node.js", "angular", "vue",
    "html", "css", "sql", "nosql", "mongodb", "postgresql", "mysql", "aws", "azure", "gcp",
    "docker", "kubernetes", "git", "ci/cd", "agile", "scrum", "machine learning", "ai",
    "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn",
    "flask", "django", "fastapi", "spring boot", "pandas", "numpy", "data analysis",
    "leadership", "communication", "teamwork", "problem solving", "management",
    "project management", "streamlit", "rest api", "graphql", "seaborn", "matplotlib"
}

def clean_text(text):
    """
    Cleans text: lowercase, remove punctuation (keeping tech symbols), 
    removes stopwords, and performs lemmatization.
    """
    if not text:
        return ""
    
    text = text.lower()
    
    # Remove special characters but keep symbols core to tech skills
    # Replace newlines, tabs
    text = re.sub(r'[\r\n\t]', ' ', text)
    
    # Remove punctuation except for things like . # + (for c++, c#, node.js)
    custom_punctuation = string.punctuation.replace('+', '').replace('#', '').replace('.', '')
    text = text.translate(str.maketrans('', '', custom_punctuation))
    
    # Process with spaCy for lemmatization and stopword removal
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.text.strip()]
    
    return " ".join(tokens)

def extract_skills(text):
    """
    Extracts matching skills from text based on the SKILL_DB.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    found_skills = set()
    
    for skill in SKILL_DB:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    return sorted(list(found_skills))
