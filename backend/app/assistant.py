import os
from dotenv import load_dotenv
load_dotenv()

SYSTEM_PROMPT = """You are CareerMate, a practical career assistant. Help the candidate improve their resume,
prepare for interviews, identify skill gaps and plan learning. Be honest: do not invent experience,
job openings, qualifications or guarantees. Keep answers actionable and concise."""

def local_reply(message: str, skills: list[str], resume_text: str) -> str:
    q = message.lower()
    if any(w in q for w in ["skill gap", "missing skill", "improve", "learn"]):
        if skills:
            return ("Your detected skills include: " + ", ".join(skills[:15]) +
                    ". Compare these with each target job's required skills. Prioritize one missing "
                    "core skill at a time, build a small demonstrable project, and add evidence to your resume.")
        return "Upload your resume first. I can then identify detected skills and suggest a focused learning plan."
    if any(w in q for w in ["interview", "prepare"]):
        return ("For a software engineering interview, prepare: data structures and algorithms, OOP, DBMS, "
                "OS, computer networks, REST APIs, and a detailed explanation of each resume project. "
                "Practice explaining the problem, architecture, trade-offs and your individual contribution.")
    if any(w in q for w in ["resume", "cv"]):
        return ("Use impact-focused bullets: action + technology + measurable outcome. Keep claims factual, "
                "include project links, and tailor the skills and project order to the job description.")
    return ("I can help with resume improvements, skill-gap analysis, job matching and interview preparation. "
            "Try asking: 'What skills should I learn next?' or 'How should I prepare for a backend interview?'")

async def generate_reply(message: str, skills: list[str], resume_text: str) -> str:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        return local_reply(message, skills, resume_text)
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=key)
        context = f"Candidate skills: {', '.join(skills)}\\nResume excerpt: {resume_text[:5000]}"
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": context + "\\nQuestion: " + message}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content or "I couldn't generate a response."
    except Exception as exc:
        return "The AI service could not be reached, so here is the local assistant response. " + local_reply(message, skills, resume_text)
