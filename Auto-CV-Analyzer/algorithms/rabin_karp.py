import time
from typing import List, Tuple, Dict


def search_pattern(text: str, pattern: str, case_sensitive: bool = False, prime: int = 101) -> Tuple[List[int], int]:
    if not case_sensitive: # Convert both text and pattern to lower case for case-insensitive search
        text = text.lower()
        pattern = pattern.lower()
    
    positions = []
    comparisons = 0
    n = len(text)
    m = len(pattern)
    
    if m > n or m == 0: # If pattern is longer than text or empty, return no matches
        return positions, comparisons
    
    # Base for hash calculation (256 for extended ASCII)
    d = 256 
    
    # Calculate hash value for pattern and first window of text
    pattern_hash = 0
    text_hash = 0
    h = 1
    
    # Calculate h = d^(m-1) % prime
    for i in range(m - 1):
        h = (h * d) % prime
    
    # Calculate initial hash values
    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % prime
        text_hash = (d * text_hash + ord(text[i])) % prime
    
    # Slide the pattern over text
    for i in range(n - m + 1):
        comparisons += 1  # Hash comparison
        
        # If hash values match, check character by character
        if pattern_hash == text_hash:
            match = True
            for j in range(m):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    match = False
                    break
            
            if match:
                positions.append(i)
        
        # Calculate hash for next window
        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            
            # Handle negative hash
            if text_hash < 0:
                text_hash += prime
    
    return positions, comparisons


def analyze_text(text: str, keywords: List[str], case_sensitive: bool = False) -> Dict:
    """
    Analyze text for multiple keywords using Rabin-Karp algorithm.
    
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
        'algorithm': 'Rabin-Karp',
        'matched_keywords': matched_keywords,
        'missing_keywords': missing_keywords,
        'matches': len(matched_keywords),
        'total_keywords': total_keywords,
        'relevance_score': round(relevance_score, 2),
        'comparisons': total_comparisons,
        'execution_time': round(execution_time, 3),
        'keyword_positions': keyword_positions
    }
