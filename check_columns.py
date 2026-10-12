import sqlite3

conn = sqlite3.connect('mutual_fund_analytics.db')
cursor = conn.cursor()

# Get table list and columns
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Table: {table_name} \nColumns: {columns}\n")

conn.close()
