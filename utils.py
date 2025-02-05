import re
import pdfplumber
import spacy
from transformers import pipeline
from model import summarize_text

# Load spaCy model for entity recognition
nlp = spacy.load("en_core_web_sm")

# Initialize Hugging Face pipelines for skill and education extraction

# Load the NER model
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
education_extraction_model = pipeline("text2text-generation", model="google/flan-t5-base")

def extract_cv_details(file):
    """
    Extract relevant details from the CV PDF.
    """
    try:
        with pdfplumber.open(file) as pdf:
            text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    except Exception as e:
        print(f"Error reading PDF {file.name}: {str(e)}")
        return None  # Skip if file is unreadable

    details = {
        "Candidate name": extract_name(text),
        "Experience": extract_experience(text),
        "Mobile Number": extract_mobile(text),
        "Email": extract_email(text),
        "skills": extract_skills(text),
        "Education": extract_education(text),
        "CV Summary": summarize_text(text),
        "CV Name": file.name
    }
    
    return details

# def extract_name(text):
#     """
#     Extract the candidate's name from the CV.
#     """
#     doc = nlp(text)
#     potential_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    
#     # Rule-based check: Look for keywords like 'Name:', 'Resume of'
#     match = re.search(r'Name[:\-]?\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', text)
    
#     if match:
#         return match.group(1)
    
#     return potential_names[0] if potential_names else "N/A"

def extract_name(text):
    """
    Extract the candidate's name from the CV.
    """
    doc = nlp(text)
    
    # Extract potential names using Named Entity Recognition (NER)
    potential_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    # Rule-based name extraction: Look for patterns like 'Name:', 'Resume of', etc.
    match = re.search(r'(?i)(?:Name[:\-]?\s*|Resume of\s*)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', text)
    
    if match:
        return match.group(1)

    # Fallback: Return the first detected name by spaCy NER
    return potential_names[0] if potential_names else "N/A"



def extract_experience(text):
    """
    Extract the candidate's years of experience from the CV.
    Handles fractional years and 'plus' modifiers.
    """
    # Updated regex pattern to capture fractional years (e.g., "3.5+ years") and similar formats
    match = re.search(r'(\d+(\.\d+)?\s*\+?\s*(?:years?|yrs?|year|experience))', text, re.IGNORECASE)
    
    if match:
        experience = match.group(1).strip()
        # Normalize the experience text by replacing variations (e.g., 'yrs' -> 'years')
        experience = experience.replace("yrs", "years").replace("yr", "year").replace("experience", "years")
        return experience
    else:
        return "N/A"




def extract_mobile(text):
    """
    Extract the candidate's mobile number from the CV.
    """
    # Updated regex pattern to handle various formats and country codes more effectively
    pattern = r'(?:(?:\+91|91|\d{2})[\s-]?)?[\d]{10}'  # Handling +91 or 91 prefix, or just 10 digits
    matches = re.findall(pattern, text)
    return matches[0] if matches else "N/A"


def extract_email(text):
    """
    Extract the candidate's email from the CV.
    """
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "N/A"




def extract_skills(text):
    """
    Extract skills from the CV using pre-trained NER model and dynamic learning.
    """
    # Run NER on the CV text to extract entities
    entities = ner_pipeline(text)
    
    # Filter the skills from the recognized entities
    skills = {ent['word'] for ent in entities if ent['entity_group'] == 'MISC' and not ent['word'].startswith('##')}
    
    # Manually filter out irrelevant or unwanted terms
    irrelevant_terms = {'Data', 'Language', 'Development', 'Tech', 'Testing', 'Control'}
    filtered_skills = [skill for skill in skills if skill not in irrelevant_terms]
    
    # Manually add common skills that might not be detected, including abbreviations
    common_skills = ['Python', 'Java', 'C++', 'SQL', 'Machine Learning', 'AI', 'JavaScript', 'AWS', 'React', 
                     'Node.js', 'Swift', 'Django', 'PostgreSQL', 'Git', 'Jira', 'CSS', 'MySQL', 'Pandas', 'Redux']
    
    # Dynamically add skills that appear in the text, ignoring case
    all_skills = filtered_skills + [skill for skill in common_skills if skill.lower() in text.lower()]
    
    # Remove duplicates and clean up
    unique_skills = list(set(all_skills))

    return unique_skills

# Example CV text
cv_text = """
Experienced in Python, Java, Swift, Typescript, React Native, Redux, ARKit, Firebase, MySQL, Realm, Core Data, 
Git, Jira, AWS, DevOps, Testing, Automation Testing, Manual Testing, Android Developer, and UI/UX Design.
"""

# Extract skills
skills = extract_skills(cv_text)

# Output the result
print("Extracted Skills:", skills)



def extract_education(text):
    """
    Extract the education details from the CV.
    """
    # Regex to extract degree & year
    matches = re.findall(r'(B\.?Tech|M\.?Tech|BSc|MSc|PhD).*?\d{4}', text)
    
    if matches:
        return ", ".join(matches)
    
    # Use LLM if regex fails
    prompt = f"Extract the educational qualifications from this CV: {text[:1000]}"
    education = education_extraction_model(prompt)
    return education[0]['generated_text']
