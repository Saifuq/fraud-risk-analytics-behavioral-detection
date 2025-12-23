import pandas as pd
from sqlalchemy import create_engine, event
from urllib.parse import quote_plus
from data_loader import load_financial_data
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

def get_engine():
    """
    Creates a SQLAlchemy engine for SQL Server.
    """
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    trusted = os.getenv("DB_TRUSTED_CONNECTION", "yes").lower() == "yes"

    if trusted:
        conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    else:
        conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};"

    params = quote_plus(conn_str)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine

def upload_to_sql(limit=5000, use_synthetic=True, table_name="NigerianTransactions"):
    """
    Loads data and uploads it to SQL Server in batches.
    """
    print(f"Loading data to upload (Limit: {limit}, Synthetic: {use_synthetic})...")
    df = load_financial_data(limit=limit, use_synthetic=use_synthetic)
    
    if df is None:
        return

    print(f"Connecting to database...")
    try:
        engine = get_engine()
        
        # Optimize upload with fast_executemany
        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            if executemany:
                cursor.fast_executemany = True

        print(f"Uploading {len(df)} rows to table '{table_name}'...")
        df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=1000)
        print("✅ Data uploaded successfully!")
        
    except Exception as e:
        print(f"❌ Error during database upload: {e}")
        print("\nTip: Make sure you have the 'ODBC Driver for SQL Server' installed and the server details correct in .env")

if __name__ == "__main__":
    # Note: This will fail until .env is populated with real details
    upload_to_sql(limit=1000, use_synthetic=True)
