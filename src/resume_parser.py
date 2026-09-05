import re


def extract_email(text):
    """
    Extract email address from resume text.
    """

    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


def extract_phone(text):
    """
    Extract phone number from resume text.
    """

    pattern = r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


def extract_name(text):
    """
    Try to extract the candidate's name
    from the first few lines of the resume.
    """

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if lines:
        return lines[0]

    return None