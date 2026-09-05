import re

from src.skill_extractor import SKILLS


# Required/preferred classification now checks against the same skill
# vocabulary used everywhere else in the app (src/skill_extractor.py),
# instead of a separate, smaller, hand-maintained list that was missing
# entries like DAX, Power Query, Jupyter Notebook, and Docker -- those
# skills could never be classified as required/preferred before, no
# matter how the job description phrased them.
KNOWN_SKILLS = SKILLS


REQUIRED_PHRASES = [
    "required",
    "must have",
    "must",
    "strong knowledge",
    "strong experience",
    "working knowledge",
    "proficient",
    "proficiency",
    "experience with",
    "experience in",
    "experience using",
    "experience creating",
    "experience building",
    "experience developing",
    "experience designing",
    "hands-on experience",
    "knowledge of",
    "good knowledge",
    "familiarity with",
    "ability to",
    "skilled in",
    "expertise in",
    "understanding of",
]


PREFERRED_PHRASES = [
    "preferred",
    "prefer",
    "desirable",
    "desired",
    "a plus",
    "plus",
    "nice to have",
    "bonus",
    "advantageous",
    "ideally",
]


def normalize(text):
    text = text.lower()
    # Collapse repeated spaces/tabs but keep line breaks intact, so
    # get_sentences() can still tell separate lines apart. Collapsing
    # everything (including newlines) into one blob previously caused
    # a "Preferred:" heading anywhere in the text to make every skill
    # in the whole document look "preferred", including ones clearly
    # listed under "Requirements:".
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _skill_in_text(skill, text):
    """
    Word-boundary-aware check for whether `skill` appears in `text`.
    A plain substring check (`skill in text`) badly false-positives for
    short skill names -- "C" would "match" almost any sentence in
    English, since most contain the letter c somewhere (e.g.
    "experience" does).
    """

    pattern = (
        r"(?<![a-zA-Z])"
        + re.escape(skill.lower())
        + r"(?![a-zA-Z])"
    )

    return re.search(pattern, text) is not None


def get_sentences(text):
    """
    Split into sentence-like chunks. Handles both prose job
    descriptions ("Experience with Python is required.") and
    bullet/list-style ones with no terminal punctuation, by treating
    each line as its own chunk before further splitting on sentence
    punctuation within that line.
    """

    sentences = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        sentences.extend(
            part.strip()
            for part in re.split(r"(?<=[.!?])\s+", line)
            if part.strip()
        )

    return sentences


# =========================================================
# HEADING-BASED EXTRACTION
# =========================================================
# Many job postings list required/preferred skills as a bare
# bullet list under a heading:
#
#   Required Skills:
#   Python
#   SQL
#
# There's no requirement phrase ("required", "experience with", ...)
# attached to each individual skill line for classify_sentence() to
# key off of, so the sentence-level phrase classifier below can't see
# it. This section walks the document heading-by-heading instead and
# attributes any recognized skill mentioned while "under" a required
# or preferred heading accordingly, as a supplementary signal.
# =========================================================

REQUIRED_HEADINGS = [
    "required",
    "required skills",
    "requirements",
    "must have",
    "must have skills",
    "mandatory skills",
    "required qualifications",
    "technical requirements",
]

PREFERRED_HEADINGS = [
    "preferred",
    "preferred skills",
    "nice to have",
    "good to have",
    "desired skills",
    "preferred qualifications",
    "bonus skills",
]

# Headings that end a required/preferred block without starting a new
# one -- seeing one of these resets back to "not in a skills list".
NEUTRAL_HEADINGS = [
    "responsibilities",
    "about the role",
    "about us",
    "about the company",
    "qualifications",
    "education",
    "experience",
    "benefits",
    "what youll do",
    "what we offer",
    "job type",
    "location",
    "job title",
    "role",
    "overview",
]


def _looks_like_heading(line):
    """
    Treat a line as a heading only if it ends with a colon (and isn't
    unreasonably long for a heading). This is intentionally narrow --
    an all-caps heuristic would misfire on short all-caps skill names
    like "SQL" or "AWS" sitting alone on their own bullet line.
    """

    stripped = line.strip()

    if not stripped or len(stripped) > 60:
        return False

    return stripped.endswith(":")


