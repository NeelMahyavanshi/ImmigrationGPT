import json
import re
from pathlib import Path
from typing import Dict, List, Any

# ============================================================================
# LOAD ELIGIBILITY RULES (Once at startup)
# ============================================================================
with open((Path(__file__).parent / 'canadian_immigration_programs.json'), 'r', encoding='utf-8') as f:
    ELIGIBILITY_RULES = json.load(f)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_min_clb(clb_text: str, noc_teer: str = "0") -> int:
    """
    Parse CLB requirements like:
    - "CLB 7"
    - "CLB 7 for NOC TEER 0 or 1; CLB 5 for NOC TEER 2 or 3"
    - "No minimum for eligibility, but affects selection points"
    
    Returns the minimum CLB required for the given NOC TEER level.
    """
    if not clb_text or not isinstance(clb_text, str):
        return 0
    
    # Handle "no minimum" cases
    if "no minimum" in clb_text.lower():
        return 0
    
    # Find all CLB numbers in text
    all_clbs = [int(m) for m in re.findall(r'CLB\s*(\d+)', clb_text)]
    if not all_clbs:
        return 0
    
    # Try to match specific TEER level
    for segment in clb_text.split(';'):
        if f"TEER {noc_teer}" in segment or f"NOC {noc_teer}" in segment:
            nums = [int(m) for m in re.findall(r'CLB\s*(\d+)', segment)]
            if nums:
                return nums[0]
    
    # Fallback: return minimum CLB found
    return min(all_clbs)


def compare_education(applicant_level: str, required_level: str) -> bool:
    """
    Compare education levels with hierarchy understanding.
    Returns True if applicant meets or exceeds requirement.
    """
    if not required_level or "not required" in required_level.lower():
        return True
    
    app = applicant_level.lower().strip()
    req = required_level.lower().strip()
    
    # Education hierarchy (lowest to highest)
    levels = [
        "less than high school",
        "high school",
        "secondary school",
        "diploma",
        "certificate",
        "post-secondary",
        "associate degree",
        "bachelor",
        "bachelor's degree",
        "masters",
        "master's degree",
        "phd",
        "doctorate"
    ]
    
    # Normalize common variations
    app = app.replace("'s degree", "").replace(" degree", "")
    req = req.replace("'s degree", "").replace(" degree", "")
    
    # Direct match
    if app in req or req in app:
        return True
    
    # Hierarchical comparison
    app_idx = next((i for i, lvl in enumerate(levels) if lvl in app), -1)
    req_idx = next((i for i, lvl in enumerate(levels) if lvl in req), -1)
    
    if app_idx >= 0 and req_idx >= 0:
        return app_idx >= req_idx
    
    return False


def check_work_experience(applicant: Dict, rules: Dict) -> tuple[bool, str]:
    """Check work experience requirements"""
    work_rules = rules.get('work_experience', {})
    
    min_years = work_rules.get('min_years')
    if min_years is None:
        return True, "No work experience required"
    
    applicant_years = applicant.get('work_experience_years', 0)
    
    # Check Canadian experience requirement
    canadian_required = work_rules.get('canadian_experience_required', False)
    has_canadian_exp = applicant.get('has_canadian_experience', False)
    
    if canadian_required and not has_canadian_exp:
        return False, f"Canadian work experience required"
    
    if applicant_years >= min_years:
        return True, f"Meets work experience requirement ({applicant_years} years)"
    else:
        return False, f"Need {min_years} years, have {applicant_years} years"


def check_language(applicant: Dict, rules: Dict) -> tuple[bool, str]:
    """Check language requirements"""
    lang_rules = rules.get('language', {})
    
    english_min = lang_rules.get('english_min', '')
    if not english_min:
        return True, "No language requirement"
    
    noc_teer = str(applicant.get('noc_teer_level', '0'))
    min_clb = extract_min_clb(english_min, noc_teer)
    
    if min_clb == 0:
        return True, "No minimum CLB required"
    
    applicant_clb = applicant.get('clb_score', 0)
    
    if applicant_clb >= min_clb:
        return True, f"Meets language requirement (CLB {applicant_clb})"
    else:
        return False, f"Need CLB {min_clb}, have CLB {applicant_clb}"


def check_education(applicant: Dict, rules: Dict) -> tuple[bool, str]:
    """Check education requirements"""
    edu_rules = rules.get('education', {})
    
    min_level = edu_rules.get('min_level', '')
    if not min_level:
        return True, "No education requirement"
    
    applicant_level = applicant.get('education_level', '')
    
    if compare_education(applicant_level, min_level):
        return True, f"Meets education requirement"
    else:
        return False, f"Need {min_level}, have {applicant_level}"


def check_age(applicant: Dict, rules: Dict) -> tuple[bool, str]:
    """Check age requirements"""
    age_rules = rules.get('age', {})
    applicant_age = applicant.get('age')
    
    if not applicant_age:
        return True, "Age not evaluated"
    
    min_age = age_rules.get('min_age')
    max_age = age_rules.get('max_age')
    
    if min_age and applicant_age < min_age:
        return False, f"Minimum age {min_age} required"
    
    if max_age and applicant_age > max_age:
        return False, f"Maximum age {max_age} exceeded"
    
    return True, "Meets age requirement"


