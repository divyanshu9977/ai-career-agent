from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .database import Base, engine, get_db
from .models import Job, CandidateProfile
from .schemas import JobCreate, ChatRequest
from .seed import seed_jobs
from .resume import extract_pdf_text, detect_skills
from .matcher import score_jobs
from .assistant import generate_reply

app = FastAPI(title="AI Career Agent API", version="1.0.0",
              description="Resume analysis, job matching, semantic-style search and career assistant.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_jobs(db)
    finally:
        db.close()

def job_dict(job, score=None, matched=None):
    data = {"id": job.id, "title": job.title, "company": job.company,
            "location": job.location, "job_type": job.job_type,
            "description": job.description, "skills": job.skills, "apply_url": job.apply_url}
    if score is not None:
        data["match_score"] = score
        data["matched_skills"] = matched or []
    return data

@app.get("/")
def root():
    return {"message": "AI Career Agent API is running", "docs": "/docs"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/jobs")
def list_jobs(q: str = "", location: str = "", db: Session = Depends(get_db)):
    query = db.query(Job)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Job.title.ilike(like), Job.description.ilike(like), Job.skills.ilike(like)))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    return [job_dict(j) for j in query.order_by(Job.id.desc()).all()]

@app.post("/api/jobs")
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job = Job(**payload.model_dump())
    db.add(job); db.commit(); db.refresh(job)
    return job_dict(job)

@app.post("/api/resume/analyze")
async def analyze_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF resume.")
    content = await file.read()
    if len(content) > 8 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File must be smaller than 8 MB.")
    try:
        text = extract_pdf_text(content)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read this PDF. Try another PDF file.")
    if not text:
        raise HTTPException(status_code=400, detail="No selectable text found. Scanned PDFs need OCR.")
    skills = detect_skills(text)
    profile = db.query(CandidateProfile).first()
    if not profile:
        profile = CandidateProfile()
        db.add(profile)
    profile.resume_text = text
    profile.skills = ", ".join(skills)
    db.commit()
    return {"filename": file.filename, "characters": len(text), "skills": skills,
            "preview": text[:1600], "message": "Resume analyzed successfully."}

@app.post("/api/recommendations")
def recommendations(payload: dict, db: Session = Depends(get_db)):
    resume_text = payload.get("resume_text", "")
    if not resume_text:
        profile = db.query(CandidateProfile).first()
        resume_text = profile.resume_text if profile else ""
    if not resume_text:
        raise HTTPException(status_code=400, detail="Upload a resume before requesting recommendations.")
    jobs = db.query(Job).all()
    ranked = score_jobs(resume_text, jobs)
    return [job_dict(x["job"], x["score"], x["matched_skills"]) for x in ranked]

@app.get("/api/search")
def search_jobs(q: str, db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    # Search across title, description and skills using the same text-ranking pipeline.
    proxy = type("SearchProfile", (), {"title": "Search", "description": q, "skills": ""})()
    ranked = score_jobs(q, jobs)
    return [job_dict(x["job"], x["score"], x["matched_skills"]) for x in ranked if x["score"] > 0]

@app.post("/api/chat")
async def chat(payload: ChatRequest):
    answer = await generate_reply(payload.message, payload.skills, payload.resume_text)
    return {"answer": answer}
