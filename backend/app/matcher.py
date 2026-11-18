import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_skills(text: str) -> list[str]:
    parts = re.split(r"[,|;\\n]", text or "")
    return sorted({p.strip().lower() for p in parts if p.strip()})

def score_jobs(resume_text: str, jobs: list):
    resume_text = resume_text or ""
    docs = [resume_text] + [
        f"{j.title}. {j.description}. Required skills: {j.skills}" for j in jobs
    ]
    if not resume_text.strip():
        return [{"job": j, "score": 0, "matched_skills": []} for j in jobs]
    try:
        matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(docs)
        scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    except ValueError:
        scores = [0.0] * len(jobs)

    results = []
    resume_lower = resume_text.lower()
    for job, score in zip(jobs, scores):
        required = clean_skills(job.skills)
        matched = [s for s in required if s in resume_lower]
        # Blend document similarity with transparent skill overlap.
        skill_score = len(matched) / max(1, len(required))
        final_score = min(100, round(float(score) * 65 + skill_score * 35))
        results.append({"job": job, "score": final_score, "matched_skills": matched})
    return sorted(results, key=lambda x: x["score"], reverse=True)
