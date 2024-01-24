import os
import logging
from openai import OpenAI
import numpy as np
from scipy.spatial.distance import cosine
from file_utils import create_directory

# Consider moving the logging configuration to the main module or a dedicated logging configuration module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure the API key is loaded and validated in the main module or via environment variables
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    logging.error('OPENAI_API_KEY environment variable not found.')
    exit(1)

def get_embedding(client, text, model="text-embedding-ada-002"):
    """
    Get embedding for the given text using the specified model.
    
    Parameters:
    client (OpenAI): The OpenAI client.
    text (str): The text to get embedding for.
    model (str): The model to use for embedding.

    Returns:
    list: The embedding of the text, or None if an error occurs.
    """
    try:
        text = text.replace("\n", " ")  # Ensure newlines don't affect embedding generation
        return client.embeddings.create(input=text, model=model).data[0].embedding
    except Exception as e:
        logging.error(f"Error in generating embedding: {e}")
        return None

def cosine_similarity(embedding1, embedding2):
    """
    Calculate cosine similarity between two embeddings.
    
    Parameters:
    embedding1, embedding2 (list): Embeddings to compare.

    Returns:
    float: Cosine similarity score.
    """
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def rank_resumes(client, job_description, resumes, embeddings_dir):
    """
    Rank resumes based on their similarity to the job description.
    
    Parameters:
    client (OpenAI): The OpenAI client.
    job_description (str): The job description text.
    resumes (list): List of tuples (filename, resume_text).
    embeddings_dir (str): Directory to store embeddings.

    Returns:
    list: Sorted list of tuples ((filename, resume_text), score).
    """
    job_embedding = get_embedding(client, job_description)
    if job_embedding is None:
        logging.error("Failed to generate job description embedding.")
        return []

    create_directory(embeddings_dir)
    np.save(os.path.join(embeddings_dir, 'job_description.npy'), job_embedding)

    ranked_resumes = []
    for filename, resume in resumes:
        resume_embedding = get_embedding(client, resume)
        if resume_embedding:
            score = cosine_similarity(np.array(job_embedding), np.array(resume_embedding))
            ranked_resumes.append(((filename, resume), score))
            np.save(os.path.join(embeddings_dir, f'{filename}.npy'), resume_embedding)

    ranked_resumes.sort(key=lambda x: x[1], reverse=True)
    return ranked_resumes
