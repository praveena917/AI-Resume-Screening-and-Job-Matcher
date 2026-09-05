import re


SKILLS = [
    # Programming
    "Python",
    "Java",
    "C",
    "JavaScript",

    # Data Analysis
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",

    # SQL / Databases
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "CTE",
    "CTEs",
    "Window Functions",
    "SQL Views",
    "Joins",

    # BI
    "Power BI",
    "DAX",
    "Power Query",
    "Excel",
    "Pivot Tables",
    "VLOOKUP",
    "Slicers",
    "Charts",
    "Tableau",

    # AI / ML
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Artificial Intelligence",
    "TensorFlow",
    "PyTorch",

    # Data Concepts
    "Data Analysis",
    "Data Visualization",
    "Data Cleaning",
    "Data Modeling",
    "KPI Reporting",
    "Business Intelligence",

    # Tools
    "Git",
    "GitHub",
    "Jupyter Notebook",
    "VS Code",
    "Docker",

    # Web
    "Flask",
    "FastAPI",
    "React",
    "Node.js",

    # Cloud
    "AWS",
    "Microsoft Azure",
    "Microsoft Fabric"
]


def normalize_text(text):
    """
    Normalize text for skill matching.
    """

    text = text.lower()

    # Normalize apostrophes
    text = text.replace("’", "'")

    # Convert common separators to spaces
    text = re.sub(r"[-_/(),]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):

    normalized_text = normalize_text(text)

    found_skills = []

    for skill in SKILLS:

        normalized_skill = normalize_text(skill)

        # Special handling for single-letter skills
        if len(normalized_skill) == 1:
            pattern = r"(?<![a-zA-Z])" + re.escape(normalized_skill) + r"(?![a-zA-Z])"

        else:
            pattern = r"(?<![a-zA-Z])" + re.escape(normalized_skill) + r"(?![a-zA-Z])"

        if re.search(pattern, normalized_text):

            # Avoid duplicate CTE / CTEs
            if skill == "CTE" and "CTEs" in found_skills:
                continue

            found_skills.append(skill)

    return found_skills