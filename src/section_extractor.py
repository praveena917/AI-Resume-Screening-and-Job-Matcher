import re


# Canonical section name -> known header variants that should map to it.
# Real resumes rarely use the bare canonical word alone ("Summary"), so we
# match on common variants too (e.g. "Professional Summary", "Work History").
SECTION_ALIASES = {
    "summary": [
        "summary",
        "professional summary",
        "career summary",
        "summary of qualifications",
        "profile",
        "professional profile",
    ],
    "objective": [
        "objective",
        "career objective",
        "professional objective",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "relevant experience",
        "employment history",
        "work history",
    ],
    "education": [
        "education",
        "academic background",
        "educational background",
        "academic qualifications",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "skills summary",
        "areas of expertise",
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses and certifications",
        "licenses certifications",
    ],
    "achievements": [
        "achievements",
        "awards",
        "honors and awards",
        "honors awards",
    ],
    "internships": [
        "internships",
        "internship experience",
    ],
}

# Flat lookup: header variant -> canonical section name
_ALIAS_TO_SECTION = {
    alias: canonical
    for canonical, aliases in SECTION_ALIASES.items()
    for alias in aliases
}


def extract_sections(text):
    """
    Extract common resume sections.
    """

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    sections = {}
    current_section = None

    for line in lines:

        normalized = line.lower().strip()

        # Remove common formatting characters
        normalized = re.sub(
            r'[^a-z\s]',
            '',
            normalized
        ).strip()

        # Collapse any double spaces left behind by the strip above
        normalized = re.sub(r'\s+', ' ', normalized)

        canonical_section = _ALIAS_TO_SECTION.get(normalized)

        if canonical_section:

            current_section = canonical_section

            # Use setdefault (not reset-to-empty) so a section that's
            # headed twice under different aliases (or repeated by
            # mistake) accumulates content instead of overwriting it.
            sections.setdefault(current_section, "")

        elif current_section:

            sections[current_section] += line + "\n"

    return sections