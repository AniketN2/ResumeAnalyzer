import streamlit as st
import os
from agents.resume_parser import parse_resume
from agents.jd_parser import parse_job_description
from utils.pdf_reader import extract_text_from_pdf
from agents.matching_agent import match_candidate
from agents.reviewer_agent import generate_review
from agents.scoring_agent import calculate_score
# Page settings
st.set_page_config(
    page_title="Resume Screening Agent",
    page_icon="📄",
    layout="wide"
)

if "candidate" not in st.session_state:
    st.session_state.candidate = None

if "jd" not in st.session_state:
    st.session_state.jd = None

if "match_result" not in st.session_state:
    st.session_state.match_result = None

st.title("📄 Resume Screening Agent")
st.write("Upload a resume and extract text from PDF")

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# File uploader
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

paths = []


if uploaded_file is not None:

    # Save file
    file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    # 1. Calculate and show file size (convert bytes to KB)
    file_size_kb = uploaded_file.size / 1024
    st.write(f"**File Size:** {file_size_kb:.2f} KB")

    # // Potential Commit

    # 2. Add button to trigger text extraction and AI parsing
    if st.button("Extract & Parse Resume"):
        
        # Call reader utility
        extracted_text, num_pages = extract_text_from_pdf(file_path)

        # 3. Show total pages
        st.write(f"**Number of Pages:** {num_pages}")

        # 4. Calculate and show word count
        word_count = len(extracted_text.split())
        st.write(f"**Total Words:** {word_count}")

        # # Display extracted raw text
        # st.subheader("Extracted Resume Text")

        # st.text_area(
        #     "Resume Content",
        #     extracted_text,
        #     height=300
        # )

        # Parse candidate with OpenAI
        st.subheader("Parsed Candidate Information")
        
        with st.spinner("Analyzing resume with AI..."):
            candidate = parse_resume(extracted_text)

        # Only display JSON if parsing succeeded; otherwise show friendly error
        if candidate is not None:
            st.json(candidate.model_dump())
            st.session_state.candidate = candidate
        else:
            st.error("⚠️ Failed to analyze the resume. Please check your API key, connection, or try another file.")

    st.subheader("Job Description")
    job_description = st.text_area(
                "Paste Job Description",
                height=250
            )
    if st.button("Extract & Parse Job Description"):
        
        if job_description:

            jd = parse_job_description(job_description)

            st.subheader("Extracted Job Description")

            if jd is not None:
                st.json(jd.model_dump())
                st.session_state.jd = jd
            else:
                st.error("⚠️ Failed to analyze the job description. Please check your API key, connection, or try another file.")

    if st.button("Comparison"):
        candidate = st.session_state.candidate
        jd = st.session_state.jd

        if candidate is None:
            st.error("⚠️ Please extract and parse a resume before running comparison.")
            st.stop()

        if jd is None:
            st.error("⚠️ Please extract and parse a job description before running comparison.")
            st.stop()

        match_result = match_candidate(
        candidate,
        jd
        )
        st.session_state.match_result = match_result
        st.subheader("Matching Result")

        st.json(match_result.model_dump())
        st.metric(
        "Skill Match",
        f"{match_result.skill_match_percentage}%"
        )

        st.metric(
        "Required Experience",
        f"{match_result.required_experience_years} years"
        )

        st.metric(
        "Candidate Experience",
        f"{match_result.candidate_experience_years} years"
        )

        st.metric(
        "Experience Gap",
        f"{match_result.experience_gap_years} years"
        )

        st.success(
            f"Matched Skills: {len(match_result.matched_skills)}"
        )

        st.warning(
            f"Missing Skills: {len(match_result.missing_skills)}"
        )

        if match_result.experience_match:
            st.success("Experience requirement is satisfied.")
        else:
            st.error("Experience requirement is not satisfied.")

        st.write("### Matched Skills")
        st.write(match_result.matched_skills)

        st.write("### Missing Skills")
        st.write(match_result.missing_skills)

        st.write("### Extra Skills")
        st.write(match_result.extra_skills)

    if st.button("Scoring and review"):
        candidate = st.session_state.candidate
        jd = st.session_state.jd
        match_result = st.session_state.match_result

        if match_result is None:
            st.error("⚠️ Please run comparison before scoring and review.")
            st.stop()

        score = calculate_score(match_result)

        st.subheader("Candidate Score")

        st.metric(
            "Overall Score",
            f"{score.total_score}/100"
        )

        st.metric(
            "Recommendation",
            score.recommendation
        )

        st.write("### Score Breakdown")

        st.write(f"Skills : {score.skill_score}")

        st.write(f"Experience : {score.experience_score}")

        st.write(f"Education : {score.education_score}")

        review = generate_review(
        candidate,
        jd,
        match_result,
        score
        )
        st.subheader("HR Review")

        st.write(review.summary)

        st.subheader("Strengths")

        for strength in review.strengths:
            st.success(strength)

        st.subheader("Weaknesses")

        for weakness in review.weaknesses:
            st.warning(weakness)

        st.subheader("Interview Questions")

        for question in review.interview_questions:
            st.write(f"• {question}")

        st.subheader("Recommendation")

        st.info(review.final_recommendation)