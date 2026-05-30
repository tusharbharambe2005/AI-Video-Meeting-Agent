"""
MeetMind — Flask REST API Server
Exposes the pipeline as HTTP endpoints for the React frontend.
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import threading
import time
import uuid
import json
import queue
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow React dev server

# ── In-memory job store (use Redis/DB in production) ──────────────────────────
jobs: dict[str, dict] = {}  # job_id -> {status, result, error, progress, log}

# ── Pipeline import (graceful) ────────────────────────────────────────────────
try:
    from utils.audio_processor import process_input
    from core.transcriber import transcribe_all
    from core.summrizer import summarizer, generate_title
    from core.extractor import extract_action_items, extract_key_decisions, extract_questions
    from core.rag_engine import build_rag_chain, ask_question as rag_ask
    PIPELINE_AVAILABLE = True
except ImportError as e:
    PIPELINE_AVAILABLE = False
    PIPELINE_IMPORT_ERROR = str(e)



def _to_list(raw) -> list:
    """Convert a numbered/bulleted string from the LLM into a clean Python list."""
    if isinstance(raw, list):
        return [str(i).strip() for i in raw if str(i).strip()]
    if not isinstance(raw, str):
        return [str(raw)]
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        # Strip leading numbering like "1.", "1)", "-", "•"
        import re
        line = re.sub(r'^(\d+[\.\)]|[-•*])\s*', '', line)
        if line:
            lines.append(line)
    return lines if lines else [raw.strip()]


def run_pipeline(job_id: str, source: str, language: str):
    """Runs the full MeetMind pipeline in a background thread."""
    jobs[job_id]["status"] = "running"
    log = jobs[job_id]["log"]

    def push(step: str, pct: int):
        log.append({"step": step, "progress": pct})
        jobs[job_id]["progress"] = pct

    try:
        push("Processing audio…", 5)
        chunks = process_input(source)

        push("Transcribing speech…", 25)
        transcript = transcribe_all(chunks, language=language)

        push("Generating title & summary…", 45)
        title   = generate_title(transcript)
        summary = summarizer(transcript)

        push("Extracting action items, decisions & questions…", 65)
        action_items = extract_action_items(transcript)
        decisions    = extract_key_decisions(transcript)
        questions    = extract_questions(transcript)

        push("Building RAG chain…", 85)
        rag_chain = build_rag_chain(transcript)
        # Keep rag_chain only in-memory — never put it in result (not JSON-serializable)
        jobs[job_id]["rag_chain"] = rag_chain

        push("Done", 100)
        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = {
            "title":        str(title).strip(),
            "transcript":   str(transcript),
            "summary":      str(summary),
            "action_items": _to_list(action_items),
            "decisions":    _to_list(decisions),
            "questions":    _to_list(questions),
        }

    except Exception as e:
        import traceback
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"]  = str(e)
        print(f"[Pipeline ERROR] job={job_id}\n{traceback.format_exc()}")



# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "pipeline_available": PIPELINE_AVAILABLE,
    })


@app.route("/api/analyse", methods=["POST"])
def analyse():
    """Start a pipeline job. Returns job_id immediately."""
    if not PIPELINE_AVAILABLE:
        return jsonify({"error": "Pipeline modules not available on this server."}), 503

    data = request.get_json(force=True)
    source   = (data.get("source")   or "").strip()
    language = (data.get("language") or "english").strip()

    if not source:
        return jsonify({"error": "source is required"}), 400

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status":   "queued",
        "progress": 0,
        "log":      [],
        "result":   None,
        "error":    None,
        "rag_chain": None,
    }

    thread = threading.Thread(target=run_pipeline, args=(job_id, source, language), daemon=True)
    thread.start()

    return jsonify({"job_id": job_id}), 202


@app.route("/api/status/<job_id>", methods=["GET"])
def status(job_id: str):
    """Poll job status and result."""
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    resp = {
        "status":   job["status"],
        "progress": job["progress"],
        "log":      job["log"],
    }

    if job["status"] == "done":
        resp["result"] = job["result"]

    if job["status"] == "error":
        resp["error"] = job["error"]

    try:
        return jsonify(resp)
    except TypeError as e:
        # Safety net: if result contains non-serializable objects, report clearly
        return jsonify({
            "status":   "error",
            "progress": job["progress"],
            "log":      job["log"],
            "error":    f"Internal serialization error: {e}. Please check server logs.",
        }), 500


@app.route("/api/chat/<job_id>", methods=["POST"])
def chat(job_id: str):
    """Ask a RAG question about the analysed meeting."""
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    if job["status"] != "done":
        return jsonify({"error": "Analysis not complete yet"}), 400

    rag_chain = job.get("rag_chain")
    if not rag_chain:
        return jsonify({"error": "RAG chain not available"}), 500

    data     = request.get_json(force=True)
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "question is required"}), 400

    try:
        answer = rag_ask(rag_chain, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 MeetMind API Server starting on http://localhost:8000")
    app.run(debug=True, port=8000, threaded=True)
