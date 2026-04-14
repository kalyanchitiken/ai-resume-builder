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

Generate resume in EXACT CLEAN FORMAT.

IMPORTANT RULES:
- ONLY main headings should be bold
- Sub-sections should NOT be bold
- Keep everything aligned clean
- Skills should NOT break into multiple lines randomly
- No unnecessary spacing
- No markdown symbols like **

FORMAT:

Name (BIG)

Email | Phone | Location | LinkedIn | GitHub

--------------------------------------------------

CAREER OBJECTIVE:
(4 lines clean paragraph)

--------------------------------------------------

PROFESSIONAL TRAINING
Role
Company | Duration | Location
• Bullet points (5–6)

--------------------------------------------------

EDUCATION
Degree
College

--------------------------------------------------

TECHNICAL SKILLS

Agentic AI & LLM Development:
LangChain, LangGraph, RAG, SQL

Deep Learning:
TensorFlow, Pandas

Machine Learning:
Random Forest, LSTM

Programming Data Analysis & Libraries:
Python, R

Chatbot & LLM Development:
RAG, FAISS

Core Concepts:
Generative AI, NLP

Natural Language Processing (NLP):
Text classification, Sentiment analysis

Tools & Platforms:
GitHub, Jupyter Notebook

--------------------------------------------------

PROJECTS

Project Name
• Bullet points (clean, 5 lines max)

--------------------------------------------------

CERTIFICATES
• List

--------------------------------------------------

LANGUAGES
English, Hindi, Telugu

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
# PDF FUNCTION
# -------------------------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors


def create_pdf(text, filename="resume.pdf"):

    doc = SimpleDocTemplate(filename)

    name_style = ParagraphStyle(
        name="Name",
        fontSize=18,
        spaceAfter=6
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
            content.append(Spacer(1, 5))
            continue

        # NAME
        if i == 0:
            content.append(Paragraph(f"<b>{line}</b>", name_style))
            continue

        # MAIN HEADINGS ONLY
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

        # NORMAL TEXT (NO EXTRA BOLD)
        content.append(Paragraph(line, normal_style))

    doc.build(content)

    return filename
