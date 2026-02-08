"""
Text cleaning and preprocessing utilities for CV analysis.
"""

import re
from typing import List, Set


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep letters, numbers, and basic punctuation
    text = re.sub(r'[^\w\s\.,;:\-\'\"()]+', ' ', text)
    
    # Remove multiple spaces
    text = ' '.join(text.split())
    
    return text.strip()


def extract_keywords(text: str, delimiter: str = ',') -> List[str]:
    """
    Extract keywords from comma-separated or newline-separated text.
    
    Args:
        text: Text containing keywords
        delimiter: Delimiter used to separate keywords
        
    Returns:
        List of cleaned keywords
    """
    # Try comma separation first
    if delimiter in text:
        keywords = text.split(delimiter)
    # Try newline separation
    elif '\n' in text:
        keywords = text.split('\n')
    # Try semicolon separation
    elif ';' in text:
        keywords = text.split(';')
    else:
        # Single keyword or space-separated
        keywords = [text]
    
    # Clean and filter keywords
    cleaned_keywords = []
    for kw in keywords:
        kw = kw.strip()
        if kw:
            cleaned_keywords.append(kw)
    
    return cleaned_keywords


def normalize_keywords(keywords: List[str]) -> List[str]:
    """
    Normalize keywords by removing duplicates and extra whitespace.
    
    Args:
        keywords: List of keywords
        
    Returns:
        Normalized list of keywords
    """
    normalized = []
    seen = set()
    
    for keyword in keywords:
        # Clean the keyword
        kw = keyword.strip()
        kw_lower = kw.lower()
        
        # Avoid duplicates (case-insensitive check)
        if kw and kw_lower not in seen:
            normalized.append(kw)
            seen.add(kw_lower)
    
    return normalized


def extract_skills_from_job_description(job_text: str) -> List[str]:
    """
    Extract skills/keywords from job description text.
    
    Args:
        job_text: Job description text
        
    Returns:
        List of extracted skills/keywords
    """
    # Common skill-related keywords and phrases
    skill_patterns = [
        r'(?:skills?|requirements?|qualifications?|experience in):?\s*([^\n.]+)',
        r'(?:must have|should have|required):?\s*([^\n.]+)',
        r'(?:knowledge of|proficiency in|expertise in):?\s*([^\n.]+)',
    ]
    
    extracted_skills = []
    
    # Try pattern matching
    for pattern in skill_patterns:
        matches = re.findall(pattern, job_text, re.IGNORECASE)
        for match in matches:
            skills = extract_keywords(match)
            extracted_skills.extend(skills)
    
    # If no patterns match, try to extract from entire text
    if not extracted_skills:
        # Look for common programming languages, tools, and technologies
        common_skills = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'SQL', 'R',
            'Machine Learning', 'Deep Learning', 'Data Analysis', 'Statistics',
            'TensorFlow', 'PyTorch', 'Pandas', 'NumPy', 'Scikit-learn',
            'Git', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask',
            'Excel', 'Tableau', 'Power BI', 'Spark', 'Hadoop',
            'Communication', 'Teamwork', 'Leadership', 'Problem Solving'
        ]
        
        job_text_lower = job_text.lower()
        for skill in common_skills:
            if skill.lower() in job_text_lower:
                extracted_skills.append(skill)
    
    return normalize_keywords(extracted_skills)


def preprocess_for_matching(text: str, remove_numbers: bool = False) -> str:
    """
    Preprocess text for pattern matching.
    
    Args:
        text: Text to preprocess
        remove_numbers: Whether to remove numbers
        
    Returns:
        Preprocessed text
    """
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Optionally remove numbers
    if remove_numbers:
        text = re.sub(r'\d+', '', text)
    
    return text.strip()


def get_word_frequency(text: str, top_n: int = 50) -> List[tuple]:
    """
    Get most frequent words in text.
    
    Args:
        text: Text to analyze
        top_n: Number of top words to return
        
    Returns:
        List of (word, frequency) tuples
    """
    # Tokenize and count words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'should', 'could', 'may', 'might', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which'
    }
    
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Count frequency
    word_freq = {}
    for word in filtered_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_words[:top_n]
