import pandas as pd
from sqlalchemy import create_engine,text

DATABASE_URL = "postgresql://admin:fintech_secret@localhost:5432/fintech_audit"
engine = create_engine(DATABASE_URL)

def ingest_csv_to_staging(csv_file_path):
    print(f"📖 Reading raw transaction data from {csv_file_path}...")
    
    # Load data into Pandas
    df = pd.read_csv(csv_file_path)
    
    total_records = len(df)
    print(f"📊 Extracted {total_records} records into memory.")

    # --- Pre-Ingestion Data Type Adjustments ---
    # Convert amounts to float numeric types; unparseable strings turn into NaN
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    print("🚀 Bulk inserting raw batch into PostgreSQL staging table...")
    
    # Push the dataframe directly into the 'stg_transactions' database table
    # if_exists='append' ensures we add onto the existing structure without dropping constraints
    df.to_sql(
        name='stg_transactions', 
        con=engine, 
        if_exists='append', 
        index=False
    )
    
    print(f"✅ Successfully staged {len(df)} records into 'stg_transactions'.")

if __name__ == "__main__":
    # Clear old staging runs first, then load the generated dirty data csv
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(text("TRUNCATE TABLE stg_transactions;"))
            
    ingest_csv_to_staging("dirty_transactions.csv")