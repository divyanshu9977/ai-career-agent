# AI Career Agent (CareerMate)

A full-stack portfolio project for resume analysis, job discovery, job ranking and career guidance.

## Features
- PDF resume text extraction (PyMuPDF)
- Skill detection from a transparent starter skill dictionary
- Job catalogue stored in SQLite, seeded with sample jobs
- Resume-to-job ranking using TF-IDF similarity plus skill overlap
- Search across job descriptions and skills
- Career assistant with optional OpenAI API; local fallback works without an API key
- React dashboard with overview, matches and chat pages

> This is a portfolio/demo application. The included jobs are sample data, not verified live vacancies. The matching score is a heuristic relevance score, not a hiring probability. Scanned PDFs need OCR and are not supported by the initial version.

## Requirements
- Python 3.10+
- Node.js 18+

## Run the backend
```bash
cd backend
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

Optional LLM:
1. Open `backend/.env`
2. Set `OPENAI_API_KEY=your_key`
3. Restart the backend

Without a key, the app uses a local career assistant.

## Run the frontend
In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

## Try it
1. Visit the dashboard.
2. Upload a text-based PDF resume (up to 8 MB).
3. Review detected skills and ranked jobs.
4. Search for roles such as `Python`, `AI`, `React`, or `SQL`.
5. Ask CareerMate about resume improvements or interview preparation.

## API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/jobs` | List jobs |
| POST | `/api/jobs` | Add a job |
| POST | `/api/resume/analyze` | Upload and analyze PDF |
| POST | `/api/recommendations` | Rank jobs for resume |
| GET | `/api/search?q=python` | Search jobs |
| POST | `/api/chat` | Ask career assistant |

## Project structure
```text
ai-career-agent/
  backend/
    app/
      assistant.py
      database.py
      main.py
      matcher.py
      models.py
      resume.py
      schemas.py
      seed.py
    requirements.txt
    .env.example
  frontend/
    src/App.jsx
    src/main.jsx
    src/style.css
    index.html
    package.json
    vite.config.js
```

## Next improvements
- Replace sample jobs with a trusted live jobs API or admin-imported listings.
- Add user accounts and per-user resume storage/consent.
- Add OCR for scanned PDFs.
- Wire the optional Sentence Transformers utility into the ranking pipeline and add a persistent FAISS/Chroma vector index for scalable retrieval. Install `backend/requirements-ai.txt` to experiment with embeddings.
- Add automated tests, Docker deployment and LLM evaluation.
