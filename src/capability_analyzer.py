# =========================================================
# CAPABILITY DETECTION
# =========================================================
# These are capabilities explicitly relevant to the type
# of work described in the job description.
#
# This is separate from technical "skills" so the application
# does not incorrectly invent Tableau, Git, etc.
#
# NOTE: this keyword list was originally tuned against one
# specific job posting's wording (phrases like "chase the why"
# and "dashboard upkeep" are verbatim from it). For job
# descriptions phrased differently, extract_job_capabilities()
# may detect few or no capabilities -- app.py handles that by
# excluding the capability dimension from the final score
# rather than scoring it 0%, but the keyword list itself would
# benefit from being broadened/generalized in a follow-up pass.
# =========================================================

CAPABILITY_KEYWORDS = {

    "Data Analysis": [
        "data analysis",
        "analyze data",
        "analyzing data",
        "analyse data"
    ],

    "Data Quality": [
        "data quality",
        "clean data",
        "clean, connected, and reliable"
    ],

    "Data Validation": [
        "data validation",
        "validate data",
        "validate"
    ],

    "QA / Quality Checks": [
        "qa checks",
        "quality checks",
        "qa"
    ],

    "Automation": [
        "automation",
        "automations",
        "automate"
    ],

    "Data Integration": [
        "data integration",
        "data integrations",
        "integrations",
        "integrating data"
    ],

    "Anomaly Detection": [
        "anomalies",
        "anomaly",
        "gaps and anomalies",
        "detect anomalies"
    ],

    "Dashboard Support": [
        "dashboard",
        "dashboards",
        "dashboard upkeep"
    ],

    "Data Queries": [
        "data queries",
        "queries"
    ],

    "Predictive Analytics": [
        "predictive analytics",
        "predicts",
        "predictions"
    ],

    "Documentation": [
        "document what you build",
        "documentation",
        "document"
    ],

    "Problem Solving": [
        "problem-solving",
        "problem solving",
        "dig into why",
        "chase the why"
    ],

    "Data Cleaning": [
        "data cleaning",
        "cleaning data",
        "cleaned data"
    ]
}


def extract_job_capabilities(job_description):

    text = job_description.lower()

    detected = []

    for capability, keywords in CAPABILITY_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in text:

                detected.append(capability)

                break

    return detected


# =========================================================
# CAPABILITY MATCHING
# =========================================================

RESUME_CAPABILITY_KEYWORDS = {

    "Data Analysis": [
        "data analysis",
        "analyzed",
        "analysis",
        "data analyst"
    ],

    "Data Quality": [
        "data quality",
        "report accuracy",
        "data accuracy",
        "data cleaning",
        "cleaned"
    ],

    "Data Validation": [
        "validation",
        "validated",
        "accuracy",
        "data accuracy"
    ],

    "QA / Quality Checks": [
        "qa",
        "quality check",
        "quality checks"
    ],

    "Automation": [
        "automation",
        "automated",
        "automate"
    ],

    "Data Integration": [
        "data integration",
        "integrations",
        "integrated"
    ],

    "Anomaly Detection": [
        "anomaly",
        "anomalies",
        "outlier",
        "outliers"
    ],

    "Dashboard Support": [
        "dashboard",
        "dashboards",
        "power bi"
    ],

    "Data Queries": [
        "sql",
        "query",
        "queries"
    ],

    "Predictive Analytics": [
        "predictive",
        "prediction",
        "machine learning"
    ],

    "Documentation": [
        "documentation",
        "documented",
        "document"
    ],

    "Problem Solving": [
        "problem solving",
        "problem-solving",
        "solved",
        "analysis"
    ],

    "Data Cleaning": [
        "data cleaning",
        "cleaned",
        "cleaning"
    ]
}


def find_capability_matches(resume_text, job_capabilities):

    resume_lower = resume_text.lower()

    matched = []
    missing = []

    for capability in job_capabilities:

        keywords = RESUME_CAPABILITY_KEYWORDS.get(
            capability,
            []
        )

        found = False

        for keyword in keywords:

            if keyword.lower() in resume_lower:

                found = True
                break

        if found:

            matched.append(capability)

        else:

            missing.append(capability)

    return matched, missing
