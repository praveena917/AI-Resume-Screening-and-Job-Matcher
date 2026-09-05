import pymupdf

from src.skill_extractor import extract_skills
from src.semantic_matcher import calculate_similarity
from src.matcher import calculate_final_score

from src.resume_parser import (
    extract_name,
    extract_email,
    extract_phone
)

from src.section_extractor import extract_sections

from src.job_analyzer import (
    extract_required_skills,
    extract_preferred_skills
)

from src.recommendation import get_recommendation
from src.capability_analyzer import (
    extract_job_capabilities,
    find_capability_matches
)


# ============================================================
# 1. EXTRACT RESUME TEXT
# ============================================================

def extract_resume_text(pdf_path):

    doc = pymupdf.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


# ============================================================
# 2. READ JOB DESCRIPTION
# ============================================================

def read_job_description(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# ============================================================
# 3. LOAD RESUME + JOB DESCRIPTION
# ============================================================

pdf_path = "Resumes/Praveena_Resume.pdf"

resume_text = extract_resume_text(pdf_path)

job_description = read_job_description(
    "job_description.txt"
)


# ============================================================
# 4. EXTRACT CANDIDATE INFORMATION
# ============================================================

candidate_name = extract_name(resume_text)

candidate_email = extract_email(resume_text)

candidate_phone = extract_phone(resume_text)

sections = extract_sections(resume_text)


# ============================================================
# 5. EXTRACT RESUME SKILLS
# ============================================================

resume_skills = extract_skills(
    resume_text
)


# ============================================================
# 6. EXTRACT REQUIRED + PREFERRED JOB SKILLS
# ============================================================

required_skills = extract_required_skills(
    job_description
)

preferred_skills = extract_preferred_skills(
    job_description
)


# ============================================================
# 7. CREATE JOB SKILL SET
# ============================================================

job_skills = list(
    dict.fromkeys(
        required_skills + preferred_skills
    )
)


# ============================================================
# 8. CREATE RESUME SKILL SET
# ============================================================

resume_skill_set = set(
    resume_skills
)


# ============================================================
# 9. MATCH REQUIRED SKILLS
# ============================================================

required_matched = [

    skill

    for skill in required_skills

    if skill in resume_skill_set

]


required_missing = [

    skill

    for skill in required_skills

    if skill not in resume_skill_set

]


# ============================================================
# 10. MATCH PREFERRED SKILLS
# ============================================================

preferred_matched = [

    skill

    for skill in preferred_skills

    if skill in resume_skill_set

]


preferred_missing = [

    skill

    for skill in preferred_skills

    if skill not in resume_skill_set

]


# ============================================================
# 11. MATCH ALL JOB SKILLS
# ============================================================

matched_skills = [

    skill

    for skill in resume_skills

    if skill in job_skills

]


missing_skills = [

    skill

    for skill in job_skills

    if skill not in resume_skill_set

]


# ============================================================
# 12. REQUIRED SKILL SCORE
# ============================================================

if len(required_skills) > 0:

    required_skill_match = (

        len(required_matched)
        / len(required_skills)

    ) * 100

else:

    required_skill_match = 0


# ============================================================
# 13. PREFERRED SKILL SCORE
# ============================================================

if len(preferred_skills) > 0:

    preferred_skill_match = (

        len(preferred_matched)
        / len(preferred_skills)

    ) * 100

else:

    preferred_skill_match = 0


# ============================================================
# 13b. JOB CAPABILITIES + CAPABILITY SCORE
# ============================================================

job_capabilities = extract_job_capabilities(
    job_description
)

capability_matched, capability_missing = find_capability_matches(
    resume_text,
    job_capabilities
)

if len(job_capabilities) > 0:

    capability_match = (

        len(capability_matched)
        / len(job_capabilities)

    ) * 100

else:

    capability_match = 0


# ============================================================
# 14. SEMANTIC MATCH
# ============================================================

semantic_match = calculate_similarity(

    resume_text,

    job_description

)


# ============================================================
# 15. FINAL AI SCORE
# ============================================================

final_score = calculate_final_score(

    required_skill_match,

    preferred_skill_match,

    capability_match,

    semantic_match,

    has_required_skills=bool(required_skills),

    has_preferred_skills=bool(preferred_skills),

    has_capabilities=bool(job_capabilities)

)


# ============================================================
# 16. AI RECOMMENDATION
# ============================================================

recommendation = get_recommendation(

    final_score

)


# ============================================================
# 17. DISPLAY RESULTS
# ============================================================

print("\n==============================")

print("   AI RESUME JOB MATCHER")

print("==============================")


# ------------------------------------------------------------
# Candidate information
# ------------------------------------------------------------

print("\n===== CANDIDATE INFORMATION =====")

print("Name:", candidate_name)

print("Email:", candidate_email)

print("Phone:", candidate_phone)


# ------------------------------------------------------------
# Resume sections
# ------------------------------------------------------------

print("\n===== RESUME SECTIONS =====")

for section, content in sections.items():

    print(f"\n--- {section.upper()} ---")

    print(content.strip())


# ------------------------------------------------------------
# Resume skills
# ------------------------------------------------------------

print("\n===== RESUME SKILLS =====")

for skill in resume_skills:

    print("✓", skill)


# ------------------------------------------------------------
# Required skills
# ------------------------------------------------------------

print("\n===== JOB REQUIRED SKILLS =====")

for skill in required_skills:

    print("✓", skill)


# ------------------------------------------------------------
# Preferred skills
# ------------------------------------------------------------

print("\n===== JOB PREFERRED SKILLS =====")

for skill in preferred_skills:

    print("✓", skill)


# ------------------------------------------------------------
# Matched skills
# ------------------------------------------------------------

print("\n===== MATCHED SKILLS =====")

for skill in matched_skills:

    print("✓", skill)


# ------------------------------------------------------------
# Missing skills
# ------------------------------------------------------------

print("\n===== MISSING SKILLS =====")

for skill in missing_skills:

    print("✗", skill)


# ------------------------------------------------------------
# Required skill matching
# ------------------------------------------------------------

print("\n===== REQUIRED SKILL MATCH =====")

for skill in required_matched:

    print("✓", skill)


for skill in required_missing:

    print("✗", skill)


# ------------------------------------------------------------
# Preferred skill matching
# ------------------------------------------------------------

print("\n===== PREFERRED SKILL MATCH =====")

for skill in preferred_matched:

    print("✓", skill)


for skill in preferred_missing:

    print("✗", skill)


# ------------------------------------------------------------
# Capability matching
# ------------------------------------------------------------

print("\n===== CAPABILITY MATCH =====")

for capability in capability_matched:

    print("✓", capability)

for capability in capability_missing:

    print("✗", capability)


# ============================================================
# 18. SCORE BREAKDOWN
# ============================================================

print("\n===== SCORE BREAKDOWN =====")

print(
    f"Required Skills:      "
    f"{required_skill_match:.2f}%"
)

print(
    f"Preferred Skills:     "
    f"{preferred_skill_match:.2f}%"
)

print(
    f"Job Capabilities:     "
    f"{capability_match:.2f}%"
    if job_capabilities
    else "Job Capabilities:      N/A (none detected)"
)

print(
    f"Semantic Similarity:  "
    f"{semantic_match:.2f}%"
)


# ============================================================
# 19. FINAL SCORE
# ============================================================

print("\n==============================")

print(
    f"FINAL AI MATCH SCORE: "
    f"{final_score:.2f}%"
)

print("==============================")


# ============================================================
# 20. AI RECOMMENDATION
# ============================================================

print("\n===== AI RECOMMENDATION =====")

print(
    "Recommendation:",
    recommendation
)