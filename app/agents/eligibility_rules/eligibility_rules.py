
# Create a comprehensive structured YAML output for Canadian immigration programs
# This will compile all the data gathered from official sources

import yaml
from datetime import datetime

# Define the complete immigration programs data structure
immigration_data = {
    "metadata": {
        "extraction_date": "2025-10-17",
        "data_sources": "Official IRCC, Provincial Government websites",
        "last_verified": "2025-10-17",
        "warning": "Immigration rules change frequently. Always verify with official sources."
    },
    "programs": []
}

# FEDERAL PROGRAMS

# Express Entry - Federal Skilled Worker
fsw_program = {
    "program_name": "Federal Skilled Worker Program (FSW)",
    "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/who-can-apply/federal-skilled-workers.html ",
    "last_updated": "2024-12",
    "federal_or_provincial": "federal",
    "province": None,
    "eligibility_rules": {
        "work_experience": {
            "min_years": 1.0,
            "min_hours": 1560,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3"],
            "timeframe": "Within last 10 years",
            "canadian_experience_required": False,
            "full_time_equivalent": "30 hrs/week for 12 months = 1 year (1,560 hours)",
            "student_work_counts": True,
            "self_employed_work_counts": True
        },
        "education": {
            "min_level": "Secondary school diploma required",
            "eca_required": True,
            "eca_note": "Required for foreign education",
            "field_restricted": False,
            "field_list": None
        },
        "language": {
            "english_min": "No minimum for eligibility, but affects selection points",
            "french_min": None,
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada", "PTE Core"],
            "test_validity": "2 years",
            "second_language_bonus": True
        },
        "age": {
            "min_age": 18,
            "max_age": None,
            "optimal_range": "18-35 years",
            "max_points_age": "18-35 (12 points)"
        },
        "settlement_funds": {
            "required": True,
            "exemptions": ["Valid job offer", "Authorized to work in Canada"],
            "table_cad": {
                1: 15263,
                2: 19001,
                3: 23360,
                4: 28362,
                5: 32168,
                6: 36280,
                7: 40392,
                "additional_per_person": 4112
            },
            "table_updated": "2025-07-07"
        },
        "connection_requirements": {
            "job_offer_required": False,
            "lmia_required": False,
            "study_in_province_required": False,
            "family_in_province_accepted": False
        }
    },
    "selection_system": {
        "points_based": True,
        "total_points_possible": 100,
        "pass_mark": 67,
        "points_breakdown": {
            "education": {"max": 25, "description": "Secondary (5) to PhD (25)"},
            "language": {"max": 28, "description": "First official language (max 24) + Second language (max 4)"},
            "work_experience": {"max": 15, "description": "1 year (9) to 6+ years (15)"},
            "age": {"max": 12, "description": "18-35 years (12 points), declines after"},
            "arranged_employment": {"max": 10, "description": "Valid job offer"},
            "adaptability": {"max": 10, "description": "Spouse education, Canadian work/study, relatives"}
        },
        "note": "67 points needed for FSW selection factors. Separate CRS score determines Express Entry invitation."
    },
    "comprehensive_ranking_system": {
        "total_possible": 1200,
        "core_human_capital_max": 600,
        "additional_points_max": 600,
        "breakdown": {
            "age_without_spouse": {"max": 110, "20-29": 110, "30": 105, "40": 50, "45+": 0},
            "age_with_spouse": {"max": 100, "20-29": 100, "30": 95, "40": 45, "45+": 0},
            "education_without_spouse": {"max": 150, "PhD": 150, "Masters": 135, "Bachelors": 120},
            "education_with_spouse": {"max": 140, "PhD": 140, "Masters": 126, "Bachelors": 112},
            "language_first_without_spouse": {"max": 136, "CLB_10+_per_ability": 34},
            "language_first_with_spouse": {"max": 128, "CLB_10+_per_ability": 32},
            "language_second": {"max": 24, "CLB_9+_per_ability": 6},
            "canadian_work_experience_without_spouse": {"max": 80, "5+_years": 80, "1_year": 40},
            "canadian_work_experience_with_spouse": {"max": 70, "5+_years": 70, "1_year": 35},
            "spouse_factors": {"max": 40, "education": 10, "language": 20, "work": 10},
            "skill_transferability": {"max": 100},
            "provincial_nomination": {"points": 600},
            "job_offer_NOC_00": {"points": 200},
            "job_offer_other": {"points": 50},
            "canadian_education": {"1-2_year": 15, "3+_year": 30},
            "french_proficiency": {"NCLC_7_no_english": 25, "NCLC_7_with_CLB_5": 50},
            "sibling_in_canada": {"points": 15}
        }
    },
    "recent_draws": {
        "note": "As of October 2025, draws focused on Canadian Experience Class and category-based selection",
        "categories_2025": ["French language proficiency", "Healthcare", "STEM", "Trades", "Transport", "Agriculture"]
    }
}

# Express Entry - Canadian Experience Class
cec_program = {
    "program_name": "Canadian Experience Class (CEC)",
    "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/who-can-apply/canadian-experience-class.html ",
    "last_updated": "2024-12",
    "federal_or_provincial": "federal",
    "province": None,
    "eligibility_rules": {
        "work_experience": {
            "min_years": 1.0,
            "min_hours": 1560,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3"],
            "timeframe": "Within last 3 years",
            "canadian_experience_required": True,
            "location": "Must be in Canada",
            "full_time_equivalent": "30 hrs/week for 12 months = 1 year",
            "student_work_counts": False,
            "authorization_required": True
        },
        "education": {
            "min_level": "Not required",
            "eca_required": False,
            "note": "Can improve CRS score if provided",
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 7 for NOC TEER 0 or 1; CLB 5 for NOC TEER 2 or 3",
            "french_min": "NCLC 7 for NOC TEER 0 or 1; NCLC 5 for NOC TEER 2 or 3",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada", "PTE Core"],
            "test_validity": "2 years",
            "second_language_bonus": True
        },
        "age": {
            "min_age": 18,
            "max_age": None,
            "note": "No minimum age requirement, but affects CRS score"
        },
        "settlement_funds": {
            "required": False,
            "note": "Not required for CEC"
        },
        "connection_requirements": {
            "job_offer_required": False,
            "lmia_required": False,
            "authorized_work_required": True
        }
    },
    "selection_system": {
        "points_based": False,
        "note": "Uses Comprehensive Ranking System (CRS) for Express Entry pool ranking",
        "minimum_requirements_must_be_met": True
    }
}

