import streamlit as st
import time
import os
from dotenv import load_dotenv

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MeetMind — AI Meeting Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_dotenv()

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background: #0a0a0f !important;
    padding: 0 !important;
}

.main .block-container {
    max-width: 1080px;
    padding: 2.5rem 2rem 6rem !important;
    margin: 0 auto;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 4rem 0 3rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(255,200,80,.10) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: #f5c842;
    border: 1px solid rgba(245,200,66,.3);
    padding: .28rem .9rem;
    border-radius: 100px;
    margin-bottom: 1.4rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.6rem, 6vw, 4rem);
    line-height: 1.08;
    letter-spacing: -.02em;
    color: #f0ebe0;
    margin-bottom: .8rem;
}
.hero h1 span { color: #f5c842; }
.hero p {
    font-size: 1.05rem;
    color: #8a877e;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Divider ── */
.rule { height: 1px; background: linear-gradient(90deg, transparent, rgba(245,200,66,.2), transparent); margin: 2.5rem 0; }

/* ── Input card ── */
.input-card {
    background: #111118;
    border: 1px solid #1f1f2e;
    border-radius: 16px;
    padding: 2rem 2.2rem 2.2rem;
    margin-bottom: 2rem;
}
.input-card h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #f0ebe0;
    margin-bottom: 1.2rem;
    letter-spacing: .01em;
}

/* ── Streamlit widget overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: #0e0e16 !important;
    border: 1px solid #2a2a3a !important;
    color: #e8e4dc !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.88rem !important;
    padding: .55rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #f5c842 !important;
    box-shadow: 0 0 0 3px rgba(245,200,66,.1) !important;
    outline: none !important;
}
label, [data-testid="stWidgetLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    color: #6a6860 !important;
    margin-bottom: .4rem !important;
}

/* ── Primary button ── */
.stButton > button {
    width: 100%;
    background: #f5c842 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: .95rem !important;
    letter-spacing: .03em !important;
    padding: .75rem 2rem !important;
    cursor: pointer !important;
    transition: all .2s ease !important;
}
.stButton > button:hover {
    background: #ffd84d !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(245,200,66,.25) !important;
}

/* ── Progress / status ── */
[data-testid="stProgress"] > div > div {
    background: #f5c842 !important;
    border-radius: 4px !important;
}
[data-testid="stProgress"] {
    background: #1a1a26 !important;
    border-radius: 4px !important;
    height: 6px !important;
}
.stSpinner > div > div { border-top-color: #f5c842 !important; }

/* ── Result tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #111118 !important;
    border-radius: 12px 12px 0 0 !important;
    border-bottom: 1px solid #1f1f2e !important;
    padding: 0 .5rem !important;
    gap: 0 !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: .78rem !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    color: #5a5850 !important;
    padding: .85rem 1.1rem !important;
    border-radius: 0 !important;
    border: none !important;
    background: transparent !important;
    transition: color .15s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #f5c842 !important;
    border-bottom: 2px solid #f5c842 !important;
}
[data-testid="stTabsContent"] {
    background: #111118 !important;
    border: 1px solid #1f1f2e !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1.8rem !important;
}

/* ── Result content ── */
.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #f5c842;
    margin-bottom: 1.2rem;
    line-height: 1.2;
}
.result-text {
    font-family: 'DM Sans', sans-serif;
    font-size: .95rem;
    color: #c8c4bc;
    line-height: 1.75;
}
.item-row {
    display: flex;
    align-items: flex-start;
    gap: .75rem;
    padding: .7rem 0;
    border-bottom: 1px solid #1a1a26;
}
.item-row:last-child { border-bottom: none; }
.item-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #f5c842;
    margin-top: .45rem;
    flex-shrink: 0;
}
.item-text {
    font-family: 'DM Sans', sans-serif;
    font-size: .92rem;
    color: #c8c4bc;
    line-height: 1.6;
}
.transcript-box {
    background: #0d0d14;
    border: 1px solid #1a1a26;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    max-height: 340px;
    overflow-y: auto;
    font-family: 'DM Mono', monospace;
    font-size: .8rem;
    color: #6a6860;
    line-height: 1.7;
    word-break: break-word;
}
.transcript-box::-webkit-scrollbar { width: 4px; }
.transcript-box::-webkit-scrollbar-track { background: transparent; }
.transcript-box::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 4px; }

