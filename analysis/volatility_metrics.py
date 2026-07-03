import pandas as pd

def calculate_flicker_rate(df: pd.DataFrame) -> float:
    """
    Calculate % of times the #1 cited source changes day-over-day for a query.
    """
    flicker_count = 0
    total_transitions = 0
    
    grouped = df.groupby(['query', 'model'])
    
    for name, group in grouped:
        group = group.sort_values('timestamp')
        sources = group['top_source'].tolist()
        
        for i in range(1, len(sources)):
            total_transitions += 1
            if sources[i] != sources[i-1]:
                flicker_count += 1
                
    return (flicker_count / total_transitions) * 100 if total_transitions > 0 else 0

def calculate_stability_index(df: pd.DataFrame, window_days=30) -> pd.DataFrame:
    """
    Citation Stability Score: % of days a source appears for a query.
    """
    # Implementation details...
    pass