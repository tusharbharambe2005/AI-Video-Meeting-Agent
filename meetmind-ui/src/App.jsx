import { useState, useRef, useEffect, useCallback } from 'react';
import { startAnalysis, pollStatus, sendChatMessage } from './api';

/* ── Icons (inline SVG components for zero-dep) ─────────────────────────── */
const Icon = {
  Zap: () => (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
    </svg>
  ),
  Mic: () => (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/>
    </svg>
  ),
  Brain: () => (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-1.16Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-1.16Z"/>
    </svg>
  ),
  MessageSquare: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
  ),
  Send: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
    </svg>
  ),
  AlertCircle: () => (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
  ),
  ChevronDown: () => (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="6 9 12 15 18 9"/>
    </svg>
  ),
  Copy: () => (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
    </svg>
  ),
  Check: () => (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  FileText: () => (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
    </svg>
  ),
  CheckSquare: () => (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
    </svg>
  ),
  Key: () => (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>
    </svg>
  ),
  HelpCircle: () => (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  ),
  ArrowRight: () => (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
    </svg>
  ),
};

/* ── Constants ──────────────────────────────────────────────────────────── */
const POLL_MS = 2000;

const STEPS = [
  'Processing audio',
  'Transcribing speech',
  'Generating title & summary',
  'Extracting action items, decisions & questions',
  'Building RAG knowledge base',
];

const TABS = [
  { id: 'summary',     label: 'Summary',      Icon: Icon.FileText },
  { id: 'actions',    label: 'Action Items', Icon: Icon.CheckSquare },
  { id: 'decisions',  label: 'Decisions',    Icon: Icon.Key },
  { id: 'questions',  label: 'Questions',    Icon: Icon.HelpCircle },
  { id: 'transcript', label: 'Transcript',   Icon: Icon.FileText },
];

const LANGUAGES = [
  { value: 'english',  label: 'English' },
  { value: 'hinglish', label: 'Hinglish' },
  { value: 'hindi',    label: 'Hindi' },
  { value: 'auto',     label: 'Auto-detect' },
];

function getActiveStep(log) {
  if (!log?.length) return -1;
  const last = log[log.length - 1].step;
  return STEPS.findIndex(s => last.toLowerCase().includes(s.split(' ')[0].toLowerCase()));
}

/* ── Navbar ─────────────────────────────────────────────────────────────── */
function Navbar() {
  return (
    <nav className="navbar" aria-label="Main navigation">
      <div className="container navbar-inner">
        <a href="#" className="logo" aria-label="MeetMind">
          <div className="logo-mark" aria-hidden="true">M</div>
          <span className="logo-name">Meet<em>Mind</em></span>
        </a>
        <div className="nav-pill">
          <span className="nav-pill-dot" aria-hidden="true" />
          AI Meeting Intelligence
        </div>
      </div>
    </nav>
  );
}

/* ── Hero ────────────────────────────────────────────────────────────────── */
function Hero() {
  return (
    <section className="hero" aria-labelledby="hero-heading">
      <div className="hero-eyebrow">
        <span className="hero-eyebrow-icon">⚡</span>
        Powered by Whisper · Mistral AI · ChromaDB
      </div>
      <h1 id="hero-heading">
        Meetings decoded,<br />
        <span className="grad">insights delivered</span>
      </h1>
      <p className="hero-sub">
        Paste any YouTube link or local video path. Get a clean transcript,
        AI summary, extracted action items, and a live RAG-powered chat.
      </p>
      <div className="hero-chips" role="list">
        {[
          [Icon.Mic,   'Speech-to-Text'],
          [Icon.Brain, 'AI Summarization'],
          [Icon.MessageSquare, 'RAG Chat'],
        ].map(([Ic, label]) => (
          <span key={label} className="hero-chip" role="listitem">
            <span className="hero-chip-icon"><Ic /></span>
            {label}
          </span>
        ))}
      </div>
    </section>
  );
}

