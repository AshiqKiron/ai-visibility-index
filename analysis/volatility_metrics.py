import pandas as pd
from src.utils.db_manager import load_data
from src.utils.config import DATA_DIR

def calculate_and_save_metrics():
    df = load_data()
    if df.empty:
        print("No data to analyze.")
        return

    # 1. Calculate Flicker Rate per Model per Day
    # Logic: Compare top source of Day N vs Day N-1
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_top = df.sort_values('position').drop_duplicates(subset=['model', 'query', 'date'], keep='first')
    
    flicker_data = []
    for (model, query), group in daily_top.groupby(['model', 'query']):
        group = group.sort_values('date')
        sources = group['source_domain'].tolist()
        dates = group['date'].tolist()
        
        for i in range(1, len(sources)):
            flicker = 1 if sources[i] != sources[i-1] else 0
            flicker_data.append({
                'date': dates[i],
                'model': model,
                'query': query,
                'flicked': flicker
            })
            
    df_flicker = pd.DataFrame(flicker_data)
    if not df_flicker.empty:
        daily_flicker_rate = df_flicker.groupby(['date', 'model'])['flicked'].mean().reset_index()
        daily_flicker_rate.rename(columns={'flicked': 'flicker_rate'}, inplace=True)
    else:
        daily_flicker_rate = pd.DataFrame(columns=['date', 'model', 'flicker_rate'])

    # 2. Calculate Authority Correlation
    corr_data = df.groupby(['model', 'source_domain']).agg(
        avg_auth=('authority_score', 'mean'),
        citation_count=('id', 'count')
    ).reset_index()

    # Merge for final summary
    summary = daily_flicker_rate.merge(corr_data, on='model', how='outer')
    
    # Save to CSV for Streamlit
    output_path = DATA_DIR / "processed" / "metrics_summary.csv"
    summary.to_csv(output_path, index=False)
    print(f"Metrics saved to {output_path}")

if __name__ == "__main__":
    calculate_and_save_metrics()