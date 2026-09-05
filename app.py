import streamlit as st
import pymupdf

from src.skill_extractor import extract_skills
from src.semantic_matcher import calculate_similarity
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
from src.matcher import calculate_final_score
from src.recommendation import get_recommendation
from src.capability_analyzer import (
    extract_job_capabilities,
    find_capability_matches
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Job Matcher",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🤖 AI Resume Screening & Job Matcher")

st.write(
    "Upload a resume and provide a job description "
    "to evaluate the candidate's suitability."
)

st.divider()


# =========================================================
# FUNCTIONS
# =========================================================

def extract_resume_text(uploaded_file):

    uploaded_file.seek(0)

    file_bytes = uploaded_file.read()

    doc = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


def calculate_percentage(matched, total):

    if not total:
        return 0.0

    return (
        len(matched) / len(total)
    ) * 100


def normalize_skill(skill):

    return skill.strip().lower()


# =========================================================
# INPUT SECTION
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📄 Resume")

    uploaded_resume = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=300,
        placeholder="Paste the complete job description here..."
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True
):

    # -----------------------------------------------------
    # Validate input
    # -----------------------------------------------------

    if uploaded_resume is None:

        st.error(
            "Please upload a resume PDF."
        )

        st.stop()


    if not job_description.strip():

        st.error(
            "Please enter the job description."
        )

        st.stop()


    # =====================================================
    # ANALYSIS
    # =====================================================

    with st.spinner(
        "Analyzing resume and job description..."
    ):

        # -------------------------------------------------
        # Resume text
        # -------------------------------------------------

        resume_text = extract_resume_text(
            uploaded_resume
        )


        # -------------------------------------------------
        # Candidate information
        # -------------------------------------------------

        candidate_name = extract_name(
            resume_text
        )

        candidate_email = extract_email(
            resume_text
        )

        candidate_phone = extract_phone(
            resume_text
        )


        # -------------------------------------------------
        # Resume sections
        # -------------------------------------------------

        sections = extract_sections(
            resume_text
        )


        # -------------------------------------------------
        # Resume skills
        # -------------------------------------------------

        resume_skills = extract_skills(
            resume_text
        )


        # -------------------------------------------------
        # Job skills
        # -------------------------------------------------

        job_skills = extract_skills(
            job_description
        )


        # -------------------------------------------------
        # Required skills
        # -------------------------------------------------

        required_skills = extract_required_skills(
            job_description
        )


        # -------------------------------------------------
        # Preferred skills
        # -------------------------------------------------

        preferred_skills = extract_preferred_skills(
            job_description
        )


        # -------------------------------------------------
        # Remove duplicate skills
        # -------------------------------------------------

        required_skills = list(
            dict.fromkeys(required_skills)
        )

        preferred_skills = list(
            dict.fromkeys(preferred_skills)
        )

        job_skills = list(
            dict.fromkeys(job_skills)
        )


        # -------------------------------------------------
        # Resume skill set
        # -------------------------------------------------

        resume_skill_set = {
            normalize_skill(skill)
            for skill in resume_skills
        }


        # =================================================
        # REQUIRED SKILL MATCHING
        # =================================================

        required_matched = []

        required_missing = []

        for skill in required_skills:

            if normalize_skill(skill) in resume_skill_set:

                required_matched.append(skill)

            else:

                required_missing.append(skill)


        # =================================================
        # PREFERRED SKILL MATCHING
        # =================================================

        preferred_matched = []

        preferred_missing = []

        for skill in preferred_skills:

            if normalize_skill(skill) in resume_skill_set:

                preferred_matched.append(skill)

            else:

                preferred_missing.append(skill)


        # =================================================
        # ALL JOB SKILL MATCHING
        # =================================================

        matched_skills = []

        for skill in job_skills:

            if normalize_skill(skill) in resume_skill_set:

                matched_skills.append(skill)


        missing_skills = []

        for skill in job_skills:

            if normalize_skill(skill) not in resume_skill_set:

                missing_skills.append(skill)


        # =================================================
        # JOB CAPABILITIES
        # =================================================

        job_capabilities = extract_job_capabilities(
            job_description
        )


        # =================================================
        # CAPABILITY MATCHING
        # =================================================

        capability_matched, capability_missing = (
            find_capability_matches(
                resume_text,
                job_capabilities
            )
        )


        # =================================================
        # SCORES
        # =================================================

        required_score = calculate_percentage(
            required_matched,
            required_skills
        )


        preferred_score = calculate_percentage(
            preferred_matched,
            preferred_skills
        )


        # -------------------------------------------------
        # Capability score
        # -------------------------------------------------

        capability_score = calculate_percentage(
            capability_matched,
            job_capabilities
        )


        # -------------------------------------------------
        # Semantic similarity
        # -------------------------------------------------

        semantic_score = calculate_similarity(
            resume_text,
            job_description
        )


        # =================================================
        # FINAL SCORE
        # =================================================
        #
        # Required skills   = 45%
        # Preferred skills  = 15%
        # Capabilities      = 20%
        # Semantic similarity = 20%
        #
        # If there are NO preferred skills specified, or NO
        # capability keywords were detected in the job
        # description, that dimension's weight is redistributed
        # across the remaining dimensions instead of scoring a
        # flat (and unfair) 0%. See src/matcher.py for the exact
        # redistributed weights for each case.
        # =================================================

        final_score = calculate_final_score(
            required_score,
            preferred_score,
            capability_score,
            semantic_score,
            has_required_skills=bool(required_skills),
            has_preferred_skills=bool(preferred_skills),
            has_capabilities=bool(job_capabilities),
        )


        # -------------------------------------------------
        # Recommendation
        # -------------------------------------------------

        recommendation = get_recommendation(final_score)


    # =====================================================
    # CANDIDATE INFORMATION
    # =====================================================

    st.divider()

    st.header(
        "👤 Candidate Information"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Name",
            candidate_name
        )

    with c2:

        st.metric(
            "Email",
            candidate_email
        )

    with c3:

        st.metric(
            "Phone",
            candidate_phone
        )


    # =====================================================
    # FINAL SCORE
    # =====================================================

    st.divider()

    st.header(
        "🎯 AI Match Result"
    )

    score_col1, score_col2 = st.columns(
        [1, 2]
    )

    with score_col1:

        st.metric(
            "Final AI Match Score",
            f"{final_score:.2f}%"
        )


    with score_col2:

        if final_score >= 80:

            st.success(
                "🟢 EXCELLENT MATCH"
            )

        elif final_score >= 70:

            st.success(
                "🟢 GOOD MATCH"
            )

        elif final_score >= 55:

            st.warning(
                "🟡 PARTIAL MATCH"
            )

        else:

            st.error(
                "🔴 POOR MATCH"
            )


    # =====================================================
    # SCORE BREAKDOWN
    # =====================================================

    st.subheader(
        "📊 Score Breakdown"
    )

    score1, score2, score3, score4 = st.columns(4)

    with score1:

        st.metric(
            "Required Skills",
            (
                f"{required_score:.2f}%"
                if required_skills
                else "N/A"
            )
        )

    with score2:

        st.metric(
            "Preferred Skills",
            (
                f"{preferred_score:.2f}%"
                if preferred_skills
                else "N/A"
            )
        )

    with score3:

        st.metric(
            "Job Capabilities",
            (
                f"{capability_score:.2f}%"
                if job_capabilities
                else "N/A"
            )
        )

    with score4:

        st.metric(
            "Semantic Similarity",
            f"{semantic_score:.2f}%"
        )


    # =====================================================
    # SKILL ANALYSIS
    # =====================================================

    st.divider()

    st.header(
        "🛠️ Skill Analysis"
    )

    skill_col1, skill_col2 = st.columns(2)


    # -----------------------------------------------------
    # Matched skills
    # -----------------------------------------------------

    with skill_col1:

        st.subheader(
            "✅ Matched Skills"
        )

        if matched_skills:

            for skill in matched_skills:

                st.success(skill)

        else:

            st.info(
                "No matching technical skills found."
            )


    # -----------------------------------------------------
    # Missing skills
    # -----------------------------------------------------

    with skill_col2:

        st.subheader(
            "❌ Missing Skills"
        )

        if missing_skills:

            for skill in missing_skills:

                st.error(skill)

        else:

            st.success(
                "No missing technical skills."
            )


    # =====================================================
    # REQUIRED SKILLS
    # =====================================================

    st.divider()

    st.header(
        "📌 Required Skills"
    )

    if required_skills:

        req_col1, req_col2 = st.columns(2)


        with req_col1:

            st.subheader(
                "Matched"
            )

            if required_matched:

                for skill in required_matched:

                    st.success(
                        f"✓ {skill}"
                    )

            else:

                st.info(
                    "No required skills matched."
                )


        with req_col2:

            st.subheader(
                "Missing"
            )

            if required_missing:

                for skill in required_missing:

                    st.error(
                        f"✗ {skill}"
                    )

            else:

                st.success(
                    "✓ All required skills matched."
                )

    else:

        st.info(
            "No required skills could be clearly identified in "
            "this job description."
        )


    # =====================================================
    # PREFERRED SKILLS
    # =====================================================

    st.divider()

    st.header(
        "⭐ Preferred Skills"
    )

    if preferred_skills:

        pref_col1, pref_col2 = st.columns(2)


        with pref_col1:

            st.subheader(
                "Matched"
            )

            if preferred_matched:

                for skill in preferred_matched:

                    st.success(
                        f"✓ {skill}"
                    )

            else:

                st.info(
                    "No preferred skills matched."
                )


        with pref_col2:

            st.subheader(
                "Missing"
            )

            if preferred_missing:

                for skill in preferred_missing:

                    st.error(
                        f"✗ {skill}"
                    )

            else:

                st.success(
                    "✓ All preferred skills matched."
                )

    else:

        st.info(
            "No preferred skills were explicitly "
            "specified in this job description."
        )


    # =====================================================
    # JOB CAPABILITIES
    # =====================================================

    st.divider()

    st.header(
        "🧩 Job Capabilities"
    )

    st.write(
        "Capabilities detected from the job description "
        "and compared against the resume."
    )

    cap_col1, cap_col2 = st.columns(2)


    with cap_col1:

        st.subheader(
            "✅ Matched Capabilities"
        )

        if capability_matched:

            for capability in capability_matched:

                st.success(
                    f"✓ {capability}"
                )

        else:

            st.info(
                "No matching capabilities detected."
            )


    with cap_col2:

        st.subheader(
            "❌ Missing Capabilities"
        )

        if capability_missing:

            for capability in capability_missing:

                st.warning(
                    f"✗ {capability}"
                )

        else:

            st.success(
                "All detected capabilities are represented."
            )


    # =====================================================
    # RESUME SKILLS
    # =====================================================

    st.divider()

    st.header(
        "📚 Resume Skills"
    )

    if resume_skills:

        st.write(
            ", ".join(resume_skills)
        )

    else:

        st.info(
            "No skills detected in the resume."
        )


    # =====================================================
    # JOB SKILLS
    # =====================================================

    st.divider()

    st.header(
        "💼 Job Skills"
    )

    if job_skills:

        st.write(
            ", ".join(job_skills)
        )

    else:

        st.info(
            "No technical skills detected from the job description."
        )


    # =====================================================
    # RESUME DETAILS
    # =====================================================

    st.divider()

    st.header(
        "📄 Resume Details"
    )

    if sections:

        for section, content in sections.items():

            with st.expander(
                section.title()
            ):

                if content.strip():

                    st.write(
                        content.strip()
                    )

                else:

                    st.info(
                        "No content detected."
                    )

    else:

        st.info(
            "No resume sections detected."
        )


    # =====================================================
    # AI RECOMMENDATION
    # =====================================================

    st.divider()

    st.header(
        "🤖 AI Recommendation"
    )

    if final_score >= 80:

        st.success(
            f"Recommendation: {recommendation}"
        )

    elif final_score >= 55:

        st.warning(
            f"Recommendation: {recommendation}"
        )

    else:

        st.error(
            f"Recommendation: {recommendation}"
        )


    # =====================================================
    # ANALYSIS DETAILS
    # =====================================================

    st.divider()

    st.header(
        "🔎 Analysis Details"
    )

    st.write(
        f"""
**Required skill coverage:** {
    f"{required_score:.2f}%"
    if required_skills
    else "No required skills could be clearly identified in this job description"
}

**Preferred skill coverage:** {
    f"{preferred_score:.2f}%"
    if preferred_skills
    else "No preferred skills specified"
}

**Capability coverage:** {
    f"{capability_score:.2f}%"
    if job_capabilities
    else "No capability keywords detected in this job description"
}

**Semantic similarity:** {semantic_score:.2f}%

**Final AI match score:** {final_score:.2f}%
"""
    )