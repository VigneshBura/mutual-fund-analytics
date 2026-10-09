import os
import pandas as pd

RAW_DIR = "data/raw"

def load_and_inspect_datasets():
    print("=== TASK 3: Loading CSV Datasets from data/raw/ ===")
    if not os.path.exists(RAW_DIR):
        print(f"Directory {RAW_DIR} does not exist.")
        return {}
    
    csv_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv')]
    datasets = {}
    for file in csv_files:
        path = os.path.join(RAW_DIR, file)
        try:
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            datasets[file] = df
        except Exception as e:
            print(f"Error loading {file}: {e}")
    print(f"Successfully loaded {len(datasets)} datasets.\n")
    return datasets

def explore_fund_master(datasets):
    print("=== TASK 6: Exploring Fund Master ===")
    fm_key = next((k for k in datasets.keys() if '01_fund_master' in k), None)
    
    if fm_key:
        df = datasets[fm_key]
        print(f"Found Fund Master file: {fm_key}")
        if 'fund_house' in df.columns:
            print("Unique Fund Houses:", df['fund_house'].nunique())
        if 'category' in df.columns:
            print("Categories:", df['category'].unique())
        if 'sub_category' in df.columns:
            print("Sub-Categories:", df['sub_category'].unique())
        if 'risk_grade' in df.columns or 'risk_category' in df.columns:
            risk_col = 'risk_grade' if 'risk_grade' in df.columns else 'risk_category'
            print("Risk Grades:", df[risk_col].unique())
    else:
        print("Fund master file not detected.")

def validate_amfi_codes(datasets):
    print("\n=== TASK 7: Validating AMFI Codes ===")
    fm_key = next((k for k in datasets.keys() if '01_fund_master' in k), None)
    nav_key = next((k for k in datasets.keys() if '02_nav_history' in k), None)
    
    if fm_key and nav_key:
        fm_df = datasets[fm_key]
        nav_df = datasets[nav_key]
        
        if 'amfi_code' in fm_df.columns and 'amfi_code' in nav_df.columns:
            fm_codes = set(fm_df['amfi_code'].dropna().unique())
            nav_codes = set(nav_df['amfi_code'].dropna().unique())
            
            missing_in_nav = fm_codes - nav_codes
            print(f"Total schemes in fund_master: {len(fm_codes)}")
            print(f"Total schemes in nav_history: {len(nav_codes)}")
            print(f"Schemes in fund_master missing from nav_history: {len(missing_in_nav)}")
            print("\n[Data Quality Summary]")
            print(f"- All fund_master schemes present in nav history: {len(missing_in_nav) == 0}")
        else:
            print(f"Could not find 'amfi_code' column. Found columns - FM: {fm_df.columns}, NAV: {nav_df.columns}")
    else:
        print("Required datasets for validation not found.")

if __name__ == "__main__":
    datasets = load_and_inspect_datasets()
    if datasets:
        explore_fund_master(datasets)
        validate_amfi_codes(datasets)