# Express Entry - Federal Skilled Trades
fst_program = {
    "program_name": "Federal Skilled Trades Program (FST)",
    "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/who-can-apply/federal-skilled-trades.html ",
    "last_updated": "2024-12",
    "federal_or_provincial": "federal",
    "province": None,
    "eligibility_rules": {
        "work_experience": {
            "min_years": 2.0,
            "min_hours": 3120,
            "noc_types": ["TEER 2 and 3 skilled trades"],
            "timeframe": "Within last 5 years",
            "canadian_experience_required": False,
            "full_time_equivalent": "30 hrs/week for 24 months = 2 years",
            "eligible_trade_groups": ["Major Group 72", "Major Group 73", "Major Group 82", "Major Group 92", "Minor Group 632", "Minor Group 633"]
        },
        "education": {
            "min_level": "Not required",
            "eca_required": False,
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 5 for speaking and listening; CLB 4 for reading and writing",
            "french_min": "NCLC 5 for speaking and listening; NCLC 4 for reading and writing",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada", "PTE Core"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "exemptions": ["Valid job offer", "Authorized to work in Canada"],
            "table_cad": {
                1: 15263,
                2: 19001,
                3: 23360,
                4: 28362,
                5: 32168,
                6: 36280,
                7: 40392,
                "additional_per_person": 4112
            }
        },
        "connection_requirements": {
            "job_offer_required": "Valid job offer (1 year minimum) OR certificate of qualification",
            "certificate_of_qualification": "Issued by provincial/territorial/federal authority",
            "lmia_required": "If job offer provided"
        }
    },
    "selection_system": {
        "points_based": False,
        "note": "Uses CRS for Express Entry ranking"
    }
}

# Add federal programs
immigration_data["programs"].extend([fsw_program, cec_program, fst_program])

print("Created structured data for Express Entry programs")
print(f"Total programs so far: {len(immigration_data['programs'])}")


# Continue building immigration programs - Atlantic Immigration Program

aip_program = {
    "program_name": "Atlantic Immigration Program (AIP)",
    "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/atlantic-immigration.html ",
    "last_updated": "2021-12",
    "federal_or_provincial": "federal",
    "province": "Atlantic provinces (NB, NS, PEI, NL)",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 1.0,
            "min_hours": 1560,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3", "TEER 4"],
            "timeframe": "Within last 5 years (before job offer date)",
            "canadian_experience_required": False,
            "full_time_equivalent": "30 hrs/week for 12 months",
            "exemption": "International graduates from Atlantic Canada institutions - no work experience required"
        },
        "education": {
            "min_level": "Depends on job offer TEER category",
            "TEER_0_1": "Canadian 1-year post-secondary OR foreign equivalent with ECA",
            "TEER_2_3_4": "Canadian high school diploma OR foreign equivalent with ECA",
            "eca_required": True,
            "eca_validity": "5 years",
            "field_restricted": False
        },
        "language": {
            "english_min": "Varies by NOC TEER",
            "french_min": "Varies by NOC TEER",
            "TEER_0_1_2_3": "CLB/NCLC 5",
            "TEER_4": "CLB/NCLC 4",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": False,
            "note": "Not required if already working in Canada with valid work permit"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_duration": "At least 1 year after permanent residence",
            "employer_designation": "Must be designated Atlantic employer",
            "endorsement_required": True,
            "endorsement_issuer": "Atlantic province"
        },
        "international_graduate_requirements": {
            "education_duration": "At least 2 years",
            "institution_location": "Atlantic province (NB, NS, PEI, NL)",
            "completion_timeframe": "Within 24 months before applying for PR",
            "study_status": "Full-time",
            "residence_requirement": "At least 16 months in Atlantic province during last 2 years before graduation"
        }
    },
    "selection_system": {
        "points_based": False,
        "requirements_based": True,
        "endorsement_required": True
    }
}

# Rural and Northern Immigration Pilot
rnip_program = {
    "program_name": "Rural and Northern Immigration Pilot (RNIP)",
    "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/rural-northern-immigration-pilot.html ",
    "last_updated": "2020-10",
    "federal_or_provincial": "federal",
    "province": "Participating communities in ON, MB, SK, AB, BC",
    "participating_communities": [
        "North Bay, ON", "Sudbury, ON", "Timmins, ON", "Sault Ste. Marie, ON", "Thunder Bay, ON",
        "Brandon, MB", "Altona/Rhineland, MB", "Moose Jaw, SK", "Claresholm, AB",
        "Vernon, BC", "West Kootenay (Trail, Castlegar, Rossland, Nelson), BC"
    ],
    "eligibility_rules": {
        "work_experience": {
            "min_years": 1.0,
            "min_hours": 1560,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3", "TEER 4", "TEER 5"],
            "timeframe": "Within last 3 years",
            "canadian_experience_required": False,
            "full_time_equivalent": "30 hrs/week for 12 months",
            "exemption": "Graduates from post-secondary in recommending community"
        },
        "education": {
            "min_level": "High school diploma or post-secondary certificate/degree",
            "eca_required": True,
            "eca_validity": "5 years",
            "canadian_education_exemption": True
        },
        "language": {
            "english_min": "Varies by NOC TEER",
            "TEER_0_1": "CLB/NCLC 6",
            "TEER_2_3": "CLB/NCLC 5",
            "TEER_4_5": "CLB/NCLC 4",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must demonstrate sufficient funds to support transition to community"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "community_recommendation_required": True,
            "intent_to_reside": "Must intend to live in the recommending community",
            "community_specific_requirements": True
        }
    },
    "selection_system": {
        "points_based": False,
        "community_driven": True,
        "recommendation_based": True
    }
}

