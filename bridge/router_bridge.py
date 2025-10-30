# bridge/router_bridge.py
from pathlib import Path
import sys
import shutil
import os

# Resolve paths
BASE = Path(__file__).resolve().parents[1]   # project root
APP_DIR = BASE / "app"
WEB_PUBLIC = BASE / "public"
WEB_PUBLIC.mkdir(parents=True, exist_ok=True)

# Ensure imports work
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Import agents (unchanged)
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
                fpath = getattr(f, "path", None)
                if fpath and Path(fpath).exists():
                    target = WEB_PUBLIC / Path(f.filename).name
                    shutil.copy2(fpath, target)
                    files.append({"name": target.name, "path": str(target)})
            except Exception:
                pass
    return files

# bridge/router_bridge.py
def _to_payload(res):
    out = getattr(res, "output", None)
    if isinstance(out, dict): return out
    out2 = getattr(res, "content", None)
    return out2 if isinstance(out2, dict) else {}

def _text_reply(res, payload):
    if isinstance(getattr(res, "content", None), str) and res.content.strip():
        return res.content.strip()
    if isinstance(payload, dict):
        rep = payload.get("reply")
        if isinstance(rep, str) and rep.strip():
            return rep.strip()
    return "How can I help with Canadian immigration today?"

def run_chitchat(user_text: str, user_id: str):
    res = chitchat_agent.run(user_text, user_id=user_id)
    files = _collect_files(res)
    payload = _to_payload(res)
    return (_text_reply(res, payload), files, payload)

def run_eligibility(user_text: str, user_id: str):
    res = eligibility_agent.run(user_text, user_id=user_id)
    return (_text_reply(res, _to_payload(res)), _collect_files(res), _to_payload(res))

def run_documents(user_text: str, user_id: str):
    res = document_agent.run(user_text, user_id=user_id)
    return (_text_reply(res, _to_payload(res)), _collect_files(res), _to_payload(res))

def run_sop(user_text: str, user_id: str):
    res = sop_agent.run(user_text, user_id=user_id)
    return (_text_reply(res, _to_payload(res)), _collect_files(res), _to_payload(res))