/* ── Input Card ──────────────────────────────────────────────────────────── */
function AnalyseCard({ onAnalyse, busy }) {
  const [source,   setSource]   = useState('');
  const [language, setLanguage] = useState('english');

  const submit = (e) => {
    e.preventDefault();
    if (source.trim() && !busy) onAnalyse(source.trim(), language);
  };

  return (
    <section className="analyse-section" aria-label="Analysis input">
      <div className="container">
        <form className="input-card" onSubmit={submit} id="analyse-form">

          <div className="card-header">
            <div className="card-header-icon" aria-hidden="true">
              <Icon.Zap />
            </div>
            <span className="card-header-title">Source &amp; Settings</span>
          </div>

          <div className="fields-row">
            <div className="field">
              <label className="field-label" htmlFor="source-input">
                YouTube URL or file path
              </label>
              <input
                id="source-input"
                className="field-input"
                type="text"
                value={source}
                onChange={e => setSource(e.target.value)}
                placeholder="https://youtube.com/watch?v=...   or   /path/to/recording.mp4"
                disabled={busy}
                required
                autoComplete="off"
                spellCheck="false"
              />
            </div>

            <div className="field">
              <label className="field-label" htmlFor="language-select">Language</label>
              <div className="select-wrap">
                <select
                  id="language-select"
                  className="field-select"
                  value={language}
                  onChange={e => setLanguage(e.target.value)}
                  disabled={busy}
                >
                  {LANGUAGES.map(l => (
                    <option key={l.value} value={l.value}>{l.label}</option>
                  ))}
                </select>
                <span className="select-arrow" aria-hidden="true"><Icon.ChevronDown /></span>
              </div>
            </div>
          </div>

          <button
            id="analyse-btn"
            type="submit"
            className="btn-analyse"
            disabled={busy || !source.trim()}
          >
            {busy
              ? <><span className="btn-spinner" aria-hidden="true" /> Analysing…</>
              : <><Icon.Zap /> Analyse Meeting <Icon.ArrowRight /></>
            }
          </button>
        </form>
      </div>
    </section>
  );
}