# Agri-Food Pilot
agrifood_program = {
    "program_name": "Agri-Food Pilot",
    "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/agri-food-pilot.html ",
    "last_updated": "2020-10",
    "federal_or_provincial": "federal",
    "province": "All provinces except Quebec",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 1.0,
            "min_months": 12,
            "timeframe": "Within last 3 years",
            "location": "In Canada through Temporary Foreign Worker Program",
            "canadian_experience_required": True,
            "full_time_equivalent": "Full-time, non-seasonal",
            "eligible_occupations": ["Farm supervisors", "Butchers", "Food processing labourers", "Harvesting labourers", "General farm workers", "Industrial butchers"]
        },
        "education": {
            "min_level": "High school diploma or post-secondary certificate/degree",
            "eca_required": True,
            "eca_validity": "5 years",
            "eca_exemption": "Canadian education",
            "note_applicants_in_canada": "Can meet EITHER job offer OR education requirement (not both)"
        },
        "language": {
            "english_min": "CLB 4",
            "french_min": "NCLC 4",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "table_cad": {
                1: 15263,
                2: 19001,
                3: 23360,
                4: 28362,
                5: 32168,
                6: 36280,
                7: 40392,
                "additional_per_person": 4112
            }
        },
        "connection_requirements": {
            "job_offer_required": "Full-time, non-seasonal, indeterminate period",
            "wage_requirement": "At or above prevailing wage for occupation and province",
            "eligible_industries": ["Meat product manufacturing (NAICS 3116)", "Greenhouse/nursery (NAICS 1114)", "Animal production (NAICS 1121-1129)"],
            "note_applicants_in_canada": "Can choose to meet job offer OR education requirement"
        }
    },
    "occupation_in_demand": {
        "list_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/agri-food-pilot/eligible-industries.html ",
        "noc_codes": ["80020", "82030", "85100", "85101", "94141", "95106"],
        "industries": ["Meat product manufacturing", "Greenhouse and nursery production", "Animal production (excluding aquaculture)"]
    },
    "selection_system": {
        "points_based": False,
        "requirements_based": True
    }
}

# Start-Up Visa
startup_program = {
    "program_name": "Start-Up Visa Program",
    "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/start-visa.html ",
    "last_updated": "2024-01",
    "federal_or_provincial": "federal",
    "province": "All provinces except Quebec",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "note": "No work experience requirement"
        },
        "education": {
            "min_level": "Not required",
            "eca_required": False,
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 5 in all abilities (listening, reading, writing, speaking)",
            "french_min": "NCLC 5 in all abilities",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must show sufficient funds to settle and live before business generates income",
            "table_cad": {
                1: 15263,
                2: 19001,
                3: 23360,
                4: 28362,
                5: 32168,
                6: 36280,
                7: 40392,
                "additional_per_person": 4112
            }
        },
        "connection_requirements": {
            "letter_of_support_required": True,
            "designated_organization": "Must receive letter from designated venture capital fund, angel investor, or business incubator",
            "minimum_investment": {
                "venture_capital_fund": 200000,
                "angel_investor_group": 75000,
                "business_incubator": 0
            },
            "ownership_requirement": "Each applicant must hold 10% or more voting rights",
            "majority_ownership": "Applicants + designated organization must hold >50% voting rights"
        }
    },
    "business_requirements": {
        "incorporation": "Must be incorporated in Canada",
        "management": "Active and ongoing management from inside Canada",
        "operations": "Essential part of business operations in Canada"
    },
    "selection_system": {
        "points_based": False,
        "requirements_based": True,
        "designated_organization_assessment": True
    }
}

# Home Care Worker Immigration Pilots
caregiver_program = {
    "program_name": "Home Care Worker Immigration Pilots (Child Care & Home Support)",
    "official_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/caregivers/home-care-worker-immigration-pilots.html ",
    "last_updated": "2025-03",
    "federal_or_provincial": "federal",
    "province": "All provinces except Quebec",
    "status": "Workers in Canada stream open; Applicants not in Canada stream closed",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 0.5,
            "min_months": 6,
            "note": "Reduced from 24 months to 6 months as of June 2024",
            "timeframe": "Within or outside Canada, no earlier than 3 years before PR application",
            "noc_codes": ["44100 - Home child care provider", "44101 - Home support worker"],
            "location": "Private home (not institutional setting)",
            "full_time_equivalent": "Full-time work",
            "canadian_experience_required": False
        },
        "education": {
            "min_level": "Canadian 1-year post-secondary OR foreign equivalent",
            "eca_required": True,
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 5",
            "french_min": "NCLC 5",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must demonstrate sufficient funds"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time job in home child care or home support",
            "employer_types": ["Private households", "Organizations that employ homecare workers full-time"]
        }
    },
    "selection_system": {
        "points_based": False,
        "requirements_based": True,
        "cap": "2,750 principal applicants per pilot annually (5,500 total)"
    }
}

# Add more federal programs
immigration_data["programs"].extend([aip_program, rnip_program, agrifood_program, startup_program, caregiver_program])

print(f"Added federal pilot programs. Total programs: {len(immigration_data['programs'])}")



# Add Provincial Nominee Programs - Ontario

