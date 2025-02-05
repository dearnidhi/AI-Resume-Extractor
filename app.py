import streamlit as st
import pandas as pd
from utils import extract_cv_details
from model import match_jd_to_cv, summarize_text
from database import insert_to_db, fetch_from_db, save_job_description, save_uploaded_cv

# Main Application
st.title("HR CV Shortlisting Tool")

# Sidebar for Job Description
st.sidebar.header("Job Description")
existing_job_descriptions = fetch_from_db("SELECT * FROM job_descriptions")
job_description_options = [jd[1] for jd in existing_job_descriptions] if existing_job_descriptions else []

# Option to select or enter a job description
job_description_option = st.sidebar.radio("Choose an Option", ["Select an Existing Job Description", "Enter Job Description"])

if job_description_option == "Select an Existing Job Description":
    selected_job_description = st.sidebar.selectbox("Select an Existing Job Description", job_description_options, index=0 if job_description_options else None)
    job_description = selected_job_description if selected_job_description else ""
else:
    job_description = st.sidebar.text_area("Enter Job Description", placeholder="Paste the job description here...")

# Main Content Area
st.header("Upload CVs")
uploaded_files = st.file_uploader("Upload CVs (PDF format, max 25 files)", accept_multiple_files=True, type=["pdf"])

# Process Button
if st.button("Process"):
    if job_description and uploaded_files:
        # Save Job Description to Database
        save_job_description(job_description)

        # Save Uploaded CVs to Database
        for file in uploaded_files:
            save_uploaded_cv(file)

        # Use job description directly (no need to process it)
        processed_jd = job_description

        # Extract Details and Match
        results = []
        for file in uploaded_files:
            try:
                cv_details = extract_cv_details(file)
                match_score = match_jd_to_cv(processed_jd, cv_details['CV Summary'])
                action = "Selected" if match_score >= 50 else "Rejected"
                cv_details['Action'] = action
                cv_details['Match Score'] = match_score  # Add match score to the results
                results.append(cv_details)
            except Exception as e:
                st.error(f"Error processing CV {file.name}: {str(e)}")

        # Create Output Table
        output_table = pd.DataFrame(results)
        st.header("Shortlisted Candidates")

        # Ensure the 'Action' column is present
        if 'Action' not in output_table.columns:
            output_table['Action'] = "N/A"

        # Apply custom styling to the table
        styled_table = (
            output_table.style
            .map(lambda x: 'background-color: lightgreen' if x == "Selected" else ('background-color: lightcoral' if x == "Rejected" else ''), subset=['Action'])
            .set_properties(**{'text-align': 'center'})
            .set_table_styles([{'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('text-align', 'center'), ('padding', '10px')]}])
        )

        st.dataframe(styled_table)

        # Save to Database
        insert_to_db(output_table)

        # Download as Excel
        output_path = "output/shortlisted_candidates.xlsx"
        output_table.to_excel(output_path, index=False)
        st.success("Processing complete. Table saved to Excel.")
        st.download_button("Download Excel", data=open(output_path, "rb"), file_name="shortlisted_candidates.xlsx")
    else:
        st.error("Please provide both Job Description and CVs.")

# Add some styling
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }
    .stTextArea>div>div>textarea {
        width: 100%;
        height: 150px;
        padding: 12px 20px;
        box-sizing: border-box;
        border: 2px solid #ccc;
        border-radius: 4px;
        background-color: #f8f8f8;
        font-size: 16px;
        resize: none;
    }
    .stDataFrame td {
        padding: 10px;
        text-align: center;
    }
    .stDataFrame th {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
