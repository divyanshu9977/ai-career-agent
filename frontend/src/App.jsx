import { useEffect, useState } from 'react'
import axios from 'axios'
import { BriefcaseBusiness, FileText, Sparkles, Search, MessageCircle, Upload, MapPin, ArrowUpRight, LoaderCircle, Target, Send, CheckCircle2 } from 'lucide-react'

const API = 'http://localhost:8000'
export default function App() {
  const [tab, setTab] = useState('overview')
  const [jobs, setJobs] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [resume, setResume] = useState(null)
  const [skills, setSkills] = useState([])
  const [resumeText, setResumeText] = useState('')
  const [query, setQuery] = useState('')
  const [chatInput, setChatInput] = useState('')
  const [messages, setMessages] = useState([{role:'assistant', text:'Hi! I am CareerMate. Upload your resume to get personalized job recommendations, or ask me a career question.'}])
  const [loading, setLoading] = useState(false)
  const [notice, setNotice] = useState('')
  const [error, setError] = useState('')
  const [selectedJob, setSelectedJob] = useState(null)

  useEffect(() => { loadJobs() }, [])
  async function loadJobs() { try { const r = await axios.get(`${API}/api/jobs`); setJobs(r.data) } catch { setError('Cannot connect to backend. Start the FastAPI server on port 8000.') } }
  async function uploadResume(e) {
    const file = e.target.files?.[0]; if (!file) return
    setLoading(true); setError(''); setNotice('')
    const data = new FormData(); data.append('file', file)
    try {
      const r = await axios.post(`${API}/api/resume/analyze`, data)
      setResume(file.name); setSkills(r.data.skills); setResumeText(r.data.preview)
      const rec = await axios.post(`${API}/api/recommendations`, {})
      setRecommendations(rec.data); setNotice('Resume analyzed. Your job matches are ready.')
      setTab('matches')
    } catch (e) { setError(e.response?.data?.detail || 'Resume upload failed.') }
    finally { setLoading(false) }
  }
  async function search() {
    if (!query.trim()) return
    setLoading(true); setError('')
    try { const r = await axios.get(`${API}/api/search`, {params:{q:query}}); setRecommendations(r.data); setTab('matches') }
    catch { setError('Search failed. Check that the backend is running.') }
    finally { setLoading(false) }
  }
  async function sendChat(e) {
    e.preventDefault(); if (!chatInput.trim()) return
    const question = chatInput; setChatInput('')
    setMessages(m => [...m, {role:'user', text:question}]); setLoading(true)
    try {
      const r = await axios.post(`${API}/api/chat`, {message:question, skills, resume_text:resumeText})
      setMessages(m => [...m, {role:'assistant', text:r.data.answer}])
    } catch { setMessages(m => [...m, {role:'assistant', text:'I could not reach the backend. Please try again.'}]) }
    finally { setLoading(false) }
  }
  const displayedJobs = recommendations.length ? recommendations : jobs
  return <div className="app">
    <aside className="sidebar">
      <div className="brand"><div className="brand-icon"><Sparkles size={20}/></div><span>CareerMate<span className="ai"> AI</span></span></div>
      <div className="nav-label">WORKSPACE</div>
      {[['overview','Overview',Target],['matches','Job matches',BriefcaseBusiness],['assistant','Career assistant',MessageCircle]].map(([id,label,Icon]) =>
        <button key={id} className={`nav ${tab===id?'active':''}`} onClick={()=>setTab(id)}><Icon size={18}/>{label}</button>)}
      <div className="sidebar-bottom"><div className="mini-card"><Sparkles size={17}/><b>Build your next move</b><p>Upload your resume to unlock personalized recommendations.</p></div><span className="muted tiny">AI Career Agent · Demo</span></div>
    </aside>
    <main className="main">
      <header className="topbar"><div><span className="muted">Workspace</span><span className="slash"> / </span>{tab==='overview'?'Overview':tab==='matches'?'Job matches':'Career assistant'}</div><div className="avatar">CA</div></header>
      <div className="content">
        {error && <div className="alert error">{error}</div>}{notice && <div className="alert success"><CheckCircle2 size={16}/>{notice}</div>}
        {tab === 'details' && selectedJob && (
  <div className="details-page">
    <button
      className="text-btn"
      onClick={() => setTab('matches')}
    >
      ← Back to jobs
    </button>

    <div className="page-title">
      <div className="eyebrow">
        <BriefcaseBusiness size={14}/> JOB DETAILS
      </div>

      <h1>{selectedJob.title}</h1>
      <p className="muted">
        {selectedJob.company} · {selectedJob.location} · {selectedJob.job_type}
      </p>
    </div>

    <div className="details-card">
      <h2>Job description</h2>
      <p>{selectedJob.description || 'No description available.'}</p>

      <h2>Required skills</h2>
      <div className="tags">
        {(selectedJob.skills || '')
          .split(',')
          .filter(Boolean)
          .map(s => <span key={s}>{s.trim()}</span>)}
      </div>

      {selectedJob.match_score !== undefined && (
        <>
          <h2>Your match score</h2>
          <p>{selectedJob.match_score}%</p>
        </>
      )}

      {selectedJob.matched_skills?.length > 0 && (
        <>
          <h2>Skills you already have</h2>
          <p>{selectedJob.matched_skills.join(', ')}</p>
        </>
      )}

      <a
        className="apply-button"
        href={selectedJob.apply_url || undefined}
        target="_blank"
        rel="noreferrer"
        onClick={e => {
          if (!selectedJob.apply_url) e.preventDefault()
        }}
      >
        {selectedJob.apply_url ? 'Apply for this job' : 'Application link unavailable'}
        <ArrowUpRight size={16}/>
      </a>
    </div>
  </div>
)}
        {tab==='overview' && <>
          <div className="welcome"><div><div className="eyebrow"><Sparkles size={14}/> YOUR AI-POWERED CAREER COMPANION</div><h1>Find the work<br/><span>you’re meant for.</span></h1><p>Turn your resume into a personalized career roadmap. Discover relevant roles and understand what skills to build next.</p><div className="searchbar"><Search size={19}/><input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&search()} placeholder="Search roles, skills, or technologies..."/><button onClick={search}>Search jobs</button></div></div><div className="hero-art"><div className="orbit orbit1"></div><div className="orbit orbit2"></div><div className="hero-center"><Sparkles size={38}/></div><div className="float-card card-one"><Target size={16}/> Skill match <b>AI-powered</b></div><div className="float-card card-two"><BriefcaseBusiness size={16}/> Career paths <b>Personalized</b></div></div></div>
          <div className="section-head"><div><h2>Your career dashboard</h2><p className="muted">A quick look at your job discovery journey.</p></div></div>
          <div className="stats"><div className="stat"><span className="stat-icon purple"><BriefcaseBusiness/></span><div><strong>{jobs.length}</strong><span>Sample jobs</span></div></div><div className="stat"><span className="stat-icon blue"><FileText/></span><div><strong>{resume?'1':'0'}</strong><span>Resume uploaded</span></div></div><div className="stat"><span className="stat-icon green"><Target/></span><div><strong>{recommendations.length}</strong><span>Ranked matches</span></div></div></div>
          <div className="section-head"><div><h2>Get started</h2><p className="muted">Three steps to a more focused job search.</p></div></div>
          <div className="steps"><div className="step"><span>01</span><FileText/><h3>Upload your resume</h3><p>We extract your skills and experience from a PDF.</p><label className="upload-btn"><Upload size={16}/> {loading?'Analyzing...':'Choose PDF'}<input type="file" accept=".pdf,application/pdf" onChange={uploadResume} disabled={loading}/></label></div><div className="step"><span>02</span><Target/><h3>Explore your matches</h3><p>See ranked jobs and the skills that overlap with your profile.</p><button className="text-btn" onClick={()=>setTab('matches')}>View jobs <ArrowUpRight size={15}/></button></div><div className="step"><span>03</span><MessageCircle/><h3>Ask your career agent</h3><p>Get practical guidance for interviews and skill gaps.</p><button className="text-btn" onClick={()=>setTab('assistant')}>Chat with AI <ArrowUpRight size={15}/></button></div></div>
          <div className="section-head"><div><h2>Recently added opportunities</h2><p className="muted">Explore roles from our sample job catalogue.</p></div><button className="text-btn" onClick={()=>setTab('matches')}>See all <ArrowUpRight size={15}/></button></div>
          <div className="job-list">
  {jobs.slice(0,3).map(j => (
    <JobCard
      key={j.id}
      job={j}
      onDetails={(job) => {
        setSelectedJob(job)
        setTab('details')
      }}
    />
  ))}
</div>
        </>}
        {tab==='matches' && <><div className="page-title"><div className="eyebrow"><Target size={14}/> DISCOVER OPPORTUNITIES</div><h1>Jobs that match <span>your ambition.</span></h1><p className="muted">Ranked by relevance to your resume or search query.</p></div><div className="toolbar"><div className="searchbar compact"><Search size={18}/><input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&search()} placeholder="Try Python, AI engineer, SQL..."/><button onClick={search}>Search</button></div><label className="upload-btn"><Upload size={16}/> Upload resume<input type="file" accept=".pdf" onChange={uploadResume}/></label></div>{skills.length>0&&<div className="skill-strip"><b>Detected skills</b>{skills.map(s=><span key={s}>{s}</span>)}</div>}<div className="results-label">{displayedJobs.length} opportunities {recommendations.length?'ranked for you':'available'}</div><div className="job-list">{displayedJobs.map(j=><JobCard key={j.id} job={j}/>)}</div></>}
        {tab==='assistant' && <div className="chat-page"><div className="page-title"><div className="eyebrow"><Sparkles size={14}/> YOUR PERSONAL CAREER GUIDE</div><h1>Let’s plan your <span>next step.</span></h1><p className="muted">Ask about your resume, skills, job search or interview preparation.</p></div><div className="chatbox"><div className="chat-head"><div className="bot-avatar"><Sparkles/></div><div><b>CareerMate</b><small><span className="online"></span> Career assistant</small></div><span className="powered">AI ASSISTANT</span></div><div className="messages">{messages.map((m,i)=><div key={i} className={`message ${m.role}`}><div className="bubble">{m.text}</div></div>)}{loading&&<div className="message assistant"><div className="bubble typing"><LoaderCircle size={15}/> Thinking...</div></div>}</div><div className="suggestions">{['How can I improve my resume?','Prepare me for a backend interview','What skills should I learn next?'].map(s=><button key={s} onClick={()=>setChatInput(s)}>{s}</button>)}</div><form className="chat-form" onSubmit={sendChat}><input value={chatInput} onChange={e=>setChatInput(e.target.value)} placeholder="Ask CareerMate anything..."/><button disabled={loading}><Send size={17}/></button></form></div></div>}
      </div>
    </main>
  </div>
}
function JobCard({ job, onDetails }) {
  return (
    <article className="job-card">
      <div className="company-mark">
        {job.company?.slice(0, 1) || 'J'}
      </div>

      <div className="job-info">
        <div className="job-title-row">
          <h3>{job.title}</h3>

          {job.match_score !== undefined && (
            <span className="match">{job.match_score}% match</span>
          )}
        </div>

        <div className="company">
          {job.company} <span>·</span>
          <MapPin size={13}/> {job.location}
          <span>·</span> {job.job_type}
        </div>

        <p>{job.description}</p>

        <div className="tags">
          {(job.skills || '').split(',').slice(0, 6).map(s => (
            <span key={s}>{s.trim()}</span>
          ))}
        </div>

        {job.matched_skills?.length > 0 && (
          <div className="matched">
            Matched: {job.matched_skills.join(', ')}
          </div>
        )}
      </div>

      <button
        className="apply details-btn"
        onClick={() => onDetails(job)}
      >
        Details <ArrowUpRight size={15}/>
      </button>
    </article>
  )
}