# Ontario OINP - Employer Job Offer Foreign Worker
oinp_foreign_worker = {
    "program_name": "Ontario Immigrant Nominee Program – Employer Job Offer: Foreign Worker Stream",
    "official_url": "http://www.ontario.ca/page/oinp-employer-job-offer-streams",
    "last_updated": "2025-07",
    "federal_or_provincial": "provincial",
    "province": "Ontario",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 2.0,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3"],
            "timeframe": "Within last 5 years",
            "canadian_experience_required": False,
            "full_time_equivalent": "Full-time, 30+ hours per week"
        },
        "education": {
            "min_level": "Varies by occupation",
            "eca_required": True,
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 5 for TEER 0,1; CLB 4 for TEER 2,3",
            "french_min": "NCLC 5 for TEER 0,1; NCLC 4 for TEER 2,3",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": False,
            "note": "Not explicitly required for OINP"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, permanent, in Ontario",
            "wage_requirement": "At or above median wage for occupation in Ontario",
            "employer_requirements": {
                "business_duration": "At least 3 years",
                "revenue_GTA": 1000000,
                "revenue_outside_GTA": 500000,
                "employees_GTA": 5,
                "employees_outside_GTA": 3
            }
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "invitation_to_apply_required": True,
        "scoring_factors": ["Education", "Job offer NOC", "Wage", "Canadian work experience", "Regional location", "Field of study"]
    }
}

# Ontario OINP - Masters Graduate
oinp_masters = {
    "program_name": "Ontario Immigrant Nominee Program – Masters Graduate Stream",
    "official_url": "http://www.ontario.ca/page/ontario-immigrant-nominee-program-streams",
    "last_updated": "2025-07",
    "federal_or_provincial": "provincial",
    "province": "Ontario",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "note": "No work experience required"
        },
        "education": {
            "min_level": "Masters degree from eligible Ontario university",
            "eca_required": False,
            "completion_timeframe": "Within 2 years of application",
            "program_duration": "At least 1 academic year",
            "study_status": "Must have been in good standing",
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 7",
            "french_min": "NCLC 7",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must demonstrate sufficient funds"
        },
        "connection_requirements": {
            "job_offer_required": False,
            "residence_requirement": "Must have lived in Ontario for at least 12 of last 24 months",
            "legal_status_required": True
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "invitation_to_apply_required": True
    }
}

# Ontario OINP - PhD Graduate
oinp_phd = {
    "program_name": "Ontario Immigrant Nominee Program – PhD Graduate Stream",
    "official_url": "http://www.ontario.ca/page/ontario-immigrant-nominee-program-streams",
    "last_updated": "2025-07",
    "federal_or_provincial": "provincial",
    "province": "Ontario",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "note": "No work experience required"
        },
        "education": {
            "min_level": "PhD from eligible Ontario university",
            "eca_required": False,
            "completion_timeframe": "Within 2 years of application",
            "program_duration": "At least 2 years",
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 7",
            "french_min": "NCLC 7",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must demonstrate sufficient funds"
        },
        "connection_requirements": {
            "job_offer_required": False,
            "residence_requirement": "Must have lived in Ontario for at least 12 of last 24 months",
            "legal_status_required": True
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "invitation_to_apply_required": True
    }
}

# Ontario OINP - In-Demand Skills
oinp_in_demand = {
    "program_name": "Ontario Immigrant Nominee Program – Employer Job Offer: In-Demand Skills Stream",
    "official_url": "http://www.ontario.ca/page/oinp-employer-job-offer-demand-skills-stream",
    "last_updated": "2025-07",
    "federal_or_provincial": "provincial",
    "province": "Ontario",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "min_months": 9,
            "note": "9 months cumulative work experience in Ontario in last 3 years",
            "noc_types": ["TEER 4", "TEER 5"],
            "eligible_occupations": ["Agriculture", "Construction", "Truck driving", "Food processing", "Manufacturing", "Personal support"],
            "canadian_experience_required": True,
            "location": "Ontario"
        },
        "education": {
            "min_level": "Canadian high school diploma OR foreign equivalent with ECA",
            "eca_required": True
        },
        "language": {
            "english_min": "CLB 4",
            "french_min": "NCLC 4",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": False
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, permanent, in Ontario",
            "job_offer_noc": "TEER 4 or 5",
            "employer_requirements": {
                "business_duration": "At least 3 years",
                "revenue_GTA": 1000000,
                "revenue_outside_GTA": 500000
            }
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "invitation_to_apply_required": True
    }
}

# Add Ontario programs
immigration_data["programs"].extend([oinp_foreign_worker, oinp_masters, oinp_phd, oinp_in_demand])

print(f"Added Ontario PNP programs. Total programs: {len(immigration_data['programs'])}")


# Add Provincial Nominee Programs - Ontario

# Ontario OINP - Employer Job Offer Foreign Worker
oinp_foreign_worker = {
    "program_name": "Ontario Immigrant Nominee Program – Employer Job Offer: Foreign Worker Stream",
    "official_url": "http://www.ontario.ca/page/oinp-employer-job-offer-streams",
    "last_updated": "2025-07",
    "federal_or_provincial": "provincial",
    "province": "Ontario",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 2.0,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3"],
            "timeframe": "Within last 5 years",
            "canadian_experience_required": False,
            "full_time_equivalent": "Full-time, 30+ hours per week"
        },
        "education": {
            "min_level": "Varies by occupation",
            "eca_required": True,
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 5 for TEER 0,1; CLB 4 for TEER 2,3",
            "french_min": "NCLC 5 for TEER 0,1; NCLC 4 for TEER 2,3",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": False,
            "note": "Not explicitly required for OINP"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, permanent, in Ontario",
            "wage_requirement": "At or above median wage for occupation in Ontario",
            "employer_requirements": {
                "business_duration": "At least 3 years",
                "revenue_GTA": 1000000,
                "revenue_outside_GTA": 500000,
                "employees_GTA": 5,
                "employees_outside_GTA": 3
            }
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "invitation_to_apply_required": True,
        "scoring_factors": ["Education", "Job offer NOC", "Wage", "Canadian work experience", "Regional location", "Field of study"]
    }
}

