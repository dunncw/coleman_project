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

## Results:
1. Share a description of the data cleaning/preparation that you needed to do.<br>
My data cleaning process was a rather simple one. i am sure that are alot more things that can be done to optimize the unstructered data found in the resumes. I started by gathering some libs to help me convert all the resumes into raw text files. and this was the extent of my datacleaning. the raw text files can be found in ```data/resumes_cleaned/```.
2. Share a vector of 20 similarity scores for the resumes.<br>
The 20 similarity scores can be found in ```data/ranked_resumes.txt```. Again this process could be improved in a couple ways by batching all the API calls together and using a more efficient way to store the data. I chose to use a txt file for simplicity as this is a small project.
3. Share the summary created by GPT for each of the top 3 candidates matching the Job
Description. <br>
each candidate summary can be found in ```data/top_candidate_summaries```. There is alot of improvements that can be make to this portion of the code. subprompting to give the model more grounding and tokens to 'think' would be one improvement. Other futher imporvements could include making more effecitent batch calls, further utilizing chat functionaly to give example summarys for the model to do some incontext learning form. more prompt engineering to give the model more context and grounding.
