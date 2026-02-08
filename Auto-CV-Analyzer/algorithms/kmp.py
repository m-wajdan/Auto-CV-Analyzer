import time
from typing import List, Tuple, Dict


def compute_lps(pattern: str) -> List[int]:
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m: # this loop calculates lps[i] for i = 1 to m-1 which stores the longest prefix suffix values for pattern
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps


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
    
    # Compute LPS array
    lps = compute_lps(pattern)
    
    i = 0  # index for text
    j = 0  # index for pattern
    
    while i < n:    # Slide the pattern over text and compare characters, using LPS to skip unnecessary comparisons
        comparisons += 1
        
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions, comparisons


def analyze_text(text: str, keywords: List[str], case_sensitive: bool = False) -> Dict:
    """
    Analyze text for multiple keywords using KMP algorithm.
    
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
    
    for keyword in keywords:
        positions, comparisons = search_pattern(text, keyword, case_sensitive)
        total_comparisons += comparisons
        
        if positions:
            matched_keywords.append(keyword)
            keyword_positions[keyword] = len(positions)
        else:
            missing_keywords.append(keyword)
    
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    total_keywords = len(keywords)
    relevance_score = (len(matched_keywords) / total_keywords * 100) if total_keywords > 0 else 0
    
    return {
        'algorithm': 'KMP',
        'matched_keywords': matched_keywords,
        'missing_keywords': missing_keywords,
        'matches': len(matched_keywords),
        'total_keywords': total_keywords,
        'relevance_score': round(relevance_score, 2),
        'comparisons': total_comparisons,
        'execution_time': round(execution_time, 3),
        'keyword_positions': keyword_positions
    }
