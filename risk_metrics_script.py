import sqlite3
import numpy as np
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('mutual_fund_analytics.db')

# 1. Load NAV history joined with fund master details
query = """
    SELECT n.amfi_code, f.scheme_name, n.date, n.nav
    FROM fact_nav n
    JOIN dim_fund f ON n.amfi_code = f.amfi_code
    ORDER BY n.amfi_code, n.date;
"""
df = pd.read_sql(query, con=conn)
conn.close()

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# 2. Calculate daily returns for each scheme
df['daily_return'] = df.groupby('amfi_code')['nav'].pct_change()

# 3. Calculate Risk & Performance Metrics per scheme
risk_metrics = []

for amfi_code, group in df.groupby('amfi_code'):
  scheme_name = group['scheme_name'].iloc[0]
  returns = group['daily_return'].dropna()

  if len(returns) > 10:  # Ensure enough data points
    # Annualized Return (assuming 252 trading days)
    ann_return = returns.mean() * 252

    # Annualized Volatility (Standard Deviation)
    ann_volatility = returns.std() * np.sqrt(252)

    # Sharpe Ratio (Assuming a risk-free rate of ~6% or 0.06)
    risk_free_rate = 0.06
    sharpe_ratio = (
        (ann_return - risk_free_rate) / ann_volatility
        if ann_volatility > 0
        else 0
    )

    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    risk_metrics.append({
        'amfi_code': amfi_code,
        'scheme_name': scheme_name,
        'annualized_return': ann_return,
        'annualized_volatility': ann_volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
    })

df_metrics = pd.DataFrame(risk_metrics)

# Sort by Sharpe Ratio descending to find top performing funds
df_metrics = df_metrics.sort_values(by='sharpe_ratio', ascending=False)

print('--- Top Funds by Sharpe Ratio ---')
print(
    df_metrics[
        [
            'scheme_name',
            'annualized_return',
            'sharpe_ratio',
            'max_drawdown',
        ]
    ].head(5)
)

# 4. Save results to CSV (fulfilling project deliverables)
df_metrics.to_csv('fund_sharpe_ranks.csv', index=False)
print(
    "\nSuccessfully saved risk metrics and rankings to 'fund_sharpe_ranks.csv'!"
)
