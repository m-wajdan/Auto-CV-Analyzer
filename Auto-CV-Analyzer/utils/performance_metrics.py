"""
Performance metrics tracking for algorithm comparison.
"""

from typing import List, Dict
import pandas as pd


def calculate_efficiency(comparisons: int, text_length: int) -> float:
    """
    Calculate efficiency as comparisons per character.
    
    Args:
        comparisons: Number of comparisons made
        text_length: Length of text analyzed
        
    Returns:
        Efficiency metric
    """
    if text_length == 0:
        return 0
    return round(comparisons / text_length, 4)


def compare_algorithms(results: List[Dict]) -> pd.DataFrame:
    """
    Compare results from multiple algorithms.
    
    Args:
        results: List of result dictionaries from algorithms
        
    Returns:
        DataFrame with comparison metrics
    """
    comparison_data = []
    
    for result in results:
        comparison_data.append({
            'Algorithm': result.get('algorithm', 'Unknown'),
            'Matches': result.get('matches', 0),
            'Relevance Score (%)': result.get('relevance_score', 0),
            'Execution Time (ms)': result.get('execution_time', 0),
            'Comparisons': result.get('comparisons', 0)
        })
    
    return pd.DataFrame(comparison_data)


def aggregate_results(cv_results: Dict[str, List[Dict]]) -> pd.DataFrame:
    """
    Aggregate results from all CVs and algorithms.
    
    Args:
        cv_results: Dictionary mapping CV filenames to list of algorithm results
        
    Returns:
        DataFrame with aggregated results
    """
    all_results = []
    
    for cv_file, results in cv_results.items():
        for result in results:
            all_results.append({
                'CV File': cv_file,
                'Algorithm': result.get('algorithm', 'Unknown'),
                'Matches': result.get('matches', 0),
                'Total Keywords': result.get('total_keywords', 0),
                'Relevance Score (%)': result.get('relevance_score', 0),
                'Execution Time (ms)': result.get('execution_time', 0),
                'Comparisons': result.get('comparisons', 0),
                'Matched Keywords': ', '.join(result.get('matched_keywords', [])),
                'Missing Keywords': ', '.join(result.get('missing_keywords', []))
            })
    
    return pd.DataFrame(all_results)


def get_best_algorithm(results: List[Dict], criterion: str = 'time') -> str:
    """
    Determine the best performing algorithm based on a criterion.
    
    Args:
        results: List of result dictionaries from algorithms
        criterion: Criterion for comparison ('time', 'comparisons', 'score')
        
    Returns:
        Name of the best algorithm
    """
    if not results:
        return "No algorithms compared"
    
    if criterion == 'time':
        best = min(results, key=lambda x: x.get('execution_time', float('inf')))
        return f"{best.get('algorithm', 'Unknown')} (fastest: {best.get('execution_time', 0):.3f} ms)"
    
    elif criterion == 'comparisons':
        best = min(results, key=lambda x: x.get('comparisons', float('inf')))
        return f"{best.get('algorithm', 'Unknown')} (most efficient: {best.get('comparisons', 0)} comparisons)"
    
    elif criterion == 'score':
        best = max(results, key=lambda x: x.get('relevance_score', 0))
        return f"{best.get('algorithm', 'Unknown')} (highest score: {best.get('relevance_score', 0):.2f}%)"
    
    return "Unknown criterion"


def get_performance_summary(results: List[Dict]) -> Dict:
    """
    Get summary statistics for algorithm performance.
    
    Args:
        results: List of result dictionaries from algorithms
        
    Returns:
        Dictionary with summary statistics
    """
    if not results:
        return {}
    
    total_time = sum(r.get('execution_time', 0) for r in results)
    total_comparisons = sum(r.get('comparisons', 0) for r in results)
    avg_score = sum(r.get('relevance_score', 0) for r in results) / len(results)
    
    fastest = min(results, key=lambda x: x.get('execution_time', float('inf')))
    most_efficient = min(results, key=lambda x: x.get('comparisons', float('inf')))
    highest_score = max(results, key=lambda x: x.get('relevance_score', 0))
    
    return {
        'total_algorithms': len(results),
        'total_time': round(total_time, 3),
        'total_comparisons': total_comparisons,
        'average_score': round(avg_score, 2),
        'fastest_algorithm': fastest.get('algorithm', 'Unknown'),
        'fastest_time': round(fastest.get('execution_time', 0), 3),
        'most_efficient_algorithm': most_efficient.get('algorithm', 'Unknown'),
        'most_efficient_comparisons': most_efficient.get('comparisons', 0),
        'highest_score_algorithm': highest_score.get('algorithm', 'Unknown'),
        'highest_score_value': round(highest_score.get('relevance_score', 0), 2)
    }


def calculate_speedup(baseline_time: float, optimized_time: float) -> float:
    """
    Calculate speedup factor between two algorithms.
    
    Args:
        baseline_time: Execution time of baseline algorithm
        optimized_time: Execution time of optimized algorithm
        
    Returns:
        Speedup factor
    """
    if optimized_time == 0:
        return 0
    return round(baseline_time / optimized_time, 2)


def rank_cvs_by_relevance(cv_results: Dict[str, List[Dict]], algorithm: str = None) -> List[tuple]:
    """
    Rank CVs by relevance score for a specific algorithm or average across all.
    
    Args:
        cv_results: Dictionary mapping CV filenames to list of algorithm results
        algorithm: Specific algorithm to rank by (None for average)
        
    Returns:
        List of (cv_file, score) tuples sorted by score descending
    """
    rankings = []
    
    for cv_file, results in cv_results.items():
        if algorithm:
            # Find result for specific algorithm
            algo_result = next((r for r in results if r.get('algorithm') == algorithm), None)
            if algo_result:
                score = algo_result.get('relevance_score', 0)
                rankings.append((cv_file, score))
        else:
            # Calculate average score across all algorithms
            if results:
                avg_score = sum(r.get('relevance_score', 0) for r in results) / len(results)
                rankings.append((cv_file, avg_score))
    
    # Sort by score descending
    rankings.sort(key=lambda x: x[1], reverse=True)
    
    return rankings
