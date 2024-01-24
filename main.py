import logging
import os
from openai import OpenAI

# Importing the new utility modules
from file_utils import read_file, save_text_file, create_directory
from config_utils import read_config
from Ingestion_and_cleaning import main as ingestion_main
from resume_ranking import rank_resumes
from generate_summaries import generate_candidate_summary

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configurations from config.json
config = read_config('config.json')

# Extracting settings from the configuration
resume_dir = config['resume_dir']
jd_dir = config['jd_dir']
resumes_cleaned_dir = config['resumes_cleaned_dir']
jd_cleaned_dir = config['jd_cleaned_dir']
output_dir = config['output_dir']
summaries_dir = config['summaries_dir']

# Check for OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    logging.error('OPENAI_API_KEY environment variable not found.')
    exit(1)

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
    ingestion_main(resume_dir, jd_dir, resumes_cleaned_dir, jd_cleaned_dir)

    # Initialize OpenAI client
    client = OpenAI()

    # Read the cleaned job description
    logging.info("Ranking resumes...")
    job_description_path = os.path.join(jd_cleaned_dir, "ML_Engineer_CRG.txt")
    job_description = read_file(job_description_path)

    # Process resumes
    resumes = [(filename, read_file(os.path.join(resumes_cleaned_dir, filename)))
               for filename in os.listdir(resumes_cleaned_dir) if filename.endswith('.txt')]

    # Rank the resumes
    ranked_resumes = rank_resumes(client, job_description, resumes)

    # Save the ranked resumes
    ranked_resumes_output = "\n".join([f"Resume: {filename}, Score: {score}, Rank: {i+1}" 
                                       for i, ((filename, _), score) in enumerate(ranked_resumes)])
    output_file_path = os.path.join(output_dir, "ranked_resumes.txt")
    save_text_file(ranked_resumes_output, output_file_path)

    # Generate summaries for top candidates
    top_candidates = get_top_candidates(output_file_path, 3)
    for candidate in top_candidates:
        candidate_resume = read_file(os.path.join(resumes_cleaned_dir, candidate))
        summary_path = generate_candidate_summary(job_description, candidate, candidate_resume, summaries_dir)
        logging.info(f"Generated summary for {candidate} at {summary_path}")

    logging.info("Done!")
