# %%
import os
from openai import OpenAI
import numpy as np
from scipy.spatial.distance import cosine
import logging

# %%
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# %%
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    logging.error('OPENAI_API_KEY environment variable not found.')
    exit(1)

# %%
def get_embedding(client, text, model="text-embedding-ada-002"):
    """Get embedding for the given text using specified model."""
    text = text.replace("\n", " ")
    try:
        return client.embeddings.create(input = text, model=model).data[0].embedding
    except Exception as e:
        logging.error(f"Error in generating embedding: {e}")
        return None

# %%
def cosine_similarity(embedding1, embedding2):
    """Calculate cosine similarity between two embeddings."""
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))


# %%
def rank_resumes(client, job_description, resumes):
    """Rank resumes based on their similarity to the job description."""
    job_embedding = get_embedding(client, job_description)
    if job_embedding is None:
        return []

    scores = []
    for filename, resume in resumes:
        resume_embedding = get_embedding(client, resume)
        if resume_embedding is not None:
            score = cosine_similarity(np.array(job_embedding), np.array(resume_embedding))
            scores.append(((filename, resume), score))

    # Sort based on scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

# %%
# testing of the above functions
# def main():
#     """Main function for testing resume ranking."""
#     # Example Job Description and Resumes for Testing
#     job_description = "Example job description text."
#     resumes = ["Resume 1 text.", "Resume 2 text.", "Resume 3 text."]

#     # Rank the resumes
#     ranked_resumes = rank_resumes(job_description, resumes)
#     for resume, score in ranked_resumes:
#         print(f"Resume: {resume}, Score: {score}")

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#     client = OpenAI()
#     main()


