# %%
# main.py

import logging
import os
from openai import OpenAI

from Ingestion_and_cleaning import main
from resume_ranking import rank_resumes
from generate_summaries import generate_candidate_summary


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directories
resume_dir = "data/Resumes"
jd_dir = "data"
resumes_cleaned_dir = "data/resumes_cleaned"
jd_cleaned_dir = "data/jd_cleaned"

api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    logging.error('OPENAI_API_KEY environment variable not found.')
    exit(1)

def read_file(file_path):
    """Read the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_top_candidates(ranked_resumes_file, top_n):
    """Retrieve top N candidates from the ranked resumes file."""
    top_candidates = []
    with open(ranked_resumes_file, 'r') as file:
        for i, line in enumerate(file):
            if i >= top_n:
                break
            parts = line.strip().split(', ')
            resume_file = parts[0].split(': ')[1]
            top_candidates.append(resume_file)
    return top_candidates


if __name__ == "__main__":
    # Ingest and clean the data
    logging.info("Starting data ingestion and cleaning...")
    #main(resume_dir, jd_dir, resumes_cleaned_dir, jd_cleaned_dir)

    # Read the cleaned job description
    logging.info("Ranking resumes...")
    client = OpenAI()
    job_description_path = os.path.join(jd_cleaned_dir, "ML_Engineer_CRG.txt")
    job_description = read_file(job_description_path)

    # Read and process resumes
    resumes = []
    for filename in os.listdir(resumes_cleaned_dir):
        if filename.endswith('.txt'):
            resume_path = os.path.join(resumes_cleaned_dir, filename)
            resume_text = read_file(resume_path)
            resumes.append((filename, resume_text))

    # Rank the resumes
    i = 1
    ranked_resumes = rank_resumes(client, job_description, resumes)
    output_lines = []
    for (filename, resume), score in ranked_resumes:
        # create the output line
        output_line = f"Resume: {filename}, Score: {score}, Rank: {i}"
        output_lines.append(output_line)
        i += 1

    # Save the output lines to a file
    output_file_path = "data/ranked_resumes.txt"
    # Create the directory for the output file if it doesn't exist
    from Ingestion_and_cleaning import save_text_file
    save_text_file("\n".join(output_lines), output_file_path)
    logging.info(f"Saved ranked resumes to {output_file_path}")

    # Generate summaries for top candidates
    top_candidates = get_top_candidates("data/ranked_resumes.txt", 3)
    job_description = read_file("data/jd_cleaned/ML_Engineer_CRG.txt")
    summaries_dir = "data/top_candidate_summaries"
    os.makedirs(summaries_dir, exist_ok=True)

    for candidate in top_candidates:
        candidate_resume = read_file(f"data/resumes_cleaned/{candidate}")
        summary_path = generate_candidate_summary(job_description, candidate, candidate_resume, summaries_dir)
        logging.info(f"Generated summary for {candidate} at {summary_path}")


