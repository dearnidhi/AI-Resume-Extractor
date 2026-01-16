# AI-Resume-Extractor
# 🧑‍💼 HR CV Shortlisting Tool

## 📌 Overview

The **HR CV Shortlisting Tool** is an AI-powered web application designed to help recruiters and HR teams automatically screen resumes against job descriptions.

The system extracts relevant information from uploaded CVs, compares them with a provided job description, calculates a match score, and classifies candidates as **Selected** or **Rejected**. All results are stored in a database and can be downloaded as an Excel file for further analysis.

---

## ✨ Features

- 📄 Upload multiple CVs (PDF format)
- 📝 Enter or select existing job descriptions
- 🧠 AI-based CV and Job Description matching
- 📊 Match score calculation for each candidate
- ✅ Automatic shortlisting (Selected / Rejected)
- 💾 Store job descriptions and CVs in a database
- 📥 Download shortlisted results as Excel
- 🎨 Clean, styled Streamlit UI

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Pandas  
- NLP / Text Similarity Models  
- SQLite / Database Integration  
- PDF Processing  

---

## 📂 Project Structure

```text
├── app.py                 # Main Streamlit application
├── utils.py               # CV text extraction logic
├── model.py               # Matching & summarization logic
├── database.py            # Database operations
├── requirements.txt       # Project dependencies
├── output/
│   └── shortlisted_candidates.xlsx
└── README.md

▶️ Installation & Setup
Prerequisites
Python 3.9+
pip

Virtual environment (recommended)

1️⃣ Clone the Repository
git clone https://github.com/your-username/hr-cv-shortlisting-tool.git
cd hr-cv-shortlisting-tool

2️⃣ Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

▶️ Run the Application
streamlit run app.py

The application will be available at:
http://localhost:8501

🧪 How It Works

Upload multiple CVs in PDF format
Enter a new job description or select an existing one
Click Process

The system:
Extracts CV content
Matches CVs with the job description
Calculates match scores
Shortlists candidates automatically
Results are displayed in a styled table and saved to Excel

⚠️ Notes

Intended for recruitment automation and demos
Match score threshold is configurable in code
Output quality depends on CV text quality
Not optimized for very large datasets
