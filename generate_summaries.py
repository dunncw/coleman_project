# generate_summaries.py

import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import openai

def generate_candidate_summary(job_description, candidate_name, candidate_resume, output_dir):
    """Generate a summary for a given candidate."""
    # Setup OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not found.")

    client = openai.Client(api_key=api_key)

    model = ChatOpenAI(model="gpt-4")
    output_parser = StrOutputParser()

    task_and_documents = ChatPromptTemplate.from_template(
        "Generate a short summary for the top candidates who fit best the job description. "
        "The summary should highlight the reasoning for their fit. "
        "Here is a copy of the job description '''{job_description}''' and "
        "here is a copy of the {candidate_name} resume '''{candidate_resume}'''. "
        "Think step by step and explain your reasoning."
    )

    chain = task_and_documents | model | output_parser

    summary = chain.invoke({
        'candidate_name': candidate_name, 
        'candidate_resume': candidate_resume, 
        'job_description': job_description
    })

    # Write summary to a file
    output_path = os.path.join(output_dir, f"{candidate_name}_summary.txt")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(summary)

    return output_path
