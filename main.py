# %%
# main.py

import logging
import os
from Ingestion_and_cleaning import main
from resume_ranking import rank_resumes
from openai import OpenAI

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
            resumes.append(resume_text)

    # Rank the resumes
    ranked_resumes = rank_resumes(client, job_description, resumes)
    for resume, score in ranked_resumes:
        logging.info(f"Resume: {resume}, Score: {score}")

