import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from src.utils.db_manager import load_data

def run_regression_analysis():
    df = load_data()
    if df.empty:
        return None

    # Prepare features: Authority Score and Freshness
    X = df[['authority_score', 'freshness_days']]
    y = df['position'] # Lower position number is better (1st, 2nd...)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit model
    model = LinearRegression()
    model.fit(X_scaled, y)

    return {
        "coefficients": dict(zip(['Authority', 'Freshness'], model.coef_)),
        "intercept": model.intercept_,
        "r_squared": model.score(X_scaled, y)
    }