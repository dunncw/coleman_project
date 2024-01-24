# %%
import os 
import logging
from doc2docx import convert
import docxpy
import PyPDF4

# %%
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# %%
def create_directory(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")

# %%
def convert_doc_to_docx(doc_path, docx_path):
    """Convert a .doc file to .docx format."""
    try:
        convert(doc_path, docx_path)
        logging.info(f"Converted {doc_path} to {docx_path}")
    except Exception as e:
        logging.error(f"Error converting {doc_path}: {e}")

# %%
def extract_text_from_docx(docx_path):
    """Extract text from a .docx file."""
    try:
        text = docxpy.process(docx_path)
        logging.info(f"Extracted text from {docx_path}")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from {docx_path}: {e}")
        return None

# %%
def extract_text_from_pdf(pdf_path):
    """Extract text from a .pdf file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF4.PdfFileReader(file)
            text = ''
            for page_num in range(reader.numPages):
                text += reader.getPage(page_num).extractText()
        logging.info(f"Extracted text from {pdf_path}")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from {pdf_path}: {e}")
        return None

# %%
def save_text_file(text, file_path):
    """Save text to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
        logging.info(f"Saved text file {file_path}")

# %%
def process_files(source_dir, target_dir):
    """Process all files in the source directory and save them as text files in the target directory."""
    for filename in os.listdir(source_dir):
        base, ext = os.path.splitext(filename)
        source_path = os.path.join(source_dir, filename)

        if ext.lower() == '.doc':
            docx_filename = base + '.docx'
            docx_path = os.path.join(source_dir, docx_filename)
            convert_doc_to_docx(source_path, docx_path)
            source_path = docx_path
            ext = '.docx'

        if ext.lower() in ['.docx', '.pdf']:
            if ext.lower() == '.docx':
                text = extract_text_from_docx(source_path)
            else:
                text = extract_text_from_pdf(source_path)

            if text:
                text_file_path = os.path.join(target_dir, base + '.txt')
                save_text_file(text, text_file_path)

# %%
def main(resume_dir, jd_dir, resumes_cleaned_dir, jd_cleaned_dir):
    # Create necessary directories
    create_directory(resumes_cleaned_dir)
    create_directory(jd_cleaned_dir)

    # Process resumes and job description
    process_files(resume_dir, resumes_cleaned_dir)
    process_files(jd_dir, jd_cleaned_dir)


