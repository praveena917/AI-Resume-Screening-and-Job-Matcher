from src.semantic_matcher import calculate_similarity


resume_text = """
I have experience in Python, SQL, Power BI,
Pandas, NumPy and data analysis.
I have worked on machine learning projects
and created data visualization dashboards.
"""


job_description = """
We are looking for a Data Analyst with experience
in Python, SQL, business intelligence, data analysis,
machine learning and dashboard development.
"""


score = calculate_similarity(
    resume_text,
    job_description
)

print(f"Semantic Similarity Score: {score:.2f}%")