"""
File reader utilities for extracting text from PDF, DOCX, TXT, and JSON files.
"""

import os
import json
import io
from typing import Optional, Dict
import pdfplumber
import docx2txt


def extract_text_from_pdf(file_path: str = None, file_content: bytes = None) -> str:
    """
    Extract text from PDF file using pdfplumber.
    
    Args:
        file_path: Path to the PDF file
        file_content: Binary content of the PDF file
        
    Returns:
        Extracted text as string
    """
    try:
        text_content = []
        
        if file_content:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
        elif file_path:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
        
        return '\n'.join(text_content).strip()
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


def extract_text_from_docx(file_path: str = None, file_content: bytes = None) -> str:
    """
    Extract text from DOCX file using docx2txt.
    
    Args:
        file_path: Path to the DOCX file
        file_content: Binary content of the DOCX file
        
    Returns:
        Extracted text as string
    """
    try:
        if file_content:
            text = docx2txt.process(io.BytesIO(file_content))
        elif file_path:
            text = docx2txt.process(file_path)
        else:
            return ""
        
        return text.strip()
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"


def extract_text_from_txt(file_path: str = None, file_content: bytes = None) -> str:
    """
    Extract text from TXT file.
    
    Args:
        file_path: Path to the TXT file
        file_content: Binary content of the TXT file
        
    Returns:
        Extracted text as string
    """
    try:
        if file_content:
            text = file_content.decode('utf-8', errors='ignore')
        elif file_path:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        else:
            return ""
        
        return text.strip()
    except Exception as e:
        return f"Error extracting TXT: {str(e)}"


def parse_job_description_txt(text: str) -> tuple:
    """
    Parse job description from TXT format.
    Expected format:
    Line 1: Job Title
    Line 2: Comma-separated skills
    
    Args:
        text: Raw text content
        
    Returns:
        Tuple of (job_title, skills_list)
    """
    lines = text.strip().split('\n')
    
    if len(lines) >= 2:
        job_title = lines[0].strip()
        skills_str = lines[1].strip()
        skills = [s.strip() for s in skills_str.split(',') if s.strip()]
        return job_title, skills
    elif len(lines) == 1:
        # Only job title provided
        return lines[0].strip(), []
    else:
        return "", []


def extract_text_from_json(file_path: str = None, file_content: bytes = None) -> str:
    """
    Extract text from JSON file.
    
    Args:
        file_path: Path to the JSON file
        file_content: Binary content of the JSON file
        
    Returns:
        Extracted text as string (all values concatenated)
    """
    try:
        if file_content:
            data = json.loads(file_content.decode('utf-8'))
        elif file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            return ""
        
        # Extract all text values from JSON recursively
        def extract_values(obj):
            if isinstance(obj, dict):
                return ' '.join(str(v) for v in obj.values() if v)
            elif isinstance(obj, list):
                return ' '.join(extract_values(item) for item in obj)
            else:
                return str(obj) if obj else ''
        
        return extract_values(data).strip()
    except Exception as e:
        return f"Error extracting JSON: {str(e)}"


def read_file(file_path: str = None, file_content: bytes = None, filename: str = None) -> str:
    """
    Read and extract text from file based on extension.
    
    Args:
        file_path: Path to the file
        file_content: Binary content of the file
        filename: Name of the file (to determine type)
        
    Returns:
        Extracted text as string
    """
    # Determine file extension
    if file_path:
        ext = os.path.splitext(file_path)[1].lower()
    elif filename:
        ext = os.path.splitext(filename)[1].lower()
    else:
        return "Error: No file path or filename provided"
    
    # Extract text based on file type
    if ext == '.pdf':
        return extract_text_from_pdf(file_path, file_content)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(file_path, file_content)
    elif ext == '.txt':
        return extract_text_from_txt(file_path, file_content)
    elif ext == '.json':
        return extract_text_from_json(file_path, file_content)
    else:
        return f"Unsupported file format: {ext}"


def load_cvs_from_directory(directory_path: str) -> Dict[str, str]:
    """
    Load all CV files from a directory.
    
    Args:
        directory_path: Path to directory containing CV files
        
    Returns:
        Dictionary mapping filenames to extracted text
    """
    cvs = {}
    
    if not os.path.exists(directory_path):
        return cvs
    
    supported_extensions = ['.pdf', '.docx', '.doc', '.txt', '.json']
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            
            if ext in supported_extensions:
                text = read_file(file_path=file_path)
                if text and not text.startswith("Error"):
                    cvs[filename] = text
    
    return cvs
