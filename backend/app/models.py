from sqlalchemy import Column, Integer, String, Text, Float
from .database import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    location = Column(String(200), default="India")
    job_type = Column(String(100), default="Full-time")
    description = Column(Text, nullable=False)
    skills = Column(Text, default="")
    apply_url = Column(String(500), default="")

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), default="Candidate")
    email = Column(String(200), default="")
    resume_text = Column(Text, default="")
    skills = Column(Text, default="")
