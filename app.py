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
You are a professional resume writer.

Generate a resume EXACTLY in this structure:

Name
Email | Phone | Location | LinkedIn | GitHub

--------------------------------------------------

CAREER OBJECTIVE:
(4-5 lines)

--------------------------------------------------

PROFESSIONAL TRAINING
Role
Company | Duration | Location
• Bullet points (5–6)

--------------------------------------------------

EDUCATION
Degree,
College, Location

--------------------------------------------------

TECHNICAL SKILLS

Agentic AI & LLM Development:
(list in line format)

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
• Description lines (5–6 points)

--------------------------------------------------

CERTIFICATES
• List

--------------------------------------------------

LANGUAGES
List in simple format (NO bullet, NO bold)

--------------------------------------------------

RULES:
- DO NOT use ** or markdown
- Keep spacing clean
- Do NOT mix sections
- Follow EXACT headings
- Keep formatting structured

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
# PDF FUNCTION
# -------------------------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors


def create_pdf(text, filename="resume.pdf"):

    doc = SimpleDocTemplate(filename)

    name_style = ParagraphStyle(name="Name", fontSize=18, spaceAfter=10)
    heading_style = ParagraphStyle(name="Heading", fontSize=12, spaceBefore=10)
    normal_style = ParagraphStyle(name="Normal", fontSize=10, leading=14)

    content = []
    lines = text.split("\n")

    for i, line in enumerate(lines):

        line = line.strip().replace("**", "")

        if not line:
            content.append(Spacer(1, 6))
            continue

        # NAME
        if i == 0:
            content.append(Paragraph(f"<b>{line}</b>", name_style))
            continue

        # SECTION HEADINGS
        if line.isupper() or line.endswith(":"):
            content.append(Paragraph(f"<b>{line}</b>", heading_style))
            content.append(
                HRFlowable(width="100%", thickness=1.5, color=colors.black)
            )
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