# Ontario OINP - Masters Graduate
oinp_masters = {
    "program_name": "Ontario Immigrant Nominee Program – Masters Graduate Stream",
    "official_url": "http://www.ontario.ca/page/ontario-immigrant-nominee-program-streams",
    "last_updated": "2025-07",
    "federal_or_provincial": "provincial",
    "province": "Ontario",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "note": "No work experience required"
        },
        "education": {
            "min_level": "Masters degree from eligible Ontario university",
            "eca_required": False,
            "completion_timeframe": "Within 2 years of application",
            "program_duration": "At least 1 academic year",
            "study_status": "Must have been in good standing",
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 7",
            "french_min": "NCLC 7",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must demonstrate sufficient funds"
        },
        "connection_requirements": {
            "job_offer_required": False,
            "residence_requirement": "Must have lived in Ontario for at least 12 of last 24 months",
            "legal_status_required": True
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "invitation_to_apply_required": True
    }
}

# Ontario OINP - PhD Graduate
oinp_phd = {
    "program_name": "Ontario Immigrant Nominee Program – PhD Graduate Stream",
    "official_url": "http://www.ontario.ca/page/ontario-immigrant-nominee-program-streams",
    "last_updated": "2025-07",
    "federal_or_provincial": "provincial",
    "province": "Ontario",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "note": "No work experience required"
        },
        "education": {
            "min_level": "PhD from eligible Ontario university",
            "eca_required": False,
            "completion_timeframe": "Within 2 years of application",
            "program_duration": "At least 2 years",
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 7",
            "french_min": "NCLC 7",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must demonstrate sufficient funds"
        },
        "connection_requirements": {
            "job_offer_required": False,
            "residence_requirement": "Must have lived in Ontario for at least 12 of last 24 months",
            "legal_status_required": True
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "invitation_to_apply_required": True
    }
}

# Ontario OINP - In-Demand Skills
oinp_in_demand = {
    "program_name": "Ontario Immigrant Nominee Program – Employer Job Offer: In-Demand Skills Stream",
    "official_url": "http://www.ontario.ca/page/oinp-employer-job-offer-demand-skills-stream",
    "last_updated": "2025-07",
    "federal_or_provincial": "provincial",
    "province": "Ontario",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "min_months": 9,
            "note": "9 months cumulative work experience in Ontario in last 3 years",
            "noc_types": ["TEER 4", "TEER 5"],
            "eligible_occupations": ["Agriculture", "Construction", "Truck driving", "Food processing", "Manufacturing", "Personal support"],
            "canadian_experience_required": True,
            "location": "Ontario"
        },
        "education": {
            "min_level": "Canadian high school diploma OR foreign equivalent with ECA",
            "eca_required": True
        },
        "language": {
            "english_min": "CLB 4",
            "french_min": "NCLC 4",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": False
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, permanent, in Ontario",
            "job_offer_noc": "TEER 4 or 5",
            "employer_requirements": {
                "business_duration": "At least 3 years",
                "revenue_GTA": 1000000,
                "revenue_outside_GTA": 500000
            }
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "invitation_to_apply_required": True
    }
}

# Add Ontario programs
immigration_data["programs"].extend([oinp_foreign_worker, oinp_masters, oinp_phd, oinp_in_demand])

print(f"Added Ontario PNP programs. Total programs: {len(immigration_data['programs'])}")


# Add BC PNP Programs

bc_skilled_worker = {
    "program_name": "BC Provincial Nominee Program – Skills Immigration: Skilled Worker",
    "official_url": "https://www.welcomebc.ca/immigrate-to-b-c/bc-pnp-skills-immigration ",
    "last_updated": "2025-04",
    "federal_or_provincial": "provincial",
    "province": "British Columbia",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 2.0,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3"],
            "timeframe": "Full-time equivalent work experience in last 10 years",
            "canadian_experience_required": False,
            "full_time_equivalent": "30 hours per week"
        },
        "education": {
            "min_level": "Minimum education credential required for occupation",
            "eca_required": True,
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 4",
            "french_min": "NCLC 4",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": False,
            "note": "Must meet minimum income requirements based on family size and residence area"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, indeterminate (no end date)",
            "wage_requirement": "Within wage range for occupation and location (WorkBC/Job Bank)",
            "employer_requirements": {
                "business_duration": "At least 1 year in BC",
                "employees_metro_vancouver": 5,
                "employees_outside_metro": 3
            }
        }
    },
    "selection_system": {
        "points_based": True,
        "registration_required": True,
        "invitation_to_apply_required": True,
        "express_entry_option": True
    },
    "occupation_in_demand": {
        "note": "BC PNP prioritizes workers in healthcare, construction, early childhood education, and in-demand occupations"
    }
}

bc_international_graduate = {
    "program_name": "BC Provincial Nominee Program – Skills Immigration: International Graduate",
    "official_url": "https://www.welcomebc.ca/immigrate-to-b-c/bc-pnp-skills-immigration ",
    "last_updated": "2025-04",
    "federal_or_provincial": "provincial",
    "province": "British Columbia",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "note": "No work experience required, but recommended"
        },
        "education": {
            "min_level": "Degree, diploma or certificate from eligible Canadian post-secondary institution",
            "program_duration": "At least 8 months (two semesters) full-time equivalent",
            "completion_timeframe": "Graduated within last 3 years",
            "eca_required": False,
            "field_restricted": False
        },
        "language": {
            "english_min": "CLB 4",
            "french_min": "NCLC 4",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": False,
            "note": "Must meet minimum wage and income requirements"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, indeterminate",
            "job_offer_noc": "TEER 1, 2, or 3 (TEER 0 not eligible)",
            "wage_requirement": "Within wage range for occupation and location"
        }
    },
    "selection_system": {
        "points_based": True,
        "registration_required": True,
        "invitation_to_apply_required": True,
        "express_entry_option": True
    }
}

