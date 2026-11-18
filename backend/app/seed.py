from sqlalchemy.orm import Session
from .models import Job

SAMPLE_JOBS = [
    ("Python Backend Intern", "TechNova", "Bengaluru", "Internship",
     "Build REST APIs using Python and FastAPI. Work with SQL databases, authentication, testing, Docker and cloud deployment.",
     "Python, FastAPI, REST APIs, SQL, SQLite, PostgreSQL, Docker, Git"),
    ("Junior AI Engineer", "MindWorks AI", "Remote", "Full-time",
     "Develop LLM-powered applications, prompt workflows, retrieval augmented generation, embeddings and vector search systems.",
     "Python, LLM, RAG, embeddings, vector database, OpenAI, NLP, FastAPI"),
    ("Data Analyst", "Insight Labs", "Gurugram", "Full-time",
     "Analyze business datasets, write SQL queries, create dashboards and communicate insights using Python and visualization tools.",
     "Python, SQL, Pandas, NumPy, Excel, Power BI, statistics"),
    ("Frontend Developer Intern", "PixelCraft", "Remote", "Internship",
     "Create responsive user interfaces with React, JavaScript, HTML and CSS. Integrate APIs and collaborate with backend engineers.",
     "React, JavaScript, HTML, CSS, REST APIs, Git"),
    ("Machine Learning Intern", "DataSpring", "Pune", "Internship",
     "Prepare datasets, train classification and regression models, evaluate model performance and deploy basic ML services.",
     "Python, scikit-learn, Pandas, NumPy, Machine Learning, FastAPI"),
    ("Software Engineer", "CloudBridge", "Hyderabad", "Full-time",
     "Develop backend services, design APIs, optimize SQL queries and write maintainable code with testing and version control.",
     "C++, Python, Java, SQL, APIs, Data Structures, Git, Docker"),
    ("NLP Engineer Intern", "LanguageAI", "Remote", "Internship",
     "Work on text processing, semantic search, transformer models, sentence embeddings and evaluation of NLP systems.",
     "Python, NLP, transformers, embeddings, PyTorch, semantic search"),
    ("Full Stack Developer", "BuildStack", "Noida", "Full-time",
     "Build web applications using React, Node.js, Express and MongoDB. Implement authentication, APIs and responsive interfaces.",
     "React, Node.js, Express, MongoDB, JavaScript, REST APIs")
]

def seed_jobs(db: Session):
    if db.query(Job).count() == 0:
        for title, company, location, job_type, description, skills in SAMPLE_JOBS:
            db.add(Job(title=title, company=company, location=location, job_type=job_type,
                       description=description, skills=skills))
        db.commit()