def check_settlement_funds(applicant: Dict, rules: Dict) -> tuple[bool, str]:
    """Check settlement funds requirements"""
    funds_rules = rules.get('settlement_funds', {})
    
    if not funds_rules.get('required', False):
        return True, "Settlement funds not required"
    
    family_size = applicant.get('family_size', 1)
    applicant_funds = applicant.get('settlement_funds_cad', 0)
    
    funds_table = funds_rules.get('table_cad', {})
    required_funds = funds_table.get(family_size, funds_table.get(7, 0))
    
    if family_size > 7:
        additional_per_person = funds_table.get('additional_per_person', 0)
        required_funds += (family_size - 7) * additional_per_person
    
    if applicant_funds >= required_funds:
        return True, f"Meets settlement funds requirement"
    else:
        return False, f"Need ${required_funds:,} CAD, have ${applicant_funds:,} CAD"


def check_job_offer(applicant: Dict, rules: Dict) -> tuple[bool, str]:
    """Check job offer requirements"""
    connection_rules = rules.get('connection_requirements', {})
    
    job_offer_required = connection_rules.get('job_offer_required', False)
    has_job_offer = applicant.get('has_job_offer', False)
    
    if job_offer_required and not has_job_offer:
        return False, "Valid job offer required"
    
    return True, "Job offer requirement met" if has_job_offer else "No job offer required"


# ============================================================================
# MAIN ELIGIBILITY EVALUATION FUNCTION
# ============================================================================

def evaluate_eligibility(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate user eligibility for all Canadian immigration programs.
    
    Args:
        user_profile: Dict containing:
            - work_experience_years (float): Years of work experience
            - education_level (str): Highest education level
            - clb_score (int): Canadian Language Benchmark score
            - noc_teer_level (str): NOC TEER category ("0", "1", "2", "3", "4", "5")
            - age (int, optional): Age in years
            - has_canadian_experience (bool, optional): Canadian work experience
            - has_job_offer (bool, optional): Valid job offer
            - settlement_funds_cad (float, optional): Available settlement funds
            - family_size (int, optional): Number of family members
    
    Returns:
        Dict containing:
            - eligible_programs: List of programs user qualifies for
            - ineligible_programs: List of programs user doesn't qualify for
            - total_evaluated: Total number of programs evaluated
    """
    
    eligible_programs = []
    ineligible_programs = []
    
    for program in ELIGIBILITY_RULES['programs']:
        rules = program.get('eligibility_rules', {})
        
        # Run all checks
        checks = {
            'work_experience': check_work_experience(user_profile, rules),
            'language': check_language(user_profile, rules),
            'education': check_education(user_profile, rules),
            'age': check_age(user_profile, rules),
            'settlement_funds': check_settlement_funds(user_profile, rules),
            'job_offer': check_job_offer(user_profile, rules)
        }
        
        # Determine if all checks passed
        all_passed = all(check[0] for check in checks.values())
        failed_checks = {k: v[1] for k, v in checks.items() if not v[0]}
        passed_checks = {k: v[1] for k, v in checks.items() if v[0]}
        
        program_result = {
            'program_name': program['program_name'],
            'official_url': program['official_url'],
            'type': program.get('federal_or_provincial', 'unknown'),
            'province': program.get('province'),
            'last_updated': program.get('last_updated')
        }
        
        if all_passed:
            program_result['status'] = 'eligible'
            program_result['details'] = passed_checks
            eligible_programs.append(program_result)
        else:
            program_result['status'] = 'ineligible'
            program_result['failed_requirements'] = failed_checks
            ineligible_programs.append(program_result)
    
    return {
        'eligible_programs': eligible_programs,
        'ineligible_programs': ineligible_programs,
        'total_evaluated': len(ELIGIBILITY_RULES['programs']),
        'summary': {
            'eligible_count': len(eligible_programs),
            'ineligible_count': len(ineligible_programs)
        }
    }




if __name__ == "__main__":
    # Test case
    sample_applicant = {
        "work_experience_years": 3,
        "education_level": "bachelor",
        "clb_score": 8,
        "noc_teer_level": "1",
        "age": 30,
        "has_canadian_experience": False,
        "has_job_offer": False,
        "settlement_funds_cad": 20000,
        "family_size": 1
    }
    
    results = evaluate_eligibility(sample_applicant)
    
    print(f"\n{'='*80}")
    print(f"ELIGIBILITY EVALUATION RESULTS")
    print(f"{'='*80}")
    print(f"\nEligible Programs: {results['summary']['eligible_count']}")
    print(f"Ineligible Programs: {results['summary']['ineligible_count']}")
    
    print(f"\n{'='*80}")
    print("ELIGIBLE PROGRAMS:")
    print(f"{'='*80}")
    for prog in results['eligible_programs']:
        print(f"\n✓ {prog['program_name']}")
        print(f"  Type: {prog['type']}")
        print(f"  URL: {prog['official_url']}")
    
    if results['ineligible_programs']:
        print(f"\n{'='*80}")
        print("INELIGIBLE PROGRAMS (First 3):")
        print(f"{'='*80}")
        for prog in results['ineligible_programs'][:3]:
            print(f"\n✗ {prog['program_name']}")
            print(f"  Failed requirements:")
            for req, reason in prog['failed_requirements'].items():
                print(f"    - {req}: {reason}")