bc_entry_level = {
    "program_name": "BC Provincial Nominee Program – Skills Immigration: Entry Level and Semi-Skilled",
    "official_url": "https://www.welcomebc.ca/immigrate-to-b-c/bc-pnp-skills-immigration ",
    "last_updated": "2025-04",
    "federal_or_provincial": "provincial",
    "province": "British Columbia",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "min_months": 9,
            "note": "9 months consecutive full-time work with supporting employer",
            "noc_types": ["TEER 4", "TEER 5"],
            "eligible_sectors": ["Tourism/hospitality", "Food processing"],
            "canadian_experience_required": True,
            "location": "British Columbia"
        },
        "education": {
            "min_level": "High school diploma or higher",
            "eca_required": True
        },
        "language": {
            "english_min": "CLB 4",
            "french_min": "NCLC 4",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": False,
            "note": "Must meet minimum wage and income requirements"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, indeterminate",
            "job_offer_noc": "Eligible TEER 4 or 5 occupations in tourism/hospitality or food processing",
            "wage_requirement": "Within wage range"
        }
    },
    "selection_system": {
        "points_based": True,
        "registration_required": True,
        "invitation_to_apply_required": True,
        "express_entry_option": False
    }
}

# Alberta AAIP
alberta_express_entry = {
    "program_name": "Alberta Advantage Immigration Program – Alberta Express Entry Stream",
    "official_url": "https://www.alberta.ca/aaip-alberta-express-entry-stream-eligibility ",
    "last_updated": "2025-05",
    "federal_or_provincial": "provincial",
    "province": "Alberta",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "note": "Must meet federal Express Entry requirements"
        },
        "education": {
            "min_level": "Must meet federal Express Entry requirements",
            "eca_required": True
        },
        "language": {
            "english_min": "Must meet federal Express Entry requirements",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"]
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must meet federal Express Entry requirements"
        },
        "connection_requirements": {
            "express_entry_profile_required": True,
            "crs_minimum": 300,
            "job_offer_required": "Varies by pathway",
            "alberta_connection_preferred": True,
            "intent_to_reside": "Must intend to live and work in Alberta"
        }
    },
    "selection_system": {
        "points_based": True,
        "invitation_based": True,
        "pathways": ["Dedicated Health Care", "Accelerated Tech", "Law Enforcement", "Priority sectors"]
    }
}

alberta_opportunity = {
    "program_name": "Alberta Advantage Immigration Program – Alberta Opportunity Stream",
    "official_url": "https://www.alberta.ca/aaip-alberta-opportunity-stream-eligibility ",
    "last_updated": "2025-08",
    "federal_or_provincial": "provincial",
    "province": "Alberta",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "option_1": "12 months full-time in Alberta within last 18 months",
            "option_2": "24 months full-time in Canada/abroad within last 30 months",
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3", "TEER 4", "TEER 5"],
            "canadian_experience_required": "Option 1 requires Alberta experience",
            "full_time_equivalent": "30 hours per week",
            "PGWP_exception": "6 months in Alberta within last 18 months"
        },
        "education": {
            "min_level": "High school diploma or higher",
            "eca_required": True
        },
        "language": {
            "english_min": "CLB 4 minimum (CLB 5 for TEER 2,3; CLB 7 for TEER 0,1)",
            "french_min": "NCLC 4 minimum",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": False
        },
        "connection_requirements": {
            "job_offer_required": True,
            "current_employment": "Must be working in occupation at time of application",
            "work_permit_required": True,
            "licensing_required": "If occupation is regulated in Alberta"
        }
    },
    "selection_system": {
        "points_based": False,
        "requirements_based": True
    }
}

# Add BC and Alberta programs
immigration_data["programs"].extend([bc_skilled_worker, bc_international_graduate, bc_entry_level, alberta_express_entry, alberta_opportunity])

print(f"Added BC and Alberta PNP programs. Total programs: {len(immigration_data['programs'])}")




# Add Atlantic provinces PNPs

# New Brunswick
nb_skilled_worker = {
    "program_name": "New Brunswick Provincial Nominee Program – Skilled Worker Stream",
    "official_url": "https://www2.gnb.ca/content/gnb/en/corporate/promo/immigration/immigrating-to-nb/nb-skilled-worker-stream.html ",
    "last_updated": "2023-10",
    "federal_or_provincial": "provincial",
    "province": "New Brunswick",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 1.0,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3"],
            "timeframe": "Within last 5 years",
            "canadian_experience_required": False,
            "full_time_equivalent": "30 hours per week, 1,560 hours per year"
        },
        "education": {
            "min_level": "High school diploma or higher",
            "eca_required": True
        },
        "language": {
            "english_min": "CLB 7 for TEER 0,1; CLB 5 for TEER 2,3",
            "french_min": "NCLC 7 for TEER 0,1; NCLC 5 for TEER 2,3",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "2 years"
        },
        "age": {
            "min_age": 19,
            "max_age": 55
        },
        "settlement_funds": {
            "required": True,
            "note": "Must demonstrate sufficient funds"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, non-seasonal, at least 30 hours per week",
            "employer_support_required": True
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "pass_mark": 65
    }
}

# Nova Scotia
ns_skilled_worker = {
    "program_name": "Nova Scotia Nominee Program – Skilled Worker Stream",
    "official_url": "http://novascotiaimmigration.ca",
    "last_updated": "2025-10",
    "federal_or_provincial": "provincial",
    "province": "Nova Scotia",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 1.0,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3"],
            "canadian_experience_required": False
        },
        "education": {
            "min_level": "High school diploma or higher",
            "eca_required": True
        },
        "language": {
            "english_min": "CLB 5",
            "french_min": "NCLC 5",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"]
        },
        "age": {
            "min_age": 21,
            "max_age": 55
        },
        "settlement_funds": {
            "required": True
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, permanent",
            "employer_requirements": "Nova Scotia employer"
        }
    },
    "selection_system": {
        "points_based": True,
        "invitation_required": True
    }
}