/* ── Processing Panel ────────────────────────────────────────────────────── */
function ProcessingPanel({ progress, log }) {
  const active = getActiveStep(log);
  return (
    <div className="container">
      <div className="processing-card" role="status" aria-live="polite">
        <div className="processing-top">
          <div className="processing-label">
            <span className="btn-spinner" style={{ borderColor: 'rgba(99,102,241,0.3)', borderTopColor: '#818CF8' }} aria-hidden="true" />
            Analysing your meeting…
          </div>
          <span className="processing-pct">{progress}%</span>
        </div>

        <div className="progress-track"
          role="progressbar"
          aria-valuenow={progress}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label="Analysis progress"
        >
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>

        <div className="steps">
          {STEPS.map((label, i) => {
            const cls = i < active ? 'done' : i === active ? 'active' : '';
            const symbol = i < active ? '✓' : i === active ? '›' : String(i + 1);
            return (
              <div key={label} className={`step ${cls}`}>
                <div className="step-indicator" aria-hidden="true">{symbol}</div>
                <span className="step-label">{label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ── Error Banner ────────────────────────────────────────────────────────── */
function ErrorBanner({ message }) {
  return (
    <div className="container">
      <div className="error-banner" role="alert">
        <span className="error-icon"><Icon.AlertCircle /></span>
        <span><strong>Error — </strong>{message}</span>
      </div>
    </div>
  );
}

/* ── Bullet List ─────────────────────────────────────────────────────────── */
function BulletList({ items }) {
  if (!Array.isArray(items) || items.length === 0)
    return <p className="items-empty">No items found.</p>;
  return (
    <ul className="items-list" role="list">
      {items.map((text, i) => (
        <li key={i} className="item" role="listitem">
          <span className="item-dot" aria-hidden="true" />
          <span className="item-text">{text}</span>
        </li>
      ))}
    </ul>
  );
}

/* ── Transcript Tab ──────────────────────────────────────────────────────── */
function TranscriptPane({ text }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2200);
    });
  };
  return (
    <div className="transcript-wrap">
      <pre className="transcript-pre" tabIndex={0} aria-label="Full meeting transcript">{text}</pre>
      <button
        id="copy-transcript-btn"
        className={`copy-btn ${copied ? 'copied' : ''}`}
        onClick={copy}
      >
        {copied ? <Icon.Check /> : <Icon.Copy />}
        {copied ? 'Copied!' : 'Copy transcript'}
      </button>
    </div>
  );
}

/* ── Results Tabs ────────────────────────────────────────────────────────── */
function ResultTabs({ result }) {
  const [active, setActive] = useState('summary');

  return (
    <div>
      <nav className="tabs-header" role="tablist" aria-label="Analysis results">
        {TABS.map(({ id, label, Icon: TabIcon }) => (
          <button
            key={id}
            role="tab"
            id={`tab-${id}`}
            aria-selected={active === id}
            aria-controls={`panel-${id}`}
            className={`tab-btn ${active === id ? 'active' : ''}`}
            onClick={() => setActive(id)}
          >
            <span className="tab-btn-icon"><TabIcon /></span>
            {label}
          </button>
        ))}
      </nav>

      <div className="tab-body">
        <div
          id={`panel-${active}`}
          role="tabpanel"
          aria-labelledby={`tab-${active}`}
          className="tab-pane"
          key={active}
        >
          {active === 'summary'     && <p className="prose">{result.summary}</p>}
          {active === 'actions'     && <BulletList items={result.action_items} />}
          {active === 'decisions'   && <BulletList items={result.decisions} />}
          {active === 'questions'   && <BulletList items={result.questions} />}
          {active === 'transcript'  && <TranscriptPane text={result.transcript} />}
        </div>
      </div>
    </div>
  );
}

/* ── Chat ────────────────────────────────────────────────────────────────── */
function ChatSection({ jobId }) {
  const [msgs,      setMsgs]    = useState([]);
  const [input,     setInput]   = useState('');
  const [thinking,  setThinking]= useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [msgs, thinking]);

  const send = async () => {
    const q = input.trim();
    if (!q || thinking) return;
    setInput('');
    setMsgs(prev => [...prev, { role: 'user', text: q }]);
    setThinking(true);
    try {
      const res = await sendChatMessage(jobId, q);
      setMsgs(prev => [...prev, { role: 'bot', text: res.data.answer }]);
    } catch (err) {
      setMsgs(prev => [...prev, { role: 'bot', text: `Error: ${err.message}` }]);
    } finally {
      setThinking(false);
    }
  };

  const onKey = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } };

  return (
    <section className="chat-section" aria-label="Chat with your meeting">
      <div className="chat-topbar">
        <div className="chat-topbar-left">
          <div className="chat-topbar-icon" aria-hidden="true"><Icon.MessageSquare /></div>
          <span className="chat-topbar-title">Chat with your meeting</span>
        </div>
        <span className="chat-topbar-tag">RAG · Grounded answers</span>
      </div>

      <div className="chat-messages" role="log" aria-live="polite" aria-label="Chat messages">
        {msgs.length === 0 && !thinking && (
          <div className="chat-empty">
            <div className="chat-empty-icon" aria-hidden="true">💬</div>
            <p className="chat-empty-text">Ask anything about your meeting</p>
          </div>
        )}

        {msgs.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <div className="msg-avatar" aria-hidden="true">
              {m.role === 'user' ? 'U' : '🧠'}
            </div>
            <div className="msg-bubble">{m.text}</div>
          </div>
        ))}

        {thinking && (
          <div className="msg bot">
            <div className="msg-avatar" aria-hidden="true">🧠</div>
            <div className="msg-bubble">
              <div className="typing-dots" aria-label="Thinking">
                <span /><span /><span />
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chat-footer">
        <input
          id="chat-input"
          className="chat-input"
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={onKey}
          placeholder="What were the main decisions made?"
          disabled={thinking}
          aria-label="Chat message input"
        />
        <button
          id="chat-send-btn"
          className="chat-send"
          onClick={send}
          disabled={!input.trim() || thinking}
          aria-label="Send message"
        >
          <Icon.Send />
        </button>
      </div>
    </section>
  );
}

