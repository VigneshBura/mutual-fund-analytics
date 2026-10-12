import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the SQLite database
conn = sqlite3.connect('mutual_fund_analytics.db')

# 1. Query Fund Master & NAV summary statistics using 'amfi_code'
df_nav_summary = pd.read_sql("""
    SELECT f.scheme_name, COUNT(n.nav) as nav_count, MIN(n.nav) as min_nav, MAX(n.nav) as max_nav, AVG(n.nav) as avg_nav
    FROM dim_fund f
    JOIN fact_nav n ON f.amfi_code = n.amfi_code
    GROUP BY f.scheme_name;
""", con=conn)

print("--- NAV Summary Statistics ---")
print(df_nav_summary.head())

# 2. Query Transaction totals by Type using 'amount_inr'
df_transactions = pd.read_sql("""
    SELECT transaction_type, COUNT(*) as total_count, SUM(amount_inr) as total_amount
    FROM fact_transactions
    GROUP BY transaction_type;
""", con=conn)

print("\n--- Transaction Breakdown ---")
print(df_transactions)

# 3. Generate a quick visualization: Transaction Amounts by Type
plt.figure(figsize=(8, 5))
sns.barplot(data=df_transactions, x='transaction_type', y='total_amount', palette='viridis')
plt.title('Total Transaction Amount by Type')
plt.xlabel('Transaction Type')
plt.ylabel('Total Amount (₹)')
plt.tight_layout()

# Save the plot
plt.savefig('transaction_analysis.png')
print("\nVisualization saved successfully as 'transaction_analysis.png'!")

conn.close()
