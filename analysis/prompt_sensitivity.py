import pandas as pd
from itertools import combinations
from src.utils.db_manager import load_data

def calculate_prompt_sensitivity_index(df: pd.DataFrame = None) -> pd.DataFrame:
    """
    PSI = Average Jaccard distance between source sets 
    for different prompt types on the same query/model.
    Higher PSI = More sensitive to prompt changes.
    """
    if df is None:
        df = load_data()
    
    results = []
    grouped = df.groupby(['model', 'query'])
    
    for (model, query), group in grouped:
        prompt_groups = group.groupby('prompt_type')['source_domain'].apply(set)
        
        if len(prompt_groups) < 2:
            continue
            
        distances = []
        for (p1, s1), (p2, s2) in combinations(prompt_groups.items(), 2):
            # Jaccard distance: 1 - (intersection / union)
            intersection = len(s1 & s2)
            union = len(s1 | s2)
            jaccard_dist = 1 - (intersection / union) if union > 0 else 1
            distances.append(jaccard_dist)
        
        avg_psi = sum(distances) / len(distances) if distances else 0
        results.append({
            'model': model,
            'query': query,
            'prompt_sensitivity_index': round(avg_psi, 3),
            'prompt_types_tested': len(prompt_groups)
        })
    
    return pd.DataFrame(results)