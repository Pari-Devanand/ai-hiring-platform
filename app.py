import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="AI Hiring Platform", layout="wide")

# =============================
# HEADER
# =============================
st.markdown(
    """
    <h1 style='text-align:center;'>AI Hiring & Job Matching Platform</h1>
    """,
    unsafe_allow_html=True
)

st.write("A dual-dashboard AI system for recruiters and job seekers")

# =============================
# ROLE SELECT
# =============================
role = st.sidebar.selectbox(
    "Login as",
    ["Applicant", "Recruiter"]
)

# =============================
# LOAD DATA
# =============================
jobs = pd.read_csv("jobs.csv")

# =============================
# APPLICANT DASHBOARD
# =============================
if role == "Applicant":

    st.header("Applicant Dashboard")

    # =========================
    # PROFILE
    # =========================
    st.subheader("Your Profile")

    name = st.text_input("Name")
    skills_input = st.text_input("Enter your skills", "python,ml,sql")

    roles = st.multiselect(
        "Target roles",
        ["AI Engineer", "Data Scientist", "ML Intern", "Backend Developer"]
    )

    # =========================
    # RESUME UPLOAD
    # =========================
    st.subheader("Upload Resume")
    uploaded_files = st.file_uploader(
        "Upload resume",
        accept_multiple_files=True,
        type=["pdf", "txt"]
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} resume uploaded")

    # =========================
    # JOB MATCHING
    # =========================
    st.subheader("Recommended Jobs")

    combined_input = skills_input + "," + ",".join(roles)
    user_skills = set([s.strip().lower() for s in combined_input.split(",")])

    scores = []
    for _, row in jobs.iterrows():
        job_skills = set(row["skills"].split(","))
        score = len(user_skills.intersection(job_skills))
        scores.append(score)

    jobs["match_score"] = scores
    ranked = jobs.sort_values(by="match_score", ascending=False)

    st.dataframe(ranked)

    # =========================
    # SELECT JOBS
    # =========================
    st.subheader("Apply to Jobs")

    selected_jobs = st.multiselect(
        "Select jobs",
        ranked["title"].tolist()
    )

    job_desc = st.text_area("Paste job description for tailoring")

    templates = [
        "Developed machine learning systems using Python.",
        "Built AI automation tools for analytics.",
        "Implemented NLP ranking models.",
        "Worked with data pipelines and ML workflows.",
        "Created predictive models and evaluation systems."
    ]

    if st.button("Generate Tailored Resume Lines"):
        result = "\n".join(random.sample(templates, 4))
        st.text(result)

    if st.button("Submit Applications"):
        if selected_jobs:
            status_list = []
            for job in selected_jobs:
                status_list.append({"Job": job, "Status": "Applied"})

            status_df = pd.DataFrame(status_list)

            st.subheader("Application Tracker")
            st.dataframe(status_df)
        else:
            st.warning("Select at least one job")


# =============================
# RECRUITER DASHBOARD
if role == "Recruiter":

    st.header("Recruiter Dashboard")

    st.subheader("Upload Job Description")
    job_text = st.text_area("Paste job description")

    st.subheader("Upload Candidate Resumes")
    resumes = st.file_uploader(
        "Upload resumes",
        accept_multiple_files=True,
        type=["pdf", "txt"]
    )

    candidate_data = []

    if resumes:
        st.success(f"{len(resumes)} resumes uploaded")

        # simulate scoring
        for file in resumes:
            score = random.randint(60, 95)
            candidate_data.append({
                "Name": file.name,
                "Match Score": score
            })

        candidates_df = pd.DataFrame(candidate_data)
        ranked_df = candidates_df.sort_values(by="Match Score", ascending=False)

        st.subheader("Candidate Ranking")
        st.dataframe(ranked_df)

        st.subheader("Shortlist Candidates")

        shortlist = st.multiselect(
            "Select candidates to shortlist",
            ranked_df["Name"].tolist()
        )

        if st.button("Shortlist Selected"):
            st.success(f"Shortlisted: {', '.join(shortlist)}")

            status_data = []
            for name in ranked_df["Name"]:
                if name in shortlist:
                    status = "Shortlisted"
                else:
                    status = "On Hold"
                status_data.append({"Candidate": name, "Status": status})

            status_df = pd.DataFrame(status_data)

            st.subheader("Application Status")
            st.dataframe(status_df)
