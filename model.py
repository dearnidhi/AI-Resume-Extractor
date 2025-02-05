from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import torch

# Check device availability (GPU or CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize the SentenceTransformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

# Initialize the Hugging Face pipeline for summarization (use CPU if GPU is unavailable)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1 if torch.cuda.is_available() else -1)

def match_jd_to_cv(jd, cv_details):
    """
    Match the Job Description (JD) with CV details based on cosine similarity.
    """
    if isinstance(cv_details, str):
        cv_summary = cv_details  # If cv_details is just a string, use it directly
    elif isinstance(cv_details, dict):
        cv_summary = cv_details.get('CV Summary', '')
    else:
        cv_summary = ""

    if not isinstance(cv_summary, str):
        cv_summary = str(cv_summary)

    try:
        jd_embedding = model.encode(jd, convert_to_tensor=True)
        cv_embedding = model.encode(cv_summary, convert_to_tensor=True)
        similarity_score = util.cos_sim(jd_embedding, cv_embedding).item() * 100
    except Exception as e:
        similarity_score = 0
        print(f"Error during matching: {str(e)}")

    return similarity_score

def summarize_text(text, max_length=512):
    """
    Summarize the given text using Hugging Face BART summarizer.
    """
    if not text or len(text.strip()) == 0:
        return "No content to summarize."

    if len(text) < 10:
        return "Text too short to summarize."

    # Adjust max_length dynamically to ensure the summary doesn't go beyond the model's limit
    max_summary_length = min(len(text) // 2, 130)  # Limit summary length
    text = text[:max_length]  # Ensure the text fits the model's input size

    try:
        summary = summarizer(text, max_length=max_summary_length, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        return "Error during summarization."
