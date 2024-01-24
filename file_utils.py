import os
import logging

def create_directory(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")

def read_file(file_path):
    """Read the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_text_file(text, file_path):
    """Save text to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
        logging.info(f"Saved text file {file_path}")
