import streamlit as st
import os
from agents.jd_parser import parse_job_description
from services.pipeline import process_resume
from utils.excel_export import export_results

# Page settings
st.set_page_config(
    page_title="Resume Screening Agent",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Screening Agent")
st.write("Upload resumes and a job description to screen candidates")

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# File uploader
uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf"],
    accept_multiple_files=True
)

paths = []

for file in uploaded_files:
    file_path = os.path.join("uploads", file.name)

    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    paths.append(file_path)

st.subheader("Job Description")
job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Analyze Resumes"):

    if not job_description:
        st.error("⚠️ Please paste a job description before analyzing.")
        st.stop()

    if not paths:
        st.error("⚠️ Please upload at least one resume before analyzing.")
        st.stop()

    jd = parse_job_description(job_description)

    if jd is None:
        st.error("⚠️ Failed to analyze the job description. Please check your API key, connection, or try again.")
        st.stop()

    results = []
    progress = st.progress(0)

    for i, path in enumerate(paths):
        try:
            result = process_resume(path, jd)
            results.append(result)
        except Exception as e:
            st.warning(f"⚠️ Failed to process {os.path.basename(path)}: {e}")

        progress.progress((i + 1) / len(paths))

    if not results:
        st.error("⚠️ No resumes were processed successfully.")
        st.stop()

    results.sort(
        key=lambda x: x["score"].total_score,
        reverse=True
    )

    st.subheader("Top Candidates")

    for index, result in enumerate(results, start=1):
        candidate = result["candidate"]
        match = result["match"]
        score = result["score"]
        #Uncomment the following line if you want to display the review for Version 1 and 2
        # review = result["review"]

        with st.expander(f"{index}. {candidate.name} — {score.total_score}/100 — {score.recommendation}"):

            st.write("### Candidate Info")
            st.json(candidate.model_dump())

            st.write("### Matching Result")
            st.metric("Skill Match", f"{match.skill_match_percentage}%")
            st.metric("Required Experience", f"{match.required_experience_years} years")
            st.metric("Candidate Experience", f"{match.candidate_experience_years} years")
            st.metric("Experience Gap", f"{match.experience_gap_years} years")

            st.success(f"Matched Skills: {len(match.matched_skills)}")
            st.warning(f"Missing Skills: {len(match.missing_skills)}")

            if match.experience_match:
                st.success("Experience requirement is satisfied.")
            else:
                st.error("Experience requirement is not satisfied.")

            st.write("**Matched Skills:**", match.matched_skills)
            st.write("**Missing Skills:**", match.missing_skills)
            st.write("**Extra Skills:**", match.extra_skills)

            st.write("### Score Breakdown")
            st.write(f"Skills: {score.skill_score}")
            st.write(f"Experience: {score.experience_score}")
            st.write(f"Education: {score.education_score}")
# For Version 1 and 2 

            # st.write("### HR Review")
            # st.write(review.summary)

            # st.write("**Strengths**")
            # for strength in review.strengths:
            #     st.success(strength)

            # st.write("**Weaknesses**")
            # for weakness in review.weaknesses:
            #     st.warning(weakness)

            # st.write("**Interview Questions**")
            # for question in review.interview_questions:
            #     st.write(f"• {question}")

            # st.write("**Final Recommendation**")
            # st.info(review.final_recommendation)

# For Langgraph Version 
            review = result.get("review")
            improvement = result.get("improvement")

            if review:
                st.write("### HR Review")
                st.write(review.summary)

                st.write("**Strengths**")
                for strength in review.strengths:
                    st.success(strength)

                st.write("**Weaknesses**")
                for weakness in review.weaknesses:
                    st.warning(weakness)

                st.write("**Interview Questions**")
                for question in review.interview_questions:
                    st.write(f"• {question}")

                st.write("**Final Recommendation**")
                st.info(review.final_recommendation)

            elif improvement:
                st.write("### Resume Improvement Plan")
                st.info("This candidate scored below the interview threshold — here's a coaching plan instead of an HR review.")
                st.write(improvement.summary)

                st.write("**Missing Skills**")
                for skill in improvement.missing_skills:
                    st.warning(skill)

                st.write("**Suggested Improvements**")
                for suggestion in improvement.suggestions:
                    st.write(f"• {suggestion}")

    excel_bytes = export_results(results)

    st.download_button(
    label="📥 Download Results as Excel",
    data=excel_bytes,
    file_name="results.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )