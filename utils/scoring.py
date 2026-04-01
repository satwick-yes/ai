from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

def calculate_similarity(jd_text, resume_texts):
    """
    Calculates TF-IDF cosine similarity between the Job Description and a list of Resumes.
    """
    if not jd_text or not resume_texts:
        return [0.0] * len(resume_texts)

    documents = [jd_text] + resume_texts
    
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
    except Exception as e:
        logging.error(f"Error in TF-IDF: {e}")
        return [0.0] * len(resume_texts)
        
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return [round(float(score) * 100, 2) for score in cosine_sim[0]]
