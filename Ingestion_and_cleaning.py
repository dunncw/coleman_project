import os
import logging
from doc2docx import convert
import docxpy
import PyPDF4
from file_utils import create_directory, save_text_file

# Setup logging - Consider configuring logging in main or a separate module for better control
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_doc_to_docx(doc_path, docx_path):
    """Convert a .doc file to .docx format."""
    try:
        convert(doc_path, docx_path)
        logging.info(f"Converted {doc_path} to {docx_path}")
    except Exception as e:
        logging.error(f"Error converting {doc_path}: {e}")
        # Rethrow or handle the exception as needed

def extract_text_from_file(file_path):
    """Extract text from a .docx or .pdf file."""
    _, ext = os.path.splitext(file_path)
    try:
        if ext.lower() == '.docx':
            return docxpy.process(file_path)
        elif ext.lower() == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF4.PdfFileReader(file)
                return ''.join([reader.getPage(page_num).extractText() for page_num in range(reader.numPages)])
    except Exception as e:
        logging.error(f"Error extracting text from {file_path}: {e}")
        return None

def process_files(source_dir, target_dir):
    """Process all files in the source directory and save them as text files in the target directory."""
    for filename in os.listdir(source_dir):
        base, ext = os.path.splitext(filename)
        source_path = os.path.join(source_dir, filename)

        if ext.lower() == '.doc':
            docx_path = os.path.join(source_dir, base + '.docx')
            convert_doc_to_docx(source_path, docx_path)
            source_path = docx_path

        if ext.lower() in ['.docx', '.pdf']:
            text = extract_text_from_file(source_path)
            if text:
                text_file_path = os.path.join(target_dir, base + '.txt')
                save_text_file(text, text_file_path)

def main(resume_dir, jd_dir, resumes_cleaned_dir, jd_cleaned_dir):
    create_directory(resumes_cleaned_dir)
    create_directory(jd_cleaned_dir)
    process_files(resume_dir, resumes_cleaned_dir)
    process_files(jd_dir, jd_cleaned_dir)

if __name__ == "__main__":
    # Assuming configuration settings are read and passed here
    config = {} # Replace with actual config read
    main(config['resume_dir'], config['jd_dir'], config['resumes_cleaned_dir'], config['jd_cleaned_dir'])
