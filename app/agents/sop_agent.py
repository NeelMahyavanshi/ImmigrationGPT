
from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openrouter import OpenRouter
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.google import Gemini
from agno.tools.file_generation import FileGenerationTools
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from pathlib import Path
from agno.tools import tool
import re
import os
from agno.db.postgres import PostgresDb

load_dotenv()   


db = PostgresDb(
    db_url=os.getenv("DATABASE_URL"),
    memory_table=os.getenv("AGNO_MEMORY_TABLE", "agno_memories"),
)

def get_sop_stylesheet():
    """
    Returns a custom, idempotent stylesheet for the SOP to prevent KeyErrors.
    """
    styles = getSampleStyleSheet()
    # Create custom styles without assuming they don't exist
    styles.add(ParagraphStyle(name='SOP-Heading1', fontSize=16, leading=22, spaceAfter=18, alignment=TA_CENTER, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='SOP-Heading2', fontSize=12, leading=16, spaceAfter=12, alignment=TA_LEFT, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='SOP-Body', fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=10))
    return styles

@tool(
    name="generate_professional_pdf",
    description="Generates a clean, professional PDF with headings, paragraphs, and page numbers."
)
def generate_professional_pdf(filename: str, content: str, output_directory: str, header_text: str = "") -> str:
    """
    Generates a high-quality PDF from text with markdown-style headings.
    """
    output_path = Path(output_directory) / filename
    doc = SimpleDocTemplate(str(output_path), pagesize=(8.5 * inch, 11 * inch), topMargin=inch, bottomMargin=inch)
    
    styles = get_sop_stylesheet() # <-- Use the safe stylesheet function

    story = []
    lines = content.strip().split('\n')
    current_paragraph = ""

    for line in lines:
        line = line.strip()
        if not line:
            if current_paragraph:
                story.append(Paragraph(current_paragraph, styles['SOP-Body']))
                current_paragraph = ""
        elif line.startswith('## '):
            if current_paragraph:
                story.append(Paragraph(current_paragraph, styles['SOP-Body']))
            story.append(Paragraph(line.replace('## ', '').strip(), styles['SOP-Heading2']))
            current_paragraph = ""
        elif line.startswith('# '):
            if current_paragraph:
                story.append(Paragraph(current_paragraph, styles['SOP-Body']))
            story.append(Paragraph(line.replace('# ', '').strip(), styles['SOP-Heading1']))
            current_paragraph = ""
        else:
            current_paragraph += line + " "

    if current_paragraph:
        story.append(Paragraph(current_paragraph, styles['SOP-Body']))

    def add_header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        if header_text:
            canvas.drawString(inch, 10.5 * inch, header_text)
        page_num = f"Page {canvas.getPageNumber()}"
        canvas.drawRightString(7.5 * inch, 0.5 * inch, page_num)
        canvas.restoreState()

    try:
        doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        return f"Successfully generated formatted PDF: {output_path}"
    except Exception as e:
        return f"Error generating PDF: {e}"

universal_instructions_concise = """
You are a universal document drafting expert. Your mission is to generate a professional PDF tailored to the user's request.

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

## WORKFLOW
1.  **Identify Document Type**: Determine if the user wants an 'SOP for Study Permit', 'Resume', 'LOR', or 'SOP after Refusal'.
2.  **Select Protocol**: Silently choose the correct protocol for that document type.
    -   **SOP**: Focus on genuine intent, program fit, and ties to home country.
    -   **Resume**: Focus on quantified achievements and skills relevant to a target role.
    -   **LOR**: Write from the recommender's perspective, using specific examples of the applicant's strengths.
    -   **Refusal SOP**: Directly and respectfully address the reasons for the prior refusal.
3.  **Research (If Needed)**: Use `GoogleSearchTools` to find specific, verifiable details (e.g., university courses, faculty, visa requirements).
4.  **Draft Text**: Write the complete document text. Use markdown for headings (`# Title`, `## Section`) and double newlines for paragraphs.
5.  **Generate PDF**: Call `generate_professional_pdf` with the drafted text, a descriptive filename, and the applicant's name as the header. Your FINAL action must be this tool call.
"""

# --- Create the Agent ---
sop_agent = Agent(
    # model=Groq(id="openai/gpt-oss-120b", temperature=0.2),
    model=Gemini(id="gemini-2.5-flash"),
    db=db,
    enable_user_memories=True,    
    add_memories_to_context=True,
    tools=[
        GoogleSearchTools(),
        generate_professional_pdf
    ],
    role="You are a universal document drafting expert for admissions and immigration.",
    name="Universal_Doc_Agent",
    instructions=universal_instructions_concise, 
    markdown=False,
)

# --- Example Run (Same as before) ---
# if __name__ == "__main__":
#     response = sop_agent.run(
#         """
#         I was refused a study permit in 2024 due to unclear financial proof and weak home ties.
#         Now I have a fixed deposit of CAD 50,000 and a job offer from my uncle’s company in Mumbai.
#         Write a new SOP addressing these concerns for UBC MEng in AI.
#         Name: Priya Mehta, Citizenship: Indian.

#         """
#     )
#     print(response.content)