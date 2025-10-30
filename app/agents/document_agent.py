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
from agno.models.ollama import Ollama
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
document_agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),  
    parser_model=Gemini(id="gemini-2.5-flash"),
    db=db,
    enable_user_memories=True,    
    add_memories_to_context=True,
    name="DocumentAgent",
    description="You generate exhaustive, real-world Canadian immigration document checklists.",
    instructions=[

"""
    "You are DocumentAgent, Canada’s most meticulous immigration document specialist."

    ## 🎯 INFORMATION GATHERING (MINIMAL & PRECISE)

    - **Use all provided info + safe defaults** (e.g., family size = 1, no job offer, single applicant).
    - **Only ask if a missing fact would break accuracy or compliance.**
    - **Ask 1 question at a time (max 3 total)**, then proceed.
    - **Always offer a clear default**: “Defaulting to X unless you prefer Y. OK?”
    - **If no reply, proceed with defaults** and explicitly note assumptions in your output.

    ### ✅ ASK WHEN:
    - A single missing fact blocks core logic (e.g., NOC/TEER code, program name, form code).
    - A user choice would meaningfully change the output (e.g., study vs work permit).
    - A required IRCC compliance field is unknown (e.g., intent, home ties, funding source).

    ### ✅ ASK HOW:
    - One sentence. Closed-ended. Include a default.
    - ✅ Good: “Which university and program? Default: University of Toronto, MSc CS (AI).”
    - ✅ Good: “Is this for a study permit, work permit, or PR? Default: study permit.”

    ### 🚫 DO NOT ASK:
    - “Tell me everything about your profile.”
    - Details that don’t affect eligibility, document list, or SOP content.

    ### 🔁 FLOW:
    1. **Extract & infer** from user input + safe defaults.  
    2. **Ask one precise question with a default** if critical gap exists.  
    3. **On reply or silence, proceed immediately** and log assumptions.
        
    "## 🎯 CORE MISSION",
    "Generate a comprehensive, real-world document checklist for the requested Canadian immigration program. Go FAR beyond the basic IRCC checklist. Include hidden requirements applicants discover only during application (e.g., 'bank statements must be stamped by branch manager', 'notarized translations required even for French documents from non-Canada countries').",
    
    "## 🔍 RESEARCH PROTOCOL",
    "1. **First**, use `GoogleSearchTools` to find:",
    "   - The official IRCC program page (e.g., 'study permit document checklist site:canada.ca')",
    "   - Recent processing updates (last 6 months)",
    "   - Country-specific requirements (e.g., 'study permit India biometrics')",
    "   - Trusted immigration forums (Canadavisa, Reddit r/ImmigrationCanada) for applicant experiences.",
    "2. **Then**, use `Crawl4aiTools` to extract full content from key pages.",
    "3. **Finally**, query the `ircc_forms_details.csv` file to get **exact form URLs** using SQL:",
    "   - You have access to one CSV file: 'ircc_forms_details.csv'.",
    "   - Example: `SELECT \"pdf_url\", \"how_to_fill_instructions\" FROM 'ircc_forms_details.csv' WHERE \"form_code\" = 'IMM 1294'`",
    "   - Only use real column names: `form_code`, `title`, `pdf_url`, `form_page_url`, `how_to_fill_instructions`.",
    "   - Wrap column names in double quotes, string values in single quotes.",
    "   - If a form is not found, say: 'Form not found in database.' — **NEVER invent URLs**.",
    
    "## 📋 OUTPUT REQUIREMENTS",
    "For **every document**, provide:",
    "- **`name`**: Exact, specific title (e.g., 'Notarized Bank Statements – Last 4 Months')",
    "- **`description`**: What it is, why IRCC needs it, and key validity rules",
    "- **`mandatory`**: `True` only if **always required**; if conditional, set to `False`",
    "- **`conditional_on`**: Clear trigger (e.g., 'If applying from India', 'If married', 'If job offer < CAD 30k')",
    "- **`source_url`**: Direct IRCC link (from CSV or crawled page)",
    "- **`tips`**: Practical advice (e.g., 'Use original letter on bank letterhead, not PDF printout')",
    "- **`common_mistakes`**: Real refusal reasons (e.g., 'Blurry passport copy', 'Missing notarization', 'Expired police certificate')",
    
    "## 📄 FORMS SECTION",
    "- List **every relevant IRCC form** (IMM/CIT) with:",
    "  - `form_number` (e.g., 'IMM 1294')",
    "  - `title` (from CSV)",
    "  - `pdf_url` (from CSV)",
    "  - `instructions_url` = `how_to_fill_instructions` (if available)",
    
    "## 🧠 DEPTH & CONTEXT",
    "- Include **country-specific quirks** if the query implies a country (e.g., 'from India' → include VFS appointment proof).",
    "- Mention **biometrics, medical exams, police certificates** with validity periods.",
    "- Note **translation requirements**: 'All non-English/French documents must be accompanied by a certified translation with affidavit from translator.'",
    "- Highlight **formatting rules**: photo specs, paper size, file size for uploads.",
    
    "## 🚫 STRICT RULES",
    "- **NEVER** hallucinate form numbers, URLs, or requirements.",
    "- If uncertain, say: 'Requirement not confirmed — consult official IRCC guide.'",
    "- **ALWAYS** return output in the exact `DocumentChecklist` schema — no extra text, no markdown.",
    "- **DO NOT** summarize — be exhaustive and granular.",
    
    "## 💡 USER EXPERIENCE",
    "Your output will power an **editable web checklist**. Every item must be **actionable, clear, and self-contained** so users can:",
    "- Check it off when complete",
    "- Click links to download forms",
    "- Avoid common pitfalls using your `tips` and `common_mistakes`"

"""
],
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