# Newfoundland and Labrador
nl_skilled_worker = {
    "program_name": "Newfoundland and Labrador Provincial Nominee Program – Skilled Worker Category",
    "official_url": "https://www.gov.nl.ca/immigration/immigrating-to-newfoundland-and-labrador/provincial-nominee-program/applicants/skilled-worker/ ",
    "last_updated": "2025-02",
    "federal_or_provincial": "provincial",
    "province": "Newfoundland and Labrador",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "note": "Work experience requirements vary by occupation"
        },
        "education": {
            "min_level": "Required for occupation",
            "eca_required": True
        },
        "language": {
            "english_min": "Required for TEER 4,5 (test results mandatory)",
            "french_min": "Alternative to English",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "test_validity": "Must be valid throughout application process"
        },
        "age": {
            "min_age": 21,
            "max_age": 59
        },
        "settlement_funds": {
            "required": True,
            "note": "Must demonstrate ability to economically establish"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, minimum 30 hours per week, at least 1 year duration",
            "job_offer_noc": "TEER 0, 1, 2, 3, 4, or 5",
            "wage_requirement": "Regional, provincial, or national prevailing wage",
            "employer_requirements": "Eligible NL employer, valid JVA if no work permit"
        }
    },
    "selection_system": {
        "points_based": False,
        "expression_of_interest": True,
        "invitation_required": True
    }
}

nl_express_entry = {
    "program_name": "Newfoundland and Labrador Provincial Nominee Program – Express Entry Skilled Worker",
    "official_url": "https://www.gov.nl.ca/immigration/immigrating-to-newfoundland-and-labrador/provincial-nominee-program/applicants/express-entry-skilled-worker/ ",
    "last_updated": "2025-02",
    "federal_or_provincial": "provincial",
    "province": "Newfoundland and Labrador",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "note": "Must meet federal Express Entry requirements"
        },
        "education": {
            "min_level": "Canadian post-secondary degree/diploma OR valid ECA",
            "eca_required": True
        },
        "language": {
            "english_min": "Must meet federal Express Entry requirements",
            "french_min": "Must meet federal Express Entry requirements",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"]
        },
        "age": {
            "min_age": 21,
            "max_age": 59
        },
        "settlement_funds": {
            "required": True
        },
        "connection_requirements": {
            "express_entry_profile_required": True,
            "job_offer_required": True,
            "job_offer_noc": "TEER 0, 1, 2, or 3",
            "job_offer_duration": "At least 1 year"
        }
    },
    "selection_system": {
        "points_based": False,
        "expression_of_interest": True,
        "invitation_required": True
    }
}

# PEI
pei_skilled_worker = {
    "program_name": "Prince Edward Island Provincial Nominee Program – Labour Impact: Skilled Worker Stream",
    "official_url": "https://www.princeedwardisland.ca/en/information/office-immigration ",
    "last_updated": "2025-10",
    "federal_or_provincial": "provincial",
    "province": "Prince Edward Island",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 2.0,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3"],
            "canadian_experience_required": False
        },
        "education": {
            "min_level": "Post-secondary degree or diploma",
            "eca_required": True
        },
        "language": {
            "english_min": "CLB 4",
            "french_min": "NCLC 4",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"]
        },
        "age": {
            "min_age": 21,
            "max_age": 59
        },
        "settlement_funds": {
            "required": True
        },
        "connection_requirements": {
            "job_offer_required": True,
            "job_offer_type": "Full-time, permanent or at least 2 years",
            "employer_requirements": "PEI employer"
        }
    },
    "selection_system": {
        "points_based": True,
        "total_points_possible": 100,
        "expression_of_interest": True,
        "invitation_required": True
    }
}

# Add Atlantic provinces
immigration_data["programs"].extend([nb_skilled_worker, ns_skilled_worker, nl_skilled_worker, nl_express_entry, pei_skilled_worker])

print(f"Added Atlantic provinces PNP programs. Total programs: {len(immigration_data['programs'])}")


# Add Quebec and remaining programs

# Quebec Skilled Worker
quebec_skilled_worker = {
    "program_name": "Quebec Skilled Worker Selection Program (SWSP) - Stream 1: Highly Qualified and Specialized Skills",
    "official_url": "https://www.immigration-quebec.gouv.qc.ca ",
    "last_updated": "2024-11",
    "federal_or_provincial": "quebec",
    "province": "Quebec",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 1.0,
            "noc_types": ["FEER 0", "FEER 1", "FEER 2"],
            "timeframe": "Within last 5 years",
            "canadian_experience_required": False,
            "note": "For non-regulated occupations"
        },
        "education": {
            "min_level": "Minimum 1 year full-time study (DEP, AEC, DEC, certificate, bachelor's, master's, or PhD)",
            "eca_required": "Not required but can be submitted",
            "equivalent_hours": "900 hours at secondary/college or 30 credits at university"
        },
        "language": {
            "french_min": "Oral French: Level 7 or higher; Written French: Level 5 or higher (Échelle québécoise)",
            "french_mandatory": True,
            "english_accepted": True,
            "accepted_tests": ["TEF Canada", "TCF Canada", "DELF", "IELTS", "CELPIP"],
            "note": "French proficiency is mandatory as of November 2023"
        },
        "age": {
            "min_age": 18,
            "max_age": None,
            "optimal_range": "18-35 years for maximum points"
        },
        "settlement_funds": {
            "required": True,
            "note": "Must sign Financial Self-Sufficiency Contract (3 months support)",
            "capacity_for_autonomy": "Eliminatory factor"
        },
        "connection_requirements": {
            "job_offer_required": False,
            "valid_job_offer_bonus": "14 points",
            "quebec_connection_points": 8,
            "intent_to_reside": "Must intend to settle in Quebec"
        }
    },
    "selection_system": {
        "points_based": True,
        "total_points_possible": "Varies by stream",
        "pass_mark_single": 50,
        "pass_mark_with_spouse": 59,
        "employability_score_single": 43,
        "employability_score_with_spouse": 52,
        "points_breakdown": {
            "education": {"max": 26},
            "work_experience": {"max": 8},
            "age": {"max": 16},
            "language_proficiency": {"max": 22},
            "connection_to_quebec": {"max": 8},
            "spouse_factors": {"max": 17},
            "valid_job_offer": {"max": 14},
            "children": {"max": 8}
        },
        "arrima_system": True,
        "expression_of_interest": True
    },
    "additional_requirements": {
        "values_attestation": "Must obtain Attestation of learning of democratic and Quebec values",
        "prohibited_employment_sectors": ["Payday loans", "Cheque cashing", "Pawnbroking", "Pornographic/sex industry"],
        "self_employment_restriction": "Cannot control company directly or indirectly"
    }
}

