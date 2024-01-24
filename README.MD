# Coleman project

# Resume Ranking Project

This project is designed to ingest and clean resumes and job descriptions, then rank the resumes based on their match to the job requirements using OpenAI's Ada2 model for embeddings.

## Project Structure

- `main.py`: The main script that orchestrates the data ingestion, cleaning, and ranking process.
- `ingestion_and_cleaning.py`: Module for ingesting and cleaning resumes and job descriptions.
- `resume_ranking.py`: Module for generating embeddings and ranking the resumes based on their similarity to the job description.
- `generate_summaries.py`: Script to generate summaries for the top candidates.

## Installation

1. Clone the repository:

2. Navigate to the project directory:
```cd coleman_project```

3. Create a virtual environment (optional):
```python -m venv .venv```
4. Activate the virtual environment:
- On Windows:
  ```
  .venv\Scripts\activate
  ```
- On Linux or macOS:
  ```
  source .venv/bin/activate
  ```

5. Install the required libraries:
  ```
  pip install -r requirements.txt
  ```

## Configuration
Set the OpenAI API key as an environment variable:
- On Windows: set OPENAI_API_KEY=your_api_key
- On Unix or MacOS: export OPENAI_API_KEY=your_api_key

## Usage
1. Place resumes in the ```data/resumes/``` (see project structer) and the job description in ```data/```. Ensure resumes are in either .doc, .docx or .pdf format.
2. Run the main script to start the process: ```python main.py```
3. The script will ingest, clean, and rank the resumes. The results will be logged, showing the ranking of each resume. ```data/ranked_resumes``` will show the results of ranking each resume. the top 3 candidates will have a summary generated for them and saved in ```data/top_candidate_summaries/```.

## Project Structure
- main.py: The main script that orchestrates the whole process.
- ingestion_and_cleaning.py: Module for ingesting and cleaning data.
- resume_ranking.py: Module for generating embeddings and ranking resumes.
- data/: Directory where  job description is stored.
- data/resumes/: Directory where the resumes are stored.
- data/resumes_cleaned/: Directory where cleaned resume data is stored.
- data/jd_cleaned/: Directory where the cleaned job description is stored.
- data/ranked_resumes/: Directory where the ranked resumes are stored.
- data/top_candidate_summaries/: Directory where the summaries are stored.
- data/ranked_resumes.txt: txt file containing the ranked resumes.
- data/embeddings.csv: npy file containing the embeddings for the resumes.