from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.tools.googlesearch import GoogleSearchTools
from dotenv import load_dotenv
from pathlib import Path
import json
import sys
from typing import Dict, Any
from rich.pretty import pprint 
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from agno.db.postgres import PostgresDb

load_dotenv()

db = PostgresDb(
    db_url=os.getenv("DATABASE_URL"),
    memory_table=os.getenv("AGNO_MEMORY_TABLE", "agno_memories"),
)

# === PYDANTIC SCHEMA ===

class EligibleProgram(BaseModel):
    program_name: str
    program_type: Optional[str] = "Unknown" 
    province: Optional[str] = None
    official_url: str
    reason: str

class IneligibleProgram(BaseModel):
    program_name: str
    missing_requirements: List[str]

class ImprovementSuggestion(BaseModel):
    action: str
    benefit: str
    steps: List[str]

class UserProfile(BaseModel):
    work_experience_years: float
    education_level: str
    clb_score: int
    noc_teer_level: str
    age: int
    has_canadian_experience: bool
    has_job_offer: bool
    settlement_funds_cad: float
    family_size: int

class EligibilityResponse(BaseModel):
    user_profile: UserProfile  # Changed from dict to UserProfile
    eligible_programs: List[EligibleProgram]
    ineligible_programs: List[IneligibleProgram]
    crs_estimate: Optional[int] = None
    improvement_suggestions: List[ImprovementSuggestion]
    next_steps: List[str]
    requires_follow_up: bool


# PATH SETUP (VERIFIED TO WORK)
AGENTS_DIR = Path(__file__).parent
RULES_DIR = AGENTS_DIR / "eligibility_rules"
JSON_PATH = Path(__file__).parent / "eligibility_rules" / "canadian_immigration_programs.json"

 
# LOAD ELIGIBILITY RULES

with open((Path(__file__).parent / 'eligibility_rules' / 'canadian_immigration_programs.json'), 'r', encoding='utf-8') as f:
    ELIGIBILITY_RULES = json.load(f)


sys.path.insert(0, str(AGENTS_DIR))
from eligibility_rules.eligibility_checker import evaluate_eligibility

# SMART HELPER TOOLS

def convert_ielts_to_clb(
    reading: float = None,
    writing: float = None,
    listening: float = None,
    speaking: float = None
) -> str:
    """
    Convert IELTS scores to Canadian Language Benchmark (CLB) levels.
    
    Args:
        reading: IELTS Reading score (0-9)
        writing: IELTS Writing score (0-9)
        listening: IELTS Listening score (0-9)
        speaking: IELTS Speaking score (0-9)
    
    Returns:
        CLB equivalents and overall assessment
    """
    
    def ielts_to_clb_single(score: float, skill: str) -> int:
        """Convert single IELTS score to CLB"""
        if skill in ['reading']:
            if score >= 8.0: return 10
            elif score >= 7.0: return 9
            elif score >= 6.5: return 8
            elif score >= 6.0: return 7
            elif score >= 5.0: return 6
            elif score >= 4.0: return 5
            else: return 4
        elif skill in ['writing']:
            if score >= 7.5: return 10
            elif score >= 7.0: return 9
            elif score >= 6.5: return 8
            elif score >= 6.0: return 7
            elif score >= 5.5: return 6
            elif score >= 5.0: return 5
            else: return 4
        elif skill in ['listening']:
            if score >= 8.5: return 10
            elif score >= 8.0: return 9
            elif score >= 7.5: return 8
            elif score >= 6.0: return 7
            elif score >= 5.5: return 6
            elif score >= 5.0: return 5
            else: return 4
        elif skill in ['speaking']:
            if score >= 7.5: return 10
            elif score >= 7.0: return 9
            elif score >= 6.5: return 8
            elif score >= 6.0: return 7
            elif score >= 5.5: return 6
            elif score >= 5.0: return 5
            else: return 4
        return 4
    
    output = "**IELTS to CLB Conversion:**\n\n"
    clb_scores = []
    
    if reading:
        clb = ielts_to_clb_single(reading, 'reading')
        output += f"- Reading: IELTS {reading} = **CLB {clb}**\n"
        clb_scores.append(clb)
    
    if writing:
        clb = ielts_to_clb_single(writing, 'writing')
        output += f"- Writing: IELTS {writing} = **CLB {clb}**\n"
        clb_scores.append(clb)
    
    if listening:
        clb = ielts_to_clb_single(listening, 'listening')
        output += f"- Listening: IELTS {listening} = **CLB {clb}**\n"
        clb_scores.append(clb)
    
    if speaking:
        clb = ielts_to_clb_single(speaking, 'speaking')
        output += f"- Speaking: IELTS {speaking} = **CLB {clb}**\n"
        clb_scores.append(clb)
    
    if clb_scores:
        min_clb = min(clb_scores)
        output += f"\n**Overall CLB Level**: {min_clb} (minimum across all skills)\n"
        output += f"\n*For immigration purposes, your CLB level is typically the lowest score across all four abilities.*"
    
    return output


