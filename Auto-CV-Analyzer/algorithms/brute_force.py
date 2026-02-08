import time
from typing import List, Tuple, Dict


def search_pattern(text: str, pattern: str, case_sensitive: bool = False) -> Tuple[List[int], int]:
    if not case_sensitive: # Convert both text and pattern to lower case for case-insensitive search
        text = text.lower()
        pattern = pattern.lower()
    
    positions = []
    comparisons = 0
    n = len(text)
    m = len(pattern)
    
    if m > n or m == 0: # If pattern is longer than text or empty, return no matches
        return positions, comparisons
    
    for i in range(n - m + 1): # Slide pattern over text
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        
        if j == m:  # Pattern found
            positions.append(i)
    
    return positions, comparisons


def analyze_text(text: str, keywords: List[str], case_sensitive: bool = False) -> Dict:
    """
    Analyze text for multiple keywords using brute force algorithm.
    
    Args:
        text: The text to analyze
        keywords: List of keywords to search for
        case_sensitive: Whether to perform case-sensitive search
        
    Returns:
        Dictionary with analysis results
    """
    start_time = time.time()
    
    matched_keywords = []
    missing_keywords = []
    total_comparisons = 0
    keyword_positions = {}
    
    for keyword in keywords: # Search each keyword in the text
        positions, comparisons = search_pattern(text, keyword, case_sensitive)
        total_comparisons += comparisons
        
        if positions:# If keyword is found, record its positions
            matched_keywords.append(keyword)
            keyword_positions[keyword] = len(positions)
        else: # If keyword is not found, record it as missing
            missing_keywords.append(keyword)
    
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    total_keywords = len(keywords)
    relevance_score = (len(matched_keywords) / total_keywords * 100) if total_keywords > 0 else 0
    
    return {
        'algorithm': 'Brute Force',
        'matched_keywords': matched_keywords,
        'missing_keywords': missing_keywords,
        'matches': len(matched_keywords),
        'total_keywords': total_keywords,
        'relevance_score': round(relevance_score, 2),
        'comparisons': total_comparisons,
        'execution_time': round(execution_time, 3),
        'keyword_positions': keyword_positions
    }
