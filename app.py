import streamlit as st
from langchain_groq import ChatGroq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

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
# 🧹 CLEAN FUNCTION (VERY IMPORTANT)
# -------------------------
def clean_text(text):
    text = text.replace("**", "")
    text = text.replace("* ", "• ")
    text = text.replace("*", "")
    text = text.replace("User Data:", "")
    return text.strip()


# -------------------------
# 🧠 AI FUNCTION
# -------------------------
def generate_resume(data):

    prompt = f"""
You are a professional resume writer.

Generate a clean ATS-friendly resume.

STRICT RULES:
- Do NOT use ** or *
- Do NOT use markdown
- Use only plain text
- Use • for bullets
- Do NOT include "User Data"
- Do NOT repeat input

FORMAT:

Name

Email | Phone | Location | LinkedIn | GitHub

--------------------------------------------------

CAREER OBJECTIVE:
(4–5 lines)

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
Group skills properly

--------------------------------------------------

PROJECTS
Project Name
• Bullet points

--------------------------------------------------

CERTIFICATES
• List

--------------------------------------------------

LANGUAGES
Simple list

--------------------------------------------------

Use this data:

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

    cleaned = clean_text(res.content)

    return cleaned


# -------------------------
# 📄 PDF FUNCTION
# -------------------------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

def create_pdf(text, filename="resume.pdf"):

    doc = SimpleDocTemplate(filename)

    name_style = ParagraphStyle(
        name="Name",
        fontSize=20,
        spaceAfter=10
    )

    contact_style = ParagraphStyle(
        name="Contact",
        fontSize=10,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        name="Heading",
        fontSize=11,
        spaceBefore=10
    )

    normal_style = ParagraphStyle(
        name="Normal",
        fontSize=10,
        leading=14
    )

    content = []
    lines = text.split("\n")

    for i, line in enumerate(lines):

        line = line.strip()

        if not line:
            content.append(Spacer(1, 6))
            continue

        # ✅ NAME (BIG + GAP)
        if i == 0:
            content.append(Paragraph(f"<b>{line}</b>", name_style))
            continue

        # ✅ CONTACT LINE WITH ICONS
        if i == 1:
            line = line.replace("Email:", "📧")
            line = line.replace("Phone:", "📞")
            line = line.replace("Location:", "📍")
            line = line.replace("LinkedIn:", "🔗")
            line = line.replace("GitHub:", "💻")

            content.append(Paragraph(line, contact_style))
            continue

        # ❌ REMOVE EXTRA DASH LINES
        if "-----" in line:
            continue

        # ✅ HEADINGS
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
            content.append(
                HRFlowable(width="100%", thickness=1.2, color=colors.black)
            )
            continue

        content.append(Paragraph(line, normal_style))

    doc.build(content)

    return filename

# -------------------------
# 🎯 STREAMLIT UI
# -------------------------

st.title("AI Resume Builder 🚀")

name = st.text_input("Name")
education = st.text_input("Education")
skills = st.text_input("Skills")
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
