import json
import os
import nltk
from scripts.similarity.get_score import get_score
from scripts.utils import get_filenames_from_dir

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

def read_json(filename):
    """Reads a JSON file and returns its content as a dictionary."""
    with open(filename) as f:
        return json.load(f)

def get_matching_score(resume_path, jd_path):
    """
    Computes the similarity score between a resume and a job description.
    
    Args:
        resume_path (str): Path to the processed resume JSON file.
        jd_path (str): Path to the processed job description JSON file.
    
    Returns:
        float: Similarity score between resume and job description (0-100).
    """
    resume_data = read_json(resume_path)
    jd_data = read_json(jd_path)
    
    resume_string = " ".join(resume_data["extracted_keywords"])
    jd_string = " ".join(jd_data["extracted_keywords"])
    
    result = get_score(resume_string, jd_string)
    return round(result[0].score * 100, 2)

# Main Execution
if __name__ == "__main__":
    resumes_dir = "Data/Processed/Resumes"
    jds_dir = "Data/Processed/JobDescription"
    
    resume_files = get_filenames_from_dir(resumes_dir)
    jd_files = get_filenames_from_dir(jds_dir)

    if not resume_files:
        print("No resumes found.")
        exit()

    if not jd_files:
        print("No job description found.")
        exit()

    # Assume only ONE job description exists (pick the first one)
    jd_filename = jd_files[0]
    jd_path = os.path.join(jds_dir, jd_filename)

    scores = []
    
    for resume_file in resume_files:
        resume_path = os.path.join(resumes_dir, resume_file)
        score = get_matching_score(resume_path, jd_path)
        scores.append((resume_file, score))

    # Sort resumes by similarity score in descending order
    ranked_resumes = sorted(scores, key=lambda x: x[1], reverse=True)

    print(f"\n📄 Job Description Used: {jd_filename}\n")
    print("📊 Ranking of Resumes Based on Similarity Score:\n")
    for rank, (resume_file, score) in enumerate(ranked_resumes, 1):
        print(f"{rank}. {resume_file} - {score}% match")
