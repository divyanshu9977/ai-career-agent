import fitz
import re

def extract_pdf_text(content: bytes) -> str:
    doc = fitz.open(stream=content, filetype="pdf")
    text = "\\n".join(page.get_text("text") for page in doc)
    return re.sub(r"\\n{3,}", "\\n\\n", text).strip()

KNOWN_SKILLS = [
    "python", "c++", "java", "javascript", "react", "node.js", "express",
    "html", "css", "sql", "mysql", "postgresql", "mongodb", "fastapi",
    "machine learning", "deep learning", "nlp", "llm", "rag", "embeddings",
    "docker", "git", "pandas", "numpy", "scikit-learn", "tensorflow",
    "pytorch", "rest api", "data structures", "figma", "power bi"
]

def detect_skills(text: str) -> list[str]:
    lower = text.lower()
    return [skill for skill in KNOWN_SKILLS if skill in lower]