def check_immigration_eligibility(
    work_experience_years: float,
    education_level: str,
    clb_score: int,
    noc_teer_level: str = "1",
    age: int = 30,
    has_canadian_experience: bool = False,
    has_job_offer: bool = False,
    settlement_funds_cad: float = 0,
    family_size: int = 1
) -> str:
    """
    Check Canadian immigration program eligibility.
    [Same as before]
    """
    
    user_profile = {
        "work_experience_years": work_experience_years,
        "education_level": education_level,
        "clb_score": clb_score,
        "noc_teer_level": str(noc_teer_level),
        "age": age,
        "has_canadian_experience": has_canadian_experience,
        "has_job_offer": has_job_offer,
        "settlement_funds_cad": settlement_funds_cad,
        "family_size": family_size
    }
    
    results = evaluate_eligibility(user_profile)
    
    output = "**🇨🇦 Canadian Immigration Eligibility Assessment**\n\n"
    output += f"✅ **Eligible Programs: {results['summary']['eligible_count']}**\n\n"
    
    if results['eligible_programs']:
        output += "### ✨ Programs You Qualify For:\n\n"
        for i, prog in enumerate(results['eligible_programs'], 1):
            output += f"{i}. **{prog['program_name']}**\n"
            output += f"   - Type: {prog['type']}\n"
            if prog.get('province'):
                output += f"   - Province: {prog['province']}\n"
            output += f"   - [Official Information]({prog['official_url']})\n\n"
    else:
        output += "### 📋 Assessment Results\n\n"
        output += "You don't currently meet minimum requirements for the evaluated programs.\n\n"
    
    return output

# 
# CREATE ENHANCED AGENT
# 

eligibility_agent = Agent(
    name="ImmigrationEligibilityAgent",
    model=Groq(id="openai/gpt-oss-120b"),
    parser_model=Gemini(id="gemini-2.0-flash"),
    db=db,
    enable_user_memories=True,    
    add_memories_to_context=True,
    tools=[
        GoogleSearchTools(),  
        convert_ielts_to_clb,
        check_immigration_eligibility
    ],
    output_schema=EligibilityResponse,
    role="You are an expert Canadian immigration advisor with access to search tools.",
    instructions=[
        "You are an expert Canadian immigration advisor with access to search tools.",
        "",
        """
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
        
        """
        "## Smart Assessment Strategy:",
        "",
        "1. **Understand the user's profile** from their message",
        "2. **Automatically look up missing info:**",
        "   - If they mention a job title, call GoogleSearchTools() to get TEER level",
        "   - If they give IELTS scores, call convert_ielts_to_clb()",
        "   - Use Google search for current program updates or specific questions",
        "",
        "3. **Infer reasonable defaults:**",
        "   - If they say 'bachelor's degree' → education_level='bachelor'",
        "   - If they say 'IELTS 7' without breakdown → assume CLB 7-8",
        "   - Assume family_size=1 unless mentioned",
        "   - Assume no job offer/Canadian experience unless stated",
        "",
        "4. **Be proactive, not interrogative:**",
        "   - DON'T ask for every single field one by one",
        "   - Extract what you can from their message",
        "   - Look up what you can automatically",
        "   - Only ask for critical missing info",
        "",
        "5. **Run eligibility check quickly:**",
        "   - Once you have: work years, education, language (CLB), TEER → call check_immigration_eligibility()",
        "   - Use reasonable estimates for optional fields",
        "",
        "6. **Present results professionally:**",
        "   - Show eligible programs first",
        "   - Explain why they qualify",
        "   - Suggest next steps",
        "",
        "## Example Flow:",
        "User: 'I'm a software engineer with 3 years experience, bachelor's, IELTS 7'",
        "You:",
        "1. Call find_noc_code('software engineer') → get TEER 1",
        "2. Assume CLB 7-8 from IELTS 7 (or convert if needed)",
        "3. Call check_immigration_eligibility(3, 'bachelor', 7, '1', 30, False, False, 0, 1)",
        "4. Present results immediately",
        "",
        "## Tools Usage:",
        "- convert_ielts_to_clb: When IELTS scores given",
        "- GoogleSearchTools: For NOC lookups, Teer lookups, program updates, specific questions",
        "- check_immigration_eligibility: Once you have core profile data",
        "",
        "Be helpful, efficient, and solution-focused!"
    ],
    markdown=False,
)


# if __name__ == "__main__":
#     print("\n" + "="*80)
#     print("🇨🇦 SMART CANADIAN IMMIGRATION ELIGIBILITY AGENT")
#     print("="*80 + "\n")
    
#     result = eligibility_agent.run(
#         "Hi! I have 3 years as a truck driver, hold a college, CLB 8, age 30."
#     )
#     pprint(result.content)