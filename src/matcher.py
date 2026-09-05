BASE_WEIGHTS = {
    "required": 0.45,
    "preferred": 0.15,
    "capability": 0.20,
    "semantic": 0.20,
}


def calculate_final_score(
    required_score,
    preferred_score,
    capability_score,
    semantic_score,
    has_required_skills=True,
    has_preferred_skills=True,
    has_capabilities=True,
):
    """
    Calculate the final AI resume-job match score.

    Base weights (used when required skills, preferred skills, and
    capability keywords were all detected in the job description):

        Required skills      = 45%
        Preferred skills     = 15%
        Job capabilities     = 20%
        Semantic similarity  = 20%

    If any of required/preferred skills or capability keywords come
    back empty for a given job description, that dimension's score is
    meaningless -- it isn't 0% because the candidate is missing
    anything, it's 0% because there was nothing to check against.
    Scoring it as a flat 0% and still weighting it would unfairly drag
    the final score down for reasons that have nothing to do with the
    candidate, so its weight is redistributed proportionally across
    the remaining dimensions instead.

    has_required_skills / has_preferred_skills / has_capabilities
    should be False when the job description yielded an empty
    required_skills / preferred_skills / job_capabilities list --
    not simply when the *match* against the resume was 0%. Semantic
    similarity has no "empty" case since it's computed from free text.
    """

    active = {
        "required": has_required_skills,
        "preferred": has_preferred_skills,
        "capability": has_capabilities,
        "semantic": True,
    }

    scores = {
        "required": required_score,
        "preferred": preferred_score,
        "capability": capability_score,
        "semantic": semantic_score,
    }

    active_weight_total = sum(
        weight
        for dimension, weight in BASE_WEIGHTS.items()
        if active[dimension]
    )

    if active_weight_total == 0:
        return 0.0

    final_score = 0.0

    for dimension, weight in BASE_WEIGHTS.items():

        if not active[dimension]:
            continue

        final_score += scores[dimension] * (weight / active_weight_total)

    return final_score
