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

# 2. Calculate daily returns
df['daily_return'] = df.groupby('amfi_code')['nav'].pct_change()

var_drawdown_data = []

for amfi_code, group in df.groupby('amfi_code'):
  scheme_name = group['scheme_name'].iloc[0]
  returns = group['daily_return'].dropna()

  if len(returns) > 10:
    # Value at Risk (VaR 95%)
    var_95 = np.percentile(returns, 5)

    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    var_drawdown_data.append({
        'amfi_code': amfi_code,
        'scheme_name': scheme_name,
        'VaR_95': var_95,
        'max_drawdown': max_drawdown,
    })

df_var_dd = pd.DataFrame(var_drawdown_data)

print('--- VaR 95% and Drawdown Summary ---')
print(df_var_dd[['scheme_name', 'VaR_95', 'max_drawdown']].head())

# 3. Save to CSV as required by project deliverables
df_var_dd.to_csv('var_drawdown_summary.csv', index=False)
print("\nSuccessfully saved summary to 'var_drawdown_summary.csv'!")