def extract_skills_by_heading(job_description):

    required_found = []
    preferred_found = []

    current_bucket = None

    for raw_line in job_description.split("\n"):

        line = raw_line.strip()

        if not line:
            continue

        if _looks_like_heading(line):

            normalized_heading = re.sub(
                r"[^a-z\s]", "", line.lower()
            ).strip()
            normalized_heading = re.sub(
                r"\s+", " ", normalized_heading
            )

            if any(h in normalized_heading for h in REQUIRED_HEADINGS):
                current_bucket = "required"

            elif any(h in normalized_heading for h in PREFERRED_HEADINGS):
                current_bucket = "preferred"

            else:
                # Any other heading (recognized neutral one, or an
                # unrecognized one) ends the current bucket, so we
                # don't keep attributing skills to a stale heading.
                current_bucket = None

            continue

        if current_bucket is None:
            continue

        # Only attribute skills from bare list lines (no terminal
        # punctuation) to the current heading. A line ending in
        # ".", "!", or "?" is a full sentence with its own wording,
        # and should be judged by that wording (classify_sentence)
        # rather than by a heading that might be several lines above
        # it -- e.g. "Knowledge of machine learning is a plus." sits
        # under a "Requirements:" heading in some job descriptions,
        # but its own phrasing already says "preferred", which should
        # win over the ambient heading.
        if line.rstrip().endswith((".", "!", "?")):
            continue

        line_lower = line.lower()

        for skill in KNOWN_SKILLS:

            if _skill_in_text(skill, line_lower):

                if current_bucket == "required":

                    if skill not in required_found:
                        required_found.append(skill)

                elif current_bucket == "preferred":

                    if skill not in preferred_found:
                        preferred_found.append(skill)

    return required_found, preferred_found


def is_hiring_ai_sentence(sentence):
    """
    Prevent AI mentioned only in the hiring-process
    paragraph from being treated as a candidate skill.
    """

    sentence = sentence.lower()

    hiring_phrases = [
        "hiring process",
        "reviewing applications",
        "analyzing resumes",
        "assessing responses",
        "recruitment team",
        "final hiring decisions",
        "application materials",
        "verification signals",
    ]

    return any(
        phrase in sentence
        for phrase in hiring_phrases
    )


def classify_sentence(sentence):

    sentence = sentence.lower()

    if is_hiring_ai_sentence(sentence):
        return None

    for phrase in PREFERRED_PHRASES:

        if phrase in sentence:
            return "preferred"

    for phrase in REQUIRED_PHRASES:

        if phrase in sentence:
            return "required"

    return None


def extract_required_skills(job_description):

    required_skills = []

    text = normalize(job_description)

    sentences = get_sentences(text)

    for skill in KNOWN_SKILLS:

        for sentence in sentences:

            if _skill_in_text(skill, sentence):

                classification = classify_sentence(sentence)

                if classification == "required":

                    if skill not in required_skills:
                        required_skills.append(skill)

                    break

    heading_required, heading_preferred = extract_skills_by_heading(
        job_description
    )

    # Heading structure is authoritative where it applies. If a skill
    # was explicitly listed under a "Preferred Skills" heading, don't
    # let an incidental phrase match elsewhere in that same bullet
    # ("experience with X", "understanding of X") override that and
    # call it required too -- the document told us exactly where the
    # author meant it to go.
    required_skills = [
        skill for skill in required_skills
        if skill not in heading_preferred
    ]

    # Supplementary pass: catch bare bullet lists under a "Required
    # Skills" style heading that the phrase classifier can't see.
    for skill in heading_required:

        if skill not in required_skills:
            required_skills.append(skill)

    return required_skills


def extract_preferred_skills(job_description):

    preferred_skills = []

    text = normalize(job_description)

    sentences = get_sentences(text)

    for skill in KNOWN_SKILLS:

        for sentence in sentences:

            if _skill_in_text(skill, sentence):

                classification = classify_sentence(sentence)

                if classification == "preferred":

                    if skill not in preferred_skills:
                        preferred_skills.append(skill)

                    break

    heading_required, heading_preferred = extract_skills_by_heading(
        job_description
    )

    # Same priority rule as extract_required_skills, mirrored: a skill
    # explicitly listed under "Required Skills" shouldn't get pulled
    # into preferred just because of incidental phrase wording.
    preferred_skills = [
        skill for skill in preferred_skills
        if skill not in heading_required
    ]

    # Supplementary pass: catch bare bullet lists under a "Preferred
    # Skills" style heading that the phrase classifier can't see.
    for skill in heading_preferred:

        if skill not in preferred_skills:
            preferred_skills.append(skill)

    return preferred_skills