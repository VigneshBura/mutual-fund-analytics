import os
import requests
import pandas as pd

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# Schemes to fetch (HDFC Top 100 + 5 key schemes)
SCHEMES = {
    "HDFC_Top_100_Direct": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

def fetch_and_save_nav(scheme_name, scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching NAV for {scheme_name} (Code: {scheme_code})...")
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        nav_data = data.get("data", [])
        
        if nav_data:
            df = pd.DataFrame(nav_data)
            df['scheme_code'] = scheme_code
            df['scheme_name'] = data.get("meta", {}).get("scheme_name", scheme_name)
            
            file_path = os.path.join(RAW_DIR, f"{scheme_name}_{scheme_code}.csv")
            df.to_csv(file_path, index=False)
            print(f"-> Successfully saved {len(df)} records to {file_path}")
        else:
            print(f"-> No NAV data found for {scheme_name}")
    else:
        print(f"-> Failed to fetch data. HTTP Status: {response.status_code}")

if __name__ == "__main__":
    for name, code in SCHEMES.items():
        fetch_and_save_nav(name, code)
    print("\nLive NAV fetching complete!")