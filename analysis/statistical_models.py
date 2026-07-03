import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from src.utils.db_manager import load_data

def run_regression_analysis():
    df = load_data()
    if df.empty:
        print("No data available for regression analysis.")
        return None

    X = df[['authority_score', 'freshness_days']]
    y = df['position']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    results = {
        "coefficients": dict(zip(['Authority', 'Freshness'], model.coef_)),
        "intercept": model.intercept_,
        "r_squared": model.score(X_scaled, y)
    }
    
    print("Regression Analysis Results:")
    for k, v in results.items():
        print(f"  {k}: {v}")
        
    return results

if __name__ == "__main__":
    run_regression_analysis()
