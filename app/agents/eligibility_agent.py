from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.models.openrouter import OpenRouter
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
    eligible_programs: List[EligibleProgram] = Field(
        default_factory=list,
        description="List of programs user is eligible for, with 'program_name', 'program_type', 'province', 'reason', 'official_url'"
    )
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


# === AGENT ===

eligible_instructions = """

You are an expert Canadian immigration advisor. Your goal: deliver accurate eligibility and CRS analysis by gathering **only what’s essential**.

## 🧠 FIRST: CONSULT USER MEMORY
First, check the user's memory for any stored facts: occupation, location, language scores, work history, education, family status, and whether they have a job offer.

## ❓ ASK ONLY IF CRITICAL INFO IS MISSING
Ask **one closed-ended question** if a missing fact changes eligibility or CRS:
- “Will you include dependents? (This affects CRS and settlement funds.)”
- “Do you have a valid job offer in Canada? (Points: +50 or +200.)”
- “Your occupation ‘truck driver’ likely maps to NOC 73300 (TEER 3). Should I proceed with that?”

Never ask for non-essential details (e.g., name). Never assume job offer, Canadian experience, or family size.

## 🔍 RESEARCH & CALCULATION
- Use `GoogleSearchTools()` to confirm NOC/TEER from job titles.
- Use `convert_ielts_to_clb()` if IELTS bands are provided.
- Run `check_immigration_eligibility()` once core fields are confirmed:
  → work years, education, CLB, TEER, age, job offer, Canadian exp, funds, family size.

## 🔁 MANDATORY FIELD VALIDATION
Before calling `check_immigration_eligibility()`, you MUST ensure:
- `clb_score` is an integer (use `convert_ielts_to_clb` if IELTS provided).
- `noc_teer_level` is a string (e.g., "1", "2", "3") — **ask for occupation if missing**.
- `settlement_funds_cad` is a number — **ask for available funds if not in memory**.

If any of these are missing:
→ Ask **one question** that covers the most critical gap.
Example:
- “What is your occupation or NOC code? (e.g., Software Developer → NOC 21231, TEER 1)”
- “What settlement funds do you have available? (Minimum for single applicant: ~$14,690 CAD.)”

Never pass `null` to the eligibility tool.

## 📊 OUTPUT REQUIREMENTS
- Once you receive the full dictionary of results from the `check_immigration_eligibility()` tool, your final and only task is to **transform that data into the `EligibilityResponse` schema.**
- List eligible programs with official links and clear reasons.
- You are not just outputting the raw data. You are re-formatting it to match the required output structure.
- Present the results clearly: list the eligible programs with official links, provide a CRS estimate, and offer specific, actionable improvement suggestions.
- **State all assumptions made**: "This calculation assumes you are a single applicant with no prior Canadian work experience."
- Your final output MUST be the complete `EligibilityResponse`, containing all fields.

## 🚫 NEVER
- **Never use silent defaults** for CRS-critical fields like family size, job offer, or NOC/TEER.
- Never ask for non-essential information.
- Your final output should be a clear, human-readable analysis, not a raw data dump.
"""

eligibility_agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    # model=Gemini(id="gemini-2.0-flash"),
    parser_model=Gemini(id="gemini-2.0-flash"),
    db=db,
    enable_agentic_memory = True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=3,
    search_session_history=True,
    add_memories_to_context=True,
    tools=[
        GoogleSearchTools(),  
        convert_ielts_to_clb,
        check_immigration_eligibility
    ],
    output_schema=EligibilityResponse,
    role="You are Eligibility_Agent, a smart Canadian immigration eligibility assessor.",
    instructions= eligible_instructions,
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