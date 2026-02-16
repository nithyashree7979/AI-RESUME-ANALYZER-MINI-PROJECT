import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import io

from utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    analyze_resume_text,
    generate_summary_and_structured_json,
)
 
load_dotenv()

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_role = st.text_input("Target Job Role")
job_description = st.text_area("Job Description (Optional)")

analyze = st.button("Analyze Resume")

if analyze and uploaded_file:

    filetype = uploaded_file.type

    if filetype == "application/pdf":
        resume_text = extract_text_from_pdf(io.BytesIO(uploaded_file.read()))

    elif filetype in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ):
        resume_text = extract_text_from_docx(uploaded_file)

    else:
        st.error("Unsupported file format")
        st.stop()

    required_keywords = job_description.split() if job_description else []
    local_result = analyze_resume_text(resume_text, required_keywords)

    st.subheader("Breakdown:")
    st.json(local_result["breakdown"])

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None

    ai_data = generate_summary_and_structured_json(
        client, resume_text, job_role, job_description
    )

    st.subheader("Summary")
    st.json(ai_data.get("summary", []))

    st.subheader("Strengths")
    st.json(ai_data.get("strengths", []))

    st.subheader("Weaknesses")
    st.json(ai_data.get("weaknesses", []))

    st.subheader("Improvements")
    st.json(ai_data.get("improvements", []))

    st.subheader("Keywords Found")
    st.json(ai_data.get("keywords_found", []))

    st.subheader("Keywords Missing")
    st.json(ai_data.get("keywords_missing", []))