# Saskatchewan SINP
saskatchewan_express_entry = {
    "program_name": "Saskatchewan Immigrant Nominee Program – International Skilled Worker: Saskatchewan Express Entry",
    "official_url": "https://www.saskatchewan.ca/residents/moving-to-saskatchewan/live-in-saskatchewan/by-immigrating/saskatchewan-immigrant-nominee-program ",
    "last_updated": "2025-03",
    "federal_or_provincial": "provincial",
    "province": "Saskatchewan",
    "eligibility_rules": {
        "work_experience": {
            "min_years": 1.0,
            "noc_types": ["TEER 0", "TEER 1", "TEER 2", "TEER 3"],
            "canadian_experience_required": False,
            "note": "Must meet federal Express Entry requirements"
        },
        "education": {
            "min_level": "Must meet federal Express Entry requirements",
            "eca_required": True
        },
        "language": {
            "english_min": "CLB 4 minimum",
            "french_min": "NCLC 4 minimum",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"],
            "note": "Must meet federal Express Entry requirements"
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must meet federal Express Entry requirements"
        },
        "connection_requirements": {
            "express_entry_profile_required": True,
            "saskatchewan_connection_required": True,
            "connection_options": ["Work experience in Saskatchewan", "Study in Saskatchewan", "Family in Saskatchewan", "Job offer"]
        }
    },
    "selection_system": {
        "points_based": True,
        "total_points_possible": 100,
        "pass_mark": 60,
        "invitation_required": True
    }
}

# Manitoba MPNP
manitoba_skilled_worker = {
    "program_name": "Manitoba Provincial Nominee Program – Skilled Worker in Manitoba Stream",
    "official_url": "https://www.gov.mb.ca/mbsupportsukraine/immigration.html ",
    "last_updated": "2025-10",
    "federal_or_provincial": "provincial",
    "province": "Manitoba",
    "eligibility_rules": {
        "work_experience": {
            "min_years": None,
            "min_months": 6,
            "note": "6 months full-time work for current Manitoba employer",
            "canadian_experience_required": True,
            "location": "Manitoba"
        },
        "education": {
            "min_level": "Varies by occupation",
            "eca_required": True
        },
        "language": {
            "english_min": "CLB 4 minimum (CLB 5-6 for regulated occupations)",
            "french_min": "NCLC 4 minimum",
            "accepted_tests": ["IELTS", "CELPIP", "TEF Canada", "TCF Canada"]
        },
        "age": {
            "min_age": 18,
            "max_age": None
        },
        "settlement_funds": {
            "required": True,
            "note": "Must demonstrate settlement funds"
        },
        "connection_requirements": {
            "job_offer_required": True,
            "current_employment": "Must be working for Manitoba employer",
            "work_permit_required": True,
            "intent_to_reside": "Must intend to live and work in Manitoba"
        }
    },
    "selection_system": {
        "points_based": True,
        "expression_of_interest": True,
        "invitation_required": True
    }
}

import json

# Add Quebec, Saskatchewan, Manitoba
immigration_data["programs"].extend([quebec_skilled_worker, saskatchewan_express_entry, manitoba_skilled_worker])

# Create summary statistics
total_programs = len(immigration_data["programs"])
federal_count = sum(1 for p in immigration_data["programs"] if p["federal_or_provincial"] == "federal")
provincial_count = sum(1 for p in immigration_data["programs"] if p["federal_or_provincial"] == "provincial")
quebec_count = sum(1 for p in immigration_data["programs"] if p["federal_or_provincial"] == "quebec")

print(f"\n=== IMMIGRATION PROGRAMS EXTRACTION SUMMARY ===")
print(f"Total programs extracted: {total_programs}")
print(f"Federal programs: {federal_count}")
print(f"Provincial programs: {provincial_count}")
print(f"Quebec programs: {quebec_count}")
print(f"\nPrograms list:")
for i, prog in enumerate(immigration_data["programs"], 1):
    print(f"{i}. {prog['program_name']} ({prog['federal_or_provincial']})")

# Convert to JSON format and save
json_output = json.dumps(immigration_data, indent=2, ensure_ascii=False)

# Save to file
with open('canadian_immigration_programs.json', 'w', encoding='utf-8') as f:
    f.write(json_output)

# Also create a summary version with key metadata
verification_summary = {
    "Extraction Date": immigration_data['metadata']['extraction_date'],
    "Total Programs": len(immigration_data['programs']),
    "Federal Programs": federal_count,
    "Provincial Programs": provincial_count,
    "Quebec Programs": quebec_count,
    "Programs List": [
        {"index": i + 1, "program_name": prog['program_name'], "type": prog['federal_or_provincial']}
        for i, prog in enumerate(immigration_data["programs"])
    ]
}

print("\nJSON file created successfully!")
print(f"\nFile size: {len(json_output)} characters")
print(f"\n=== SAMPLE OUTPUT (First 2000 characters) ===\n")
print(json_output[:2000])
print("\n... [truncated for display] ...")

print("\nVerification summary:", verification_summary)

# Write summary to file
with open('extraction_summary.json', 'w', encoding='utf-8') as f:
    json.dump(verification_summary, f, indent=2, ensure_ascii=False)

print("\n✓ JSON file saved: canadian_immigration_programs.json")
print("✓ Summary file saved: extraction_summary.json")
