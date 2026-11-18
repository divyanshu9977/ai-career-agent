from pydantic import BaseModel, Field

class JobCreate(BaseModel):
    title: str
    company: str
    location: str = "India"
    job_type: str = "Full-time"
    description: str
    skills: str = ""
    apply_url: str = ""

class ChatRequest(BaseModel):
    message: str
    resume_text: str = ""
    skills: list[str] = Field(default_factory=list)
