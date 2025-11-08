import logging
from pathlib import Path
import sys
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE = Path(__file__).resolve().parents[1]   
APP_DIR = BASE / "app"

# --- IMPORT SHARED CONFIG ---
sys.path.insert(0, str(BASE))  # Add project root to path
from config import GENERATED_FILES_DIR

# Ensure imports work
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Import agents 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.agents.chitchat_agent import chitchat_agent
from app.agents.eligibility_agent import eligibility_agent
from app.agents.sop_agent import sop_agent
from app.agents.document_agent import document_agent

def run_chitchat(user_text: str, user_id: str):
    logger.info(f"Running chitchat for user {user_id}: {user_text[:50]}...")
    try:
        res = chitchat_agent.run(user_text, user_id=user_id)
        json_output = json.loads(res.content.model_dump_json())
        reply = json_output.get("reply", "")
        escalate_to = json_output.get("escalate_to", "")
        logger.info(f"Chitchat completed for user {user_id}")
        logger.info(f"Chitchat reply for user {user_id}, reply : {reply}, escalate_to: {escalate_to}")
        return reply, escalate_to
    except Exception as e:
        logger.error(f"Error in run_chitchat for user {user_id}: {e}")
        raise

def run_eligibility(user_text: str, user_id: str):
    logger.info(f"Running eligibility for user {user_id}: {user_text[:50]}...")
    try:
        res = eligibility_agent.run(user_text, user_id=user_id)
        json_output = json.loads(res.content.model_dump_json())
        user_profile = json_output.get("user_profile", {})
        eligible_programs = json_output.get("eligible_programs", [])
        ineligible_programs = json_output.get("ineligible_programs", [])
        crs_estimate = json_output.get("crs_estimate", None)
        improvement_suggestions = json_output.get("improvement_suggestions", [])
        next_steps = json_output.get("next_steps", [])
        requires_follow_up = json_output.get("requires_follow_up", False)
        logger.info(f"Eligibility completed for user {user_id}")
        logger.info(f"CRS estimate for user {user_id}: {crs_estimate}")
        return user_profile, eligible_programs, ineligible_programs, crs_estimate, improvement_suggestions, next_steps, requires_follow_up
    except Exception as e:
        logger.error(f"Error in run_eligibility for user {user_id}: {e}")
        raise

def run_documents(user_text: str, user_id: str):
    logger.info(f"Running documents for user {user_id}: {user_text[:50]}...")
    try:
        res = document_agent.run(user_text, user_id=user_id)
        json_output = json.loads(res.content.model_dump_json())
        
        # Ensure these .get() calls match the Pydantic schema field names exactly
        program = json_output.get("program", "")
        overview = json_output.get("overview", "")
        required_documents = json_output.get("required_documents", [])
        conditional_documents = json_output.get("conditional_documents", [])
        optional_but_recommended = json_output.get("optional_but_recommended", [])
        forms = json_output.get("forms", [])
        official_guide_url = json_output.get("official_guide_url", "")
        
        logger.info(f"Documents completed for user {user_id} for program: {program}")
        
        # The order of this returned tuple matters
        return (
            program,
            overview,
            required_documents,
            conditional_documents,
            optional_but_recommended,
            forms,
            official_guide_url,
        )
    except Exception as e:
        logger.error(f"Error in run_documents for user {user_id}: {e}", exc_info=True)
        return "", "", [], [], [], [], ""


def run_sop(user_text: str, user_id: str):
    """
    Runs the SOP agent and returns (reply_text, supabase_pdf_url).
    If the model hallucinates a non-existent 'json' tool or similar, we retry once
    with a hard constraint appended to the user_text.
    """
    logger.info(f"Running SOP for user {user_id}: {user_text[:50]}...")

    def _extract(res):
        try:
            json_output = json.loads(res.content.model_dump_json())
        except Exception as e:
            logger.error(f"Failed to parse SOPAgentResponse JSON: {e}", exc_info=True)
            # Fallback minimal reply
            json_output = {"reply": "Your document request has been processed.", "files": []}

        reply_text = json_output.get("reply", "Your document request has been processed.")
        pdf_file_url = None

        if res.files and len(res.files) > 0:
            logger.info(f"✅ Agent returned {len(res.files)} file(s)")
            for file in res.files:
                logger.info(f"   📄 File name: {getattr(file, 'name', '')}")
                # Prefer Supabase URL carried with the File
                if getattr(file, "url", None) and getattr(file, "name", "").endswith(".pdf"):
                    logger.info(f"   🔗 Found Supabase URL: {file.url[:80]}...")
                    pdf_file_url = file.url
                    break

        if pdf_file_url:
            logger.info(f"✅ Returning Supabase URL: {pdf_file_url[:100]}...")
        else:
            logger.warning("⚠️ No Supabase URL found in agent response")

        return reply_text, pdf_file_url

    # First attempt
    try:
        res = sop_agent.run(user_text, user_id=user_id)
        return _extract(res)
    except Exception as e:
        msg = str(e)
        logger.warning(f"SOP first attempt failed: {msg}")

        # Retry only for tool hallucinations or similar tool_use_failed issues
        should_retry = (
            "attempted to call tool 'json'" in msg
            or "tool_use_failed" in msg
            or "tool call validation failed" in msg
        )

        if not should_retry:
            logger.error(f"Non-retryable SOP error: {e}", exc_info=True)
            return f"An error occurred: {str(e)}", None

        logger.warning("Retrying SOP with hard constraint to forbid 'json' tool calls.")
        hard_nudge = (
            user_text
            + "\n\n[System constraint to model: Do NOT call any tool named 'json'. "
              "Generate the document, call only generate_professional_pdf, then OUTPUT final JSON as plain text "
              "matching SOPAgentResponse with reply and files.]"
        )

        try:
            res = sop_agent.run(hard_nudge, user_id=user_id)
            return _extract(res)
        except Exception as e2:
            logger.error(f"SOP retry failed: {e2}", exc_info=True)
            return f"An error occurred: {str(e2)}", None
