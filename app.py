import streamlit as st
from langchain_groq import ChatGroq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import os

# 🔐 API KEY (Streamlit Cloud will use secrets)
api_key = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=api_key
)

# -------------------------
# AI FUNCTION
# -------------------------
def generate_resume(data):

    prompt = f"""
Generate ATS-friendly resume.

Rules:
- No markdown (** or *)
- Use • bullets

Name: {data['name']}
Education: {data['education']}
Skills: {data['skills']}
Projects: {data['projects']}
Experience: {data['experience']}
Certifications: {data['certifications']}
Links: {data['links']}
Job Description: {data['job_description']}
"""

    res = llm.invoke(prompt)
    return res.content


# -------------------------
# PDF FUNCTION
# -------------------------
def create_pdf(text):

    filename = "resume.pdf"

    doc = SimpleDocTemplate(filename)

    name_style = ParagraphStyle(name="Name", fontSize=18)
    section_style = ParagraphStyle(name="Section", fontSize=12)
    normal_style = ParagraphStyle(name="Normal", fontSize=10)

    content = []
    lines = text.split("\n")

    SECTION_KEYWORDS = [
        "Career Objective",
        "Professional Experience",
        "Education",
        "Technical Skills",
        "Projects",
        "Certifications",
        "Languages"
    ]

    for i, line in enumerate(lines):

        line = line.replace("**", "").replace("*", "").strip()

        if not line:
            content.append(Spacer(1, 8))
            continue

        if i == 0:
            content.append(Paragraph(f"<b>{line}</b>", name_style))
            continue

        if any(k in line for k in SECTION_KEYWORDS):
            content.append(Paragraph(line, section_style))
            content.append(HRFlowable(width="100%", thickness=1.5))
            continue

        content.append(Paragraph(line, normal_style))

    doc.build(content)
    return filename


# -------------------------
# UI
# -------------------------
st.title("AI Resume Builder 🚀")

name = st.text_input("Name")
education = st.text_input("Education")
skills = st.text_area("Skills")
projects = st.text_area("Projects")
experience = st.text_area("Experience")
certifications = st.text_area("Certifications")
links = st.text_area("Links")
jd = st.text_area("Job Description")

if st.button("Generate Resume"):

    data = {
        "name": name,
        "education": education,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "certifications": certifications,
        "links": links,
        "job_description": jd
    }

    resume = generate_resume(data)

    st.subheader("Resume")
    st.text(resume)

    pdf_file = create_pdf(resume)

    with open(pdf_file, "rb") as f:
        st.download_button(
            "Download PDF",
            f.read(),
            file_name="resume.pdf"
        )