from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.google import Gemini
from agno.tools.function import ToolResult
from agno.media import File
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from agno.tools import tool
import os
import sys
from agno.db.postgres import PostgresDb
from typing import List, Optional
from pydantic import BaseModel, Field
from supabase import create_client, Client
from io import BytesIO
import logging
import re
import unicodedata
import json


sys.path.insert(0, str(Path(__file__).resolve().parents[2])) 
from config import GENERATED_FILES_DIR_STR as GENERATED_FILES_DIR

load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SOPAgentResponse(BaseModel):
    reply: str
    files: Optional[List[str]] = Field(default_factory=list)

db = PostgresDb(
    db_url=os.getenv("DATABASE_URL"),
    memory_table=os.getenv("AGNO_MEMORY_TABLE", "agno_memories"),
)

# --------------- Typography helpers ---------------

def _register_fonts():
    """Register a Unicode-friendly font; fallback to Helvetica if missing."""
    try:
        fonts_dir = Path(__file__).resolve().parents[2] / "fonts"
        pdfmetrics.registerFont(TTFont("DejaVu", str(fonts_dir / "DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(fonts_dir / "DejaVuSans-Bold.ttf")))
        return "DejaVu", "DejaVu-Bold"
    except Exception:
        return "Helvetica", "Helvetica-Bold"

BASE_FONT, BASE_FONT_BOLD = _register_fonts()

def normalize_punctuation(text: str) -> str:
    """Fix smart quotes/dashes/NBSP and other glyphs that render as squares."""
    if not text:
        return text
    t = unicodedata.normalize("NFKC", text)
    replacements = {
        "\u2018": "'", "\u2019": "'", "\u201A": "'", "\u201B": "'",
        "\u201C": '"', "\u201D": '"', "\u201E": '"',
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-", "\u2212": "-",
        "\u00A0": " ", "\u2022": "-", "\u25AA": "-", "\u25A0": "-", "\u2026": "..."
    }
    for bad, good in replacements.items():
        t = t.replace(bad, good)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t

def markdown_to_html_minimal(text: str) -> str:
    """Convert **bold** and *italic* to <b>/<i> for ReportLab Paragraph."""
    if not text:
        return text
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    t = re.sub(r"^\s*-{3,}\s*$", "", t, flags=re.MULTILINE)
    return t

def preprocess(text: str) -> str:
    return markdown_to_html_minimal(normalize_punctuation(text))

def get_sop_stylesheet():
    styles = getSampleStyleSheet()
    # base
    styles["Normal"].fontName = BASE_FONT
    styles["Normal"].fontSize = 11
    styles["Normal"].leading = 15
    styles["Heading1"].fontName = BASE_FONT_BOLD
    styles["Heading2"].fontName = BASE_FONT_BOLD
    # custom
    if "SOP-Heading1" not in styles:
        styles.add(ParagraphStyle(name="SOP-Heading1", fontName=BASE_FONT_BOLD,
                                  fontSize=16, leading=22, spaceAfter=18, alignment=TA_CENTER))
    if "SOP-Heading2" not in styles:
        styles.add(ParagraphStyle(name="SOP-Heading2", fontName=BASE_FONT_BOLD,
                                  fontSize=12, leading=16, spaceAfter=10, alignment=TA_LEFT))
    if "SOP-Body" not in styles:
        styles.add(ParagraphStyle(name="SOP-Body", fontName=BASE_FONT,
                                  fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=8))
    if "SOP-Small" not in styles:
        styles.add(ParagraphStyle(name="SOP-Small", fontName=BASE_FONT,
                                  fontSize=9, leading=12, alignment=TA_LEFT, textColor="#555555"))
    return styles

# --------------- PDF tool ---------------

@tool(
    name="generate_professional_pdf",
    description="Generates a clean, professional PDF and uploads it to Supabase Storage."
)
def generate_professional_pdf(
    filename: str,
    content: str,
    user_id: str,
    output_directory: str,
    header_text: str = ""
) -> ToolResult:
    """
    - Normalizes punctuation to avoid black squares.
    - Converts minimal Markdown (**bold**/*italic*) to HTML (<b>/<i>).
    - Uses a Unicode-safe font.
    - Adds signature block on a new page if the text requests it.
    - Uploads to Supabase and returns the public URL.
    """
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=(8.5 * inch, 11 * inch),
            topMargin=0.9 * inch, bottomMargin=0.8 * inch,
            leftMargin=0.85 * inch, rightMargin=0.85 * inch
        )
        styles = get_sop_stylesheet()
        story = []

        lines = content.split("\n")
        current_paragraph = ""

        def flush_paragraph():
            nonlocal current_paragraph
            if current_paragraph.strip():
                story.append(Paragraph(preprocess(current_paragraph.strip()), styles["SOP-Body"]))
                current_paragraph = ""

        for raw in lines:
            line = raw.rstrip("\n")
            if not line.strip():
                flush_paragraph()
                story.append(Spacer(1, 6))
                continue
            if line.startswith("## "):
                flush_paragraph()
                story.append(Paragraph(preprocess(line[3:].strip()), styles["SOP-Heading2"]))
                continue
            if line.startswith("# "):
                flush_paragraph()
                story.append(Paragraph(preprocess(line[2:].strip()), styles["SOP-Heading1"]))
                continue
            current_paragraph += (" " + line.strip())

        flush_paragraph()

        wants_signature = ("Applicant Signature" in content) or ("Signature:" in content)
        if wants_signature:
            story.append(PageBreak())
            story.append(Paragraph(preprocess("Signature"), styles["SOP-Heading2"]))
            story.append(Spacer(1, 8))
            story.append(Paragraph(preprocess("Applicant Signature: _____________________________"), styles["SOP-Body"]))
            story.append(Paragraph(preprocess("Date: __________________"), styles["SOP-Body"]))

        def add_header_footer(canvas, _doc):
            canvas.saveState()
            canvas.setFont(BASE_FONT, 9)
            if header_text:
                canvas.drawString(0.85 * inch, 10.75 * inch, normalize_punctuation(header_text))
            page_num = f"Page {canvas.getPageNumber()}"
            canvas.drawRightString(7.65 * inch, 0.55 * inch, page_num)
            canvas.restoreState()

        doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        # Optional local save
        if os.getenv("SAVE_LOCAL_PDF", "false").lower() == "true":
            os.makedirs(output_directory, exist_ok=True)
            with open(os.path.join(output_directory, filename), "wb") as f:
                f.write(pdf_bytes)

        # Upload to Supabase
        storage_path = f"{user_id}/{filename}"
        supabase.storage.from_("user_documents").upload(
            path=storage_path, file=pdf_bytes,
            file_options={"content-type": "application/pdf", "upsert": "true"}
        )
        public_url = supabase.storage.from_("user_documents").get_public_url(storage_path)

        pdf_file = File(content=pdf_bytes, name=filename, url=public_url, content_type="application/pdf")
        return ToolResult(content=f"Successfully generated and uploaded {filename}", files=[pdf_file])

    except Exception as e:
        logger.error(f"PDF generation/upload error: {e}", exc_info=True)
        return ToolResult(content=f"Error generating PDF: {e}", files=[])


universal_instructions_concise = """
You are a professional document drafting engine. Your sole task: generate a polished immigration document as a PDF.

## 🧠 FIRST: CONSULT USER MEMORY
First, review all stored user information: name, occupation, education, work history, language scores, and their stated immigration goals.

## ❓ ONE CLARIFYING QUESTION (If Critical Info Missing)
Ask **only if the document type or target is unclear**:
- “Is this SOP for a Study Permit, PR application, or Expression of Interest?”
- “What is the exact name of your target program and institution?”

If non-critical info is missing (e.g., full name), use placeholders like `[Your Name]`.

## 📝 DRAFTING & TOOL USE
- Select the correct drafting framework based on the user's confirmed purpose (SOP, EOI, LOR, etc.).
- Select the correct framework:
  → Study Permit SOP (For university admissions: Around 800–1,000 words amd For student visa applications: A more concise range of 500–700 words, it should have temporary intent, home ties)
  → PR Letter (100–200 words, clear ask, background, relevance)
  → EOI (300–600 words, skills, provincial alignment)
  → LOR (300–600 words, recommender identity, concrete examples)
- Draft full content in clean markdown.
- **Immediately call `generate_professional_pdf`** with:
  → filename: `<DocType>_<Placeholder>_<Program>.pdf`
  → content: full drafted text
  → user_id, output_directory, header_text

## 🚫 HARD RULES
- Ask all the necessary clarifying questions **upfront**; do not generate partial drafts.
- Use placeholders for any non-critical missing info.
- **Never draft a document without a clear, confirmed purpose.**
- Never mention JSON, formatting, or your own limitations.
- Never refuse to generate — use placeholders if needed.
- Your only allowed tool is `generate_professional_pdf`.

"""


# --- Create the Agent ---
sop_agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    parser_model=Gemini(id="gemini-2.0-flash"),
    db=db,
    enable_agentic_memory = True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=3,
    search_session_history=True,
    add_memories_to_context=True,
    tools=[
        generate_professional_pdf,
    ],
    role="You are a universal document drafting expert for admissions and immigration.",
    name="Universal_Doc_Agent",
    instructions=universal_instructions_concise,
    markdown=False,
    output_schema=SOPAgentResponse,
)

import json
# --- Example Run ---
if __name__ == "__main__":    
    res = sop_agent.run("""
    Write a Statement of Purpose for Ananya Singh, a 24-year-old Indian applicant with a B.Tech in Computer Science from IIT Delhi, 
    applying for MSc Computer Science at UofT. She has 2 years experience at Infosys as a Software Engineer, strong coding skills,
    and a passion for AI research. She aims to contribute to AI advancements in healthcare post-graduation.
    """
    )
    json_output = json.loads(res.content.model_dump_json())
    print(json_output)
    print(f"Agent reply: {res.content}")
    print(f"\nGenerated files:")
    if res.files:
        for file in res.files:
            print(f"  - {file.name} (url: {file.url})")
            print(f"    Size: {len(file.content)} bytes")
    else:
        print(" No files generated")

