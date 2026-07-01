import time
from create_tables import setup_database
from generate_data import generate_dirty_data
from ingest_to_staging import ingest_csv_to_staging
from run_audit import run_audit_pipeline
from view_report import generate_audit_report

def run_end_to_end_pipeline():
    print("🎬 STARTING MASTER FINTECH DATA PIPELINE RUN 🎬\n")
    start_time = time.time()

    # Step 1: Re-build database structure
    print("[STEP 1/5]")
    setup_database()
    print("-" * 40)

    # Step 2: Generate fresh data
    print("[STEP 2/5] Simulating transaction logs...")
    df = generate_dirty_data(num_records=5000) # Increased to 5,000 for scale!
    df.to_csv("dirty_transactions.csv", index=False)
    print("-" * 40)

    # Step 3: Ingest to Staging Table
    print("[STEP 3/5]")
    ingest_csv_to_staging("dirty_transactions.csv")
    print("-" * 40)

    # Step 4: Run SQL Audit rules
    print("[STEP 4/5]")
    run_audit_pipeline()
    print("-" * 40)

    # Step 5: Generate Final Dash Report
    print("[STEP 5/5]")
    generate_audit_report()
    
    end_time = time.time()
    print(f"\n🏁 Pipeline execution completed in {round(end_time - start_time, 2)} seconds.")

if __name__ == "__main__":
    run_end_to_end_pipeline()