/* ── Chat ── */
.chat-wrap {
    background: #111118;
    border: 1px solid #1f1f2e;
    border-radius: 16px;
    padding: 1.6rem;
    margin-top: 2rem;
}
.chat-wrap h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #f0ebe0;
    margin-bottom: 1.2rem;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: .9rem;
}
.msg-user > div {
    background: #f5c842;
    color: #0a0a0f;
    font-family: 'DM Sans', sans-serif;
    font-size: .88rem;
    padding: .6rem 1rem;
    border-radius: 14px 14px 4px 14px;
    max-width: 74%;
    font-weight: 500;
}
.msg-bot {
    display: flex;
    justify-content: flex-start;
    margin-bottom: .9rem;
}
.msg-bot > div {
    background: #17171f;
    color: #c8c4bc;
    font-family: 'DM Sans', sans-serif;
    font-size: .88rem;
    padding: .6rem 1rem;
    border-radius: 14px 14px 14px 4px;
    max-width: 78%;
    line-height: 1.6;
    border: 1px solid #22222e;
}
.chat-history {
    max-height: 320px;
    overflow-y: auto;
    margin-bottom: 1rem;
    padding-right: .4rem;
}
.chat-history::-webkit-scrollbar { width: 3px; }
.chat-history::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 4px; }

