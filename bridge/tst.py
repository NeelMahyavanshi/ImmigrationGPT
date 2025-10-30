# bridge/router_bridge.py
from pathlib import Path
import sys, shutil, os, sys

BASE = Path(__file__).resolve().parents[1] 
APP_DIR = BASE / "app"
WEB_PUBLIC = BASE / "web" / "public"
WEB_PUBLIC.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(APP_DIR))


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents.chitchat_agent import chitchat_agent
from app.agents.eligibility_agent import eligibility_agent
from app.agents.sop_agent import sop_agent
from app.agents.document_agent import document_agent

def _collect_files(run_output):
    files = []
    if getattr(run_output, "files", None):
        for f in run_output.files:
            try:
                if getattr(f, "path", None) and Path(f.path).exists():
                    target = WEB_PUBLIC / Path(f.filename).name
                    shutil.copy2(f.path, target)
                    files.append({"name": target.name, "url": f"/{target.name}"})
            except Exception:
                pass
    return files

def run_chitchat(user_text: str, user_id: str) -> tuple[str, list[dict], dict]:
    res = chitchat_agent.run(user_text, user_id=user_id)
    files = _collect_files(res)
    payload = {}
    try:
        # If output_schema was returned in .output or .content, pass dict forward
        out = getattr(res, "output", None) or getattr(res, "content", None)
        if isinstance(out, dict):
            payload = out
    except Exception:
        pass
    return (res.content or "Done.", files, payload)

def run_eligibility(user_text: str, user_id: str) -> tuple[str, list[dict], dict]:
    res = eligibility_agent.run(user_text, user_id=user_id)
    payload = {}
    try:
        # If output_schema was returned in .output or .content, pass dict forward
        out = getattr(res, "output", None) or getattr(res, "content", None)
        if isinstance(out, dict):
            payload = out
    except Exception:
        pass
    return (res.content or "Eligibility check complete.", [], payload)

def run_documents(user_text: str, user_id: str) -> tuple[str, list[dict], dict]:
    res = document_agent.run(user_text, user_id=user_id)
    payload = {}
    try:
        out = getattr(res, "output", None) or getattr(res, "content", None)
        if isinstance(out, dict):
            payload = out
    except Exception:
        pass
    return (res.content or "Checklist generated.", [], payload)

def run_sop(user_text: str, user_id: str) -> tuple[str, list[dict], dict]:
    res = sop_agent.run(user_text, user_id=user_id)
    files = _collect_files(res)
    return (res.content or "SOP generated.", files, {})