/* ── Results ─────────────────────────────────────────────────────────────── */
function ResultsSection({ result, jobId }) {
  const wc = result.transcript?.split(/\s+/).length ?? 0;
  const ai = Array.isArray(result.action_items) ? result.action_items.length : '—';
  const kd = Array.isArray(result.decisions)    ? result.decisions.length    : '—';
  const oq = Array.isArray(result.questions)    ? result.questions.length    : '—';

  return (
    <section className="results-section" aria-label="Analysis results">
      <div className="container">

        <div className="result-header">
          <h2 className="result-title">{result.title}</h2>
          <div className="stat-row" role="list">
            {[
              ['Words',        wc.toLocaleString()],
              ['Action Items', ai],
              ['Decisions',    kd],
              ['Questions',    oq],
            ].map(([label, val]) => (
              <span key={label} className="stat-badge" role="listitem">
                <span className="stat-badge-dot" aria-hidden="true" />
                {label}&nbsp;<strong className="stat-badge-val">{val}</strong>
              </span>
            ))}
          </div>
        </div>

        <ResultTabs result={result} />
        <ChatSection jobId={jobId} />

      </div>
    </section>
  );
}

/* ── Empty State ─────────────────────────────────────────────────────────── */
function EmptyState() {
  return (
    <div className="container">
      <div className="empty-state" aria-label="No analysis yet">
        <div className="empty-icon" aria-hidden="true">🎙️</div>
        <p className="empty-title">Ready to analyse</p>
        <p className="empty-sub">Paste a YouTube URL or local file path above and click Analyse</p>
      </div>
    </div>
  );
}

/* ── App ─────────────────────────────────────────────────────────────────── */
export default function App() {
  const [status,   setStatus]   = useState('idle');
  const [progress, setProgress] = useState(0);
  const [log,      setLog]      = useState([]);
  const [result,   setResult]   = useState(null);
  const [error,    setError]    = useState(null);
  const [jobId,    setJobId]    = useState(null);
  const pollRef = useRef(null);

  const stopPoll = () => { if (pollRef.current) { clearInterval(pollRef.current); pollRef.current = null; } };

  const startPoll = useCallback((id) => {
    stopPoll();
    pollRef.current = setInterval(async () => {
      try {
        const res  = await pollStatus(id);
        const data = res.data;
        setProgress(data.progress ?? 0);
        setLog(data.log ?? []);
        setStatus(data.status);
        if (data.status === 'done')  { setResult(data.result); stopPoll(); }
        if (data.status === 'error') { setError(data.error || 'Unknown error.'); stopPoll(); }
      } catch (e) {
        setError(`Polling failed: ${e.message}`);
        setStatus('error');
        stopPoll();
      }
    }, POLL_MS);
  }, []);

  useEffect(() => () => stopPoll(), []);

  const handleAnalyse = async (source, language) => {
    setStatus('running');
    setProgress(0);
    setLog([]);
    setResult(null);
    setError(null);
    setJobId(null);
    try {
      const res = await startAnalysis(source, language);
      const id  = res.data.job_id;
      setJobId(id);
      startPoll(id);
    } catch (e) {
      const msg = e.response?.data?.error || e.message;
      setError(msg);
      setStatus('error');
    }
  };

  const busy = status === 'running';

  return (
    <div className="app">
      <div className="app-canvas" aria-hidden="true" />

      <Navbar />

      <main id="main-content">
        <Hero />
        <div className="sep" role="separator" />
        <AnalyseCard onAnalyse={handleAnalyse} busy={busy} />

        {busy   && <ProcessingPanel progress={progress} log={log} />}
        {error  && <ErrorBanner message={error} />}
        {result && <ResultsSection result={result} jobId={jobId} />}
        {!busy && !result && !error && <EmptyState />}
      </main>

      <footer className="footer">
        <div className="container footer-inner">
          <p className="footer-copy">
            Built by Tushar Bharambe — LangChain · Mistral AI · Whisper · ChromaDB
          </p>
          <nav className="footer-links" aria-label="External links">
            <a className="footer-link" href="https://console.mistral.ai" target="_blank" rel="noopener noreferrer">Mistral AI</a>
            <a className="footer-link" href="https://www.sarvam.ai"      target="_blank" rel="noopener noreferrer">Sarvam AI</a>
            <a className="footer-link" href="https://openai.com/whisper"  target="_blank" rel="noopener noreferrer">Whisper</a>
          </nav>
        </div>
      </footer>
    </div>
  );
}
