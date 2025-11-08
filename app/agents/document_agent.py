import random
from typing import List, Optional
from pydantic import BaseModel, Field
from agno.agent import Agent, RunOutput
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.crawl4ai import Crawl4aiTools
from dotenv import load_dotenv
from rich.pretty import pprint 
from pathlib import Path
from agno.tools.csv_toolkit import CsvTools
from agno.models.openrouter import OpenRouter
import os
from agno.db.postgres import PostgresDb

load_dotenv()


db = PostgresDb(
    db_url=os.getenv("DATABASE_URL"),
    memory_table=os.getenv("AGNO_MEMORY_TABLE", "agno_memories"),
)


# === PYDANTIC SCHEMA ===
class DocumentItem(BaseModel):
    name: str = Field(description="Exact document name (e.g., 'Notarized Bank Statements')")
    description: str = Field(description="What it is and why it's needed")
    mandatory: bool = Field(description="True if always required")
    conditional_on: Optional[str] = Field(default=None, description="When required")
    source_url: Optional[str] = Field(default=None, description="IRCC or official link")
    tips: Optional[str] = Field(default=None, description="Practical advice")
    common_mistakes: Optional[str] = Field(default=None, description="What applicants get wrong")

class FormItem(BaseModel):
    form_number: str = Field(description="e.g., IMM 1294")
    title: str = Field(description="Official title")
    pdf_url: str = Field(description="Direct PDF link")
    instructions_url: Optional[str] = Field(default=None)

class DocumentChecklist(BaseModel):
    program: str = Field(description="e.g., Study Permit - Outside Canada")
    overview: str = Field(description="Brief strategy summary")
    required_documents: List[DocumentItem]
    conditional_documents: List[DocumentItem] = Field(default_factory=list)
    optional_but_recommended: List[DocumentItem] = Field(default_factory=list)
    forms: List[FormItem]
    official_guide_url: str


db_path = Path(__file__).parent.parent.parent / "data" / "forms" / "ircc_forms_details.csv"

# === AGENT ===

document_agent_instructions = """"

You are DocumentAgent, Canada’s most meticulous immigration document specialist. Generate exhaustive, real-world checklists that go beyond basic IRCC lists, including hidden pitfalls and practical tips.

CONSULT MEMORY
First, review the user's memory for their target program, location (province and country of residence), and occupation. This context is critical.

INFORMATION GATHERING
- Use all provided info + safe defaults (family_size=1, single applicant, no job offer).
- Ask only if a single missing fact changes the program’s checklist (e.g., study vs work vs PR, in-Canada vs outside). Asl all question at a time (max 3), include a default, and proceed if no reply.

RESEARCH PROTOCOL
- First search: Use `GoogleSearchTools` to find the official IRCC and provincial government pages for the specified program. (e.g., “study permit checklist site:canada.ca”).
- Then : Use `Crawl4aiTools` to extract detailed requirements.
- Then add: processing updates (≤6 months), country-specific requirements (e.g., biometrics, PCC routing), VFS quirks.
- Use `CsvTools` to query your internal `ircc_forms_details.csv` to fetch form numbers, titles, pdf_url, and instructions_url (do not invent). 
    The columns of the CSV "ircc_forms_details.csv" : form_code,title,last_updated,form_page_url,pdf_url,how_to_fill_instructions
    You have to find all the detals about forms from this CSV file anyhow. DO not search exact form number in the csv, instead search by keyword match : form number, title or any other relevant keywords to find the correct form details.

OUTPUT REQUIREMENTS (strict schema)
For each document (required/conditional/optional):
- name (specific), description (what/why + validity rules), mandatory (True only if always required), conditional_on (trigger), source_url (IRCC/province/CSV), tips (practical steps), common_mistakes (real refusal causes).
Forms list: form_number, title, pdf_url, instructions_url (if any).
Also include overview (strategy summary) and official_guide_url.

DEPTH & CONTEXT
- Biometrics, medicals, PCC validity windows.
- Translation rules (non‑EN/FR → certified translation + affidavit).
- Photo specs, file size limits, paper size guidance.
- Country/region quirks when implied (e.g., VFS appointments, notarization norms).

STRICT RULES
- Never hallucinate forms, numbers, or links. If not found, say “Form not found in database.”
- Always return the exact DocumentChecklist schema (no extra text/markdown).
- Flag assumptions clearly (e.g., “Assuming outside-Canada study permit.”).
- Be exhaustive; do not summarize.
- Output powers an editable checklist; ensure clarity and actionability.

"""
document_agent = Agent(
    # model=Groq(id="openai/gpt-oss-120b"),
    model=Gemini(id="gemini-2.5-flash"),        
    parser_model=Gemini(id="gemini-2.0-flash"),       
    db=db,
    enable_agentic_memory = True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=3,
    search_session_history=True,
    add_memories_to_context=True,
    name="DocumentAgent",
    description="You generate exhaustive, real-world Canadian immigration document checklists.",
    instructions=document_agent_instructions,
    tools=[
        GoogleSearchTools(),    
        Crawl4aiTools(),
        CsvTools(
            csvs=[db_path],
            enable_read_csv_file=True,
            enable_list_csv_files=True,
            enable_get_columns=True,
            enable_query_csv_file=True
        )
    ],
    output_schema=DocumentChecklist,
)

# === RUN ===
# programs = [
#     "Study Permit from India",
#     "Express Entry - Federal Skilled Worker",
#     "Spousal Sponsorship",
#     "Visitor Visa from Nigeria",
#     "Work Permit under International Mobility Program"
# ]

# query = random.choice(programs)
# print(f"🔍 Researching documents for: {query}\n")

# run: RunOutput = document_agent.run(query)

# pprint(run.content)
