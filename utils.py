import io
import re
from openai import OpenAI
from PyPDF2 import PdfReader
import docx
import json


# ----------- PDF TEXT EXTRACTION --------------
def extract_text_from_pdf(file_bytes):
    reader = PdfReader(file_bytes)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# ----------- DOCX TEXT EXTRACTION --------------
def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([p.text for p in doc.paragraphs])


# ----------- KEYWORD + SCORE ANALYSIS ----------
def analyze_resume_text(resume_text, required_keywords):

    txt = resume_text.lower()
    required = [k.lower() for k in required_keywords]
    found = [k for k in required if k in txt]
    missing = [k for k in required if k not in txt]

    length_score = min(max(len(txt.split()) / 400 * 100, 10), 100)
    skills_score = int((len(found) / (len(required) if required else 1)) * 100)

    has_contact = bool(re.search(r"\b(email|@)\b", txt))
    has_section_headers = bool(re.search(r"\b(experience|education|skills|projects)\b", txt))

    formatting_score = 50
    formatting_score += 25 if has_contact else -10
    formatting_score += 25 if has_section_headers else -10
    formatting_score = max(0, min(formatting_score, 100))

    score = int(0.5 * skills_score + 0.3 * formatting_score + 0.2 * length_score)

    breakdown = {
        "skills_score": skills_score,
        "formatting_score": formatting_score,
        "length_score": length_score,
        "found_keywords_count": len(found),
        "required_keywords_count": len(required),
    }

    return {
        "score": score,
        "breakdown": breakdown,
        "keywords_found": found,
        "keywords_missing": missing,
    }


# ----------- AI SUMMARY GENERATOR --------------
def generate_summary_and_structured_json(client: OpenAI, resume_text: str, job_role="", job_description=""):

    # Fallback if no API key
    if client is None:
        txt = resume_text.strip().split("\n")[:12]
        return {
            "summary": [line.strip() for line in txt if line.strip()][:6],
            "strengths": ["Clear technical skills section"],
            "weaknesses": ["Could add more measurable impact (metrics)"],
            "improvements": ["Add achievement numbers", "Tailor skills to job description"],
            "keywords_found": [],
            "keywords_missing": [],
            "rewrite_bullets": [],
        }

    system_msg = (
        "You are a resume review AI. "
        "IMPORTANT: Respond with JSON ONLY — no explanations, no text before/after. "
        "Return exactly this structure:\n"
        "{\n"
        '  "summary": [],\n'
        '  "strengths": [],\n'
        '  "weaknesses": [],\n'
        '  "improvements": [],\n'
        '  "keywords_found": [],\n'
        '  "keywords_missing": [],\n'
        '  "rewrite_bullets": []\n'
        "}"
    )

    user_msg = (
        f"Job Role: {job_role}\n"
        f"Job Description:\n{job_description}\n"
        f"Resume:\n{resume_text}"
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.2,
        max_tokens=800,
    )

    import json, re

    raw = resp.choices[0].message.content


    # ---- FIX: extract the JSON safely even if GPT adds text ----
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass

    # fallback empty JSON
    return {
        "summary": [],
        "strengths": [],
        "weaknesses": [],
        "improvements": [],
        "keywords_found": [],
        "keywords_missing": [],
        "rewrite_bullets": [],
    }
