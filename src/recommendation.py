def get_recommendation(final_score):
    """
    Turn the final AI match score into a human-readable
    recommendation label.
    """

    if final_score >= 80:
        return "EXCELLENT MATCH"

    elif final_score >= 70:
        return "GOOD MATCH"

    elif final_score >= 55:
        return "PARTIAL MATCH"

    else:
        return "POOR MATCH"
