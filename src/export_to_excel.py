import pandas as pd
from data_loader import load_financial_data
import argparse
import os

def export_data_to_excel(limit=None, use_synthetic=False, output_file="fraud_data_export.xlsx"):
    """
    Loads data and exports it to an Excel (.xlsx) file.
    Note: Excel has a limit of 1,048,576 rows.
    """
    max_excel_rows = 1048575 # Excel limit minus header
    
    if limit is None or limit > max_excel_rows:
        print(f"Note: Excel limit is 1,048,576 rows. Capping export at 1,048,575 rows.")
        limit = max_excel_rows

    print(f"Fetching data (Targeting: {limit} rows, Synthetic: {use_synthetic})...")
    # We use streaming in load_financial_data via the limit parameter
    df = load_financial_data(limit=limit, use_synthetic=use_synthetic)
    
    if df is not None:
        if len(df) > max_excel_rows:
            print(f"Trimming data to {max_excel_rows} rows for Excel compatibility.")
            df = df.iloc[:max_excel_rows]
            
        print(f"Exporting {len(df)} rows to {output_file}...")
        try:
            # Using openpyxl engine
            df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"Success! File saved at: {os.path.abspath(output_file)}")
        except Exception as e:
            print(f"Error during export: {e}")
    else:
        print("Failed to load data. Export aborted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Financial Data to Excel")
    parser.add_argument("--limit", type=int, default=1000, help="Number of rows to export")
    parser.add_argument("--real", action="store_true", help="Use real data instead of synthetic")
    parser.add_argument("--out", type=str, default="fraud_data_export.xlsx", help="Output filename")
    
    args = parser.parse_args()
    
    export_data_to_excel(limit=args.limit, use_synthetic=not args.real, output_file=args.out)