/* ── Status steps ── */
.step-row {
    display: flex;
    align-items: center;
    gap: .75rem;
    padding: .45rem 0;
    font-family: 'DM Mono', monospace;
    font-size: .78rem;
    color: #5a5850;
}
.step-row.done { color: #a0c878; }
.step-row.active { color: #f5c842; }
.step-icon { width: 14px; text-align: center; }

/* ── Stat chips ── */
.stat-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1.2rem; }
.stat-chip {
    background: #0d0d14;
    border: 1px solid #1f1f2e;
    border-radius: 8px;
    padding: .5rem 1rem;
    font-family: 'DM Mono', monospace;
    font-size: .75rem;
    color: #6a6860;
}
.stat-chip span { color: #f5c842; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ─── Pipeline import (graceful fallback) ────────────────────────────────────
try:
    from utils.audio_processor import process_input
    from core.transcriber import transcribe_all
    from core.summrizer import summarizer, generate_title
    from core.extractor import extract_action_items, extract_key_decisions, extract_questions
    from core.rag_engine import build_rag_chain, ask_question
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False

# ─── Session state init ──────────────────────────────────────────────────────
for key, val in {
    "result": None,
    "processing": False,
    "chat_history": [],
    "pipeline_error": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">AI Meeting Intelligence</div>
  <h1>Meet<span>Mind</span></h1>
  <p>Drop in a YouTube link or local video — get a full transcript, smart summary, action items, and a chat interface powered by RAG.</p>
</div>
<div class="rule"></div>
""", unsafe_allow_html=True)

# ─── Input panel ─────────────────────────────────────────────────────────────
st.markdown('<div class="input-card"><h3>📥 Source & Settings</h3>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    source = st.text_input(
        "YouTube URL or local file path",
        placeholder="https://youtube.com/watch?v=...  or  /path/to/video.mp4",
        key="source_input",
    )
with col2:
    language = st.selectbox("Language", ["english", "hinglish", "hindi", "auto"], index=0)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Run button ───────────────────────────────────────────────────────────────
run_clicked = st.button("🚀  Analyse Meeting", disabled=st.session_state.processing)

# ─── Pipeline execution ───────────────────────────────────────────────────────
if run_clicked and source.strip():
    if not PIPELINE_AVAILABLE:
        st.session_state.pipeline_error = (
            "Pipeline modules not found. Make sure `utils/`, `core/` packages "
            "are installed and importable."
        )
    else:
        st.session_state.processing = True
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_error = None
        st.rerun()

elif run_clicked and not source.strip():
    st.warning("Please enter a YouTube URL or file path first.")

# ─── Processing UI ─────────────────────────────────────────────────────────────
if st.session_state.processing:
    STEPS = [
        ("🎧", "Processing audio…"),
        ("✍️",  "Transcribing speech…"),
        ("📝", "Generating title & summary…"),
        ("🔍", "Extracting action items, decisions, questions…"),
        ("🔗", "Building RAG chain…"),
    ]

    status_placeholder = st.empty()
    prog = st.progress(0)

    def render_steps(done_up_to):
        html = ""
        for i, (icon, label) in enumerate(STEPS):
            cls = "done" if i < done_up_to else ("active" if i == done_up_to else "")
            tick = "✓" if i < done_up_to else ("›" if i == done_up_to else "·")
            html += f'<div class="step-row {cls}"><span class="step-icon">{tick}</span>{icon} {label}</div>'
        status_placeholder.markdown(html, unsafe_allow_html=True)

    try:
        render_steps(0); prog.progress(5)
        chunks = process_input(st.session_state.source_input)

        render_steps(1); prog.progress(25)
        transcript = transcribe_all(chunks, language=language)

        render_steps(2); prog.progress(45)
        title   = generate_title(transcript)
        summary = summarizer(transcript)

        render_steps(3); prog.progress(65)
        action_items = extract_action_items(transcript)
        decisions    = extract_key_decisions(transcript)
        questions    = extract_questions(transcript)

        render_steps(4); prog.progress(85)
        rag_chain = build_rag_chain(transcript)

        prog.progress(100)
        render_steps(len(STEPS))
        time.sleep(.4)

        st.session_state.result = {
            "title":        title,
            "transcript":   transcript,
            "summary":      summary,
            "action_items": action_items,
            "decisions":    decisions,
            "questions":    questions,
            "rag_chain":    rag_chain,
        }

    except Exception as e:
        st.session_state.pipeline_error = str(e)

    finally:
        st.session_state.processing = False
        prog.empty()
        st.rerun()

# ─── Error banner ─────────────────────────────────────────────────────────────
if st.session_state.pipeline_error:
    st.error(f"**Pipeline error:** {st.session_state.pipeline_error}")

# ─── Results ──────────────────────────────────────────────────────────────────
res = st.session_state.result
if res:
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # Title + stats
    wc = len(res["transcript"].split())
    ai = len(res["action_items"]) if isinstance(res["action_items"], list) else "—"
    kd = len(res["decisions"])    if isinstance(res["decisions"],    list) else "—"
    oq = len(res["questions"])    if isinstance(res["questions"],    list) else "—"

    st.markdown(f"""
    <div class="result-title">{res['title']}</div>
    <div class="stat-row">
      <div class="stat-chip">Words <span>{wc:,}</span></div>
      <div class="stat-chip">Action items <span>{ai}</span></div>
      <div class="stat-chip">Key decisions <span>{kd}</span></div>
      <div class="stat-chip">Open questions <span>{oq}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ──
    tab_summary, tab_actions, tab_decisions, tab_questions, tab_transcript = st.tabs([
        "📋  Summary",
        "✅  Action Items",
        "🔑  Decisions",
        "❓  Questions",
        "📄  Transcript",
    ])

    def bullet_list(items):
        if isinstance(items, list):
            return "".join(
                f'<div class="item-row"><div class="item-dot"></div><div class="item-text">{i}</div></div>'
                for i in items
            )
        return f'<p class="result-text">{items}</p>'

    with tab_summary:
        st.markdown(f'<p class="result-text">{res["summary"]}</p>', unsafe_allow_html=True)

    with tab_actions:
        st.markdown(bullet_list(res["action_items"]), unsafe_allow_html=True)

    with tab_decisions:
        st.markdown(bullet_list(res["decisions"]), unsafe_allow_html=True)

    with tab_questions:
        st.markdown(bullet_list(res["questions"]), unsafe_allow_html=True)

    with tab_transcript:
        st.markdown(
            f'<div class="transcript-box">{res["transcript"]}</div>',
            unsafe_allow_html=True,
        )
        if st.button("📋  Copy transcript"):
            st.write("Use Ctrl+A → Ctrl+C inside the box above.")

    # ── RAG Chat ──
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-wrap">
      <h3>💬 Chat with your meeting</h3>
    </div>
    """, unsafe_allow_html=True)

    # Render history
    if st.session_state.chat_history:
        history_html = '<div class="chat-history">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                history_html += f'<div class="msg-user"><div>{msg["content"]}</div></div>'
            else:
                history_html += f'<div class="msg-bot"><div>{msg["content"]}</div></div>'
        history_html += "</div>"
        st.markdown(history_html, unsafe_allow_html=True)

    # Input row
    q_col, btn_col = st.columns([5, 1])
    with q_col:
        user_q = st.text_input(
            "Ask a question",
            placeholder="What were the main decisions made?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with btn_col:
        ask_btn = st.button("Ask →", key="ask_btn")

    if ask_btn and user_q.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        try:
            from core.rag_engine import ask_question
            answer = ask_question(res["rag_chain"], user_q)
        except Exception as e:
            answer = f"Error: {e}"
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

# ─── Empty state ──────────────────────────────────────────────────────────────
if not res and not st.session_state.processing:
    st.markdown("""
    <div style="text-align:center;padding:3rem 0 2rem;color:#3a3830;">
      <div style="font-size:3rem;margin-bottom:1rem;">🎙️</div>
      <div style="font-family:'DM Mono',monospace;font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;">
        Paste a link or path above and hit Analyse
      </div>
    </div>
    """, unsafe_allow_html=True)