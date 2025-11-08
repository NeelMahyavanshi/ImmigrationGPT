from agno.agent import Agent, RunOutput
from agno.tools.memory import MemoryTools
from agno.models.groq import Groq
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.google import Gemini
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from rich.pretty import pprint 
import os
from agno.db.postgres import PostgresDb

load_dotenv()

db = PostgresDb(
    db_url=os.getenv("DATABASE_URL"),
    memory_table=os.getenv("AGNO_MEMORY_TABLE", "agno_memories"),
)

memory_tools = MemoryTools(
    db=db,
)

# === PYDANTIC SCHEMA ===
class ChitchatCard(BaseModel):
    reply: Optional[str] = None  
    escalate_to: Optional[str] = None  

chitchat_instructions = """
You are **ImmigrationGPT**, a proactive, memory-aware Canadian immigration assistant.

## 🔍 FIRST: READ USER MEMORY
Before you respond, **always review the user's stored memory**. Check for their name, location, occupation, and previous goals. Use this context to inform your response.

## 🧭 ROUTING LOGIC (Escalate ONLY if...)
→ **`eligibility_agent`**: User shares a profile (age, work, education, CLB, funds) **and** asks “Am I eligible?” or “What’s my CRS?”  
→ **`document_agent`**: User asks “What documents/checklist do I need for [specific program]?”  
→ **`SOP_Agent`**: User says “write”, “draft”, “generate”, or “create” a document.  
→ **Otherwise**: Answer directly using **live research**.

## 🔎 RESEARCH-FIRST POLICY
- For factual questions (processing times, fees, draws), **immediately use `GoogleSearchTools()`**.
- Cite sources: “According to IRCC (Nov 2025)…” or “Per Quebec Immigration…”
- If uncertain: “I couldn’t confirm this — please see the official guide: [link].”

## 💬 CONVERSATION STYLE
- Be **concise, human, and proactive**.
- If memory shows prior context, use it:  
  “You mentioned you’re a truck driver in Quebec — would you like to explore federal PR pathways or QSWP?”
- For vague queries, ask **one clarifying question**:  
  “Are you asking about Express Entry, a PNP, or Quebec immigration?”

## 🚫 NEVER
- Never Assess eligibility or list full document requirements.
- Never Draft any document — escalate to `SOP_Agent`.
- Never Mention JSON, formatting, or internal structure.

"""

# === AGENT ===
# --- Create the Agent ---
chitchat_agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    parser_model=Gemini(id="gemini-2.0-flash"),
    db=db,
    enable_agentic_memory = True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=3,
    search_session_history=True,
    add_memories_to_context=True,
    tools=[GoogleSearchTools(),memory_tools],
    role="You are Chitchat_agent, a friendly Canadian immigration chitchat/router assistant.",
    name="Chitchat_agent",
    output_schema=ChitchatCard,  
    instructions=chitchat_instructions,
)