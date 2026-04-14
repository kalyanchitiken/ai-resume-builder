import streamlit as st
from langchain_groq import ChatGroq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import os

# -------------------------
# 🔐 API KEY
# -------------------------
api_key = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=api_key
)

# -------------------------
# 🧠 AI FUNCTION
# -------------------------
def generate_resume(data):

    prompt = f"""
You are a professional resume writer.

Generate resume in EXACT CLEAN FORMAT.

IMPORTANT RULES:
- ONLY main headings should be bold
- Sub-sections should NOT be bold
- Keep everything aligned clean
- Skills should NOT break randomly
- No markdown (**)

FORMAT:

Name

Email | Phone | Location | LinkedIn | GitHub

--------------------------------------------------

CAREER OBJECTIVE:
(4 lines)

--------------------------------------------------

PROFESSIONAL TRAINING
Role
Company | Duration | Location
• Bullet points

--------------------------------------------------

EDUCATION
Degree
College

--------------------------------------------------

TECHNICAL SKILLS

Agentic AI & LLM Development:
(list)

Deep Learning:
(list)

Machine Learning:
(list)

Programming Data Analysis & Libraries:
(list)

Chatbot & LLM Development:
(list)

Core Concepts:
(list)

Natural Language Processing (NLP):
(list)

Tools & Platforms:
(list)

--------------------------------------------------

PROJECTS
Project Name
• Points

--------------------------------------------------

CERTIFICATES
• List

--------------------------------------------------

LANGUAGES
List

--------------------------------------------------

User Data:
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
# 📄 PDF FUNCTION
# -------------------------
def create_pdf(text, filename="resume.pdf"):

    doc = SimpleDocTemplate(filename)

    name_style = ParagraphStyle(name="Name", fontSize=18, spaceAfter=6)
    heading_style = ParagraphStyle(name="Heading", fontSize=11, spaceBefore=10)
    normal_style = ParagraphStyle(name="Normal", fontSize=10, leading=14)

    content = []
    lines = text.split("\n")

    for i, line in enumerate(lines):

        line = line.strip()

        if not line:
            content.append(Spacer(1, 5))
            continue

        # NAME
        if i == 0:
            content.append(Paragraph(f"<b>{line}</b>", name_style))
            continue

        # HEADINGS
        if line in [
            "CAREER OBJECTIVE:",
            "PROFESSIONAL TRAINING",
            "EDUCATION",
            "TECHNICAL SKILLS",
            "PROJECTS",
            "CERTIFICATES",
            "LANGUAGES"
        ]:
            content.append(Paragraph(f"<b>{line}</b>", heading_style))
            content.append(HRFlowable(width="100%", thickness=1.2, color=colors.black))
            continue

        content.append(Paragraph(line, normal_style))

    doc.build(content)
    return filename


# -------------------------
# 🎯 STREAMLIT UI (VERY IMPORTANT 🔥)
# -------------------------

st.title("AI Resume Builder 🚀")

name = st.text_input("Name")
education = st.text_input("Education")
skills = st.text_input("Skills (comma separated)")
projects = st.text_area("Projects")
experience = st.text_area("Experience")
certifications = st.text_area("Certifications")
links = st.text_area("Links (Email | Phone | LinkedIn etc.)")
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

    with st.spinner("Generating Resume..."):
        resume_text = generate_resume(data)

        st.subheader("📄 Resume Preview")
        st.text(resume_text)

        pdf_file = create_pdf(resume_text)

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Download Resume PDF",
                data=f,
                file_name="resume.pdf",
                mime="application/pdf"
            )
