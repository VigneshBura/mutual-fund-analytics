import os
import pandas as pd
from sqlalchemy import create_engine

# Define database path
db_path = 'mutual_fund_analytics.db'
engine = create_engine(f'sqlite:///{db_path}')

print(f"Database engine created successfully at {db_path}")

# Dictionary mapping table names to their corresponding CSV files
tables_to_load = {
    'dim_fund': 'data/raw/01_fund_master.csv',
    'fact_nav': 'data/raw/02_nav_history.csv',
    'fact_aum': 'data/raw/03_aum_by_fund_house.csv',
    'fact_sip': 'data/raw/04_monthly_sip_inflows.csv',
    'fact_transactions': 'data/raw/08_investor_transactions.csv'
}

for table_name, file_path in tables_to_load.items():
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Load into SQLite table
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Successfully loaded '{table_name}' with {len(df)} rows.")
    else:
        print(f"Warning: File not found for {table_name} at {file_path}")
