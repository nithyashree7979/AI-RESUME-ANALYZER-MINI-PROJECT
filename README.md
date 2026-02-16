📄 AI Resume Analyzer

AI Resume Analyzer is a Streamlit-based web application that uses OpenAI NLP to analyze resumes and provide intelligent feedback.
The system extracts text from uploaded resumes and generates insights such as summary, strengths, weaknesses, improvement suggestions, and a resume score breakdown.

This project helps job seekers improve their resumes using AI-driven analysis.

🎯 Objective

The objective of this project is to build an AI-powered application that:
Analyzes resumes automatically
Extracts key skills and important information
Identifies strengths and weaknesses
Suggests improvements to enhance resume quality
Generates a resume score based on multiple parameters

🚀 Features

1. Upload resume in PDF or TXT format
2. Automatic text extraction using PyPDF2
3. AI-based resume summary
4. Skills identification
5. Strengths and weaknesses analysis
6. Resume improvement suggestions
7. Resume score breakdown
8. Simple and user-friendly Streamlit interface


📊 Resume Score Breakdown

The system evaluates resumes using the following metrics:
Skills Score – Based on detected technical and domain skills
Formatting Score – Checks structure and readability
Length Score – Evaluates resume length suitability
Keyword Match – Compares found keywords with required keywords


⚙️ Installation & Setup

1.Clone the repository

git clone https://github.com/nithyashree7979/AI-RESUME-ANALYZER-MINI-PROJECT.git
cd AI-RESUME-ANALYZER-MINI-PROJECT

2.Create virtual environment

python -m venv venv
venv\Scripts\activate

3.Install dependencies

pip install -r requirements.txt

4.Add OpenAI API Key

OPENAI_API_KEY=your_api_key_here

5.Run the application

streamlit run app.py

🛠️ Tech Stack

Python
Streamlit
OpenAI API
PyPDF2
python-dotenv


🧠 How It Works

1. User uploads a resume (PDF/TXT)
2. Text is extracted using PyPDF2
3. Resume content is sent to OpenAI API
4. The AI analyzes the resume and returns:Summary
 Extracted skills
 Strengths
 Weaknesses
 Improvement suggestions
 Resume score breakdown


📸 Output

The application displays:
Resume summary
Skills found in the resume
Strength areas
Areas to improve
Resume score metrics

🔐 Security Note

The OpenAI API key is stored in a .env file and is not uploaded to GitHub to maintain security.

Nithyashree CP
AI Resume Analyzer – Mini Project
