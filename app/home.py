def load_data():
    """Safely load metrics CSV, handling missing/empty/corrupt files."""
    if not METRICS_PATH.exists():
        st.warning("⚠️ No data file found. The GitHub Action collector hasn't run yet.")
        return pd.DataFrame(columns=['date', 'model', 'flicker_rate', 'authority_score', 'citation_count'])
    
    try:
        # Check file size first - empty files are 0 bytes
        if METRICS_PATH.stat().st_size == 0:
            st.warning("⚠️ Data file exists but is empty. The collector ran but produced no results.")
            return pd.DataFrame(columns=['date', 'model', 'flicker_rate', 'authority_score', 'citation_count'])
        
        df = pd.read_csv(METRICS_PATH)
        
        # Verify required columns exist
        required_cols = ['date', 'model']
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            st.error(f"Data file is malformed. Missing columns: {missing}")
            return pd.DataFrame()
            
        return df
        
    except pd.errors.EmptyDataError:
        st.warning("⚠️ Data file is empty. Waiting for successful collection cycle...")
        return pd.DataFrame(columns=['date', 'model', 'flicker_rate', 'authority_score', 'citation_count'])
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return pd.DataFrame()
