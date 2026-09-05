from src.job_analyzer import (
    extract_required_skills,
    extract_preferred_skills
)


job_description = """
Data Analyst

Requirements:
Python
SQL
Power BI
Pandas
NumPy

Preferred:
Machine Learning
Tableau
AWS
"""


required = extract_required_skills(
    job_description
)

preferred = extract_preferred_skills(
    job_description
)


print("\n===== REQUIRED SKILLS =====")

for skill in required:
    print("✓", skill)


print("\n===== PREFERRED SKILLS =====")

for skill in preferred:
    print("✓", skill)