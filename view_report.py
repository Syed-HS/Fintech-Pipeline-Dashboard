from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://admin:fintech_secret@localhost:5432/fintech_audit"
engine = create_engine(DATABASE_URL)

def generate_audit_report():
    print("\n==================================================")
    print("      📊 FINTECH PIPELINE AUDIT REPORT            ")
    print("==================================================\n")

    with engine.connect() as connection:
        # 1. Fetch overall counts
        clean_count = connection.execute(text("SELECT COUNT(*) FROM fct_transactions_clean;")).scalar()
        quarantine_count = connection.execute(text("SELECT COUNT(*) FROM quarantine_transactions;")).scalar()
        total = clean_count + quarantine_count
        
        print(f"📈 Total Processed Records : {total}")
        print(f"✅ Clean Records (Passed)  : {clean_count} ({round((clean_count/total)*100, 2)}%)")
        print(f"🚨 Quarantined (Failed)    : {quarantine_count} ({round((quarantine_count/total)*100, 2)}%)\n")
        
        print("--------------------------------------------------")
        print("          CRITICAL BREAKDOWN BY REASON            ")
        print("--------------------------------------------------")
        
        # 2. Fetch specific breakdown of failures
        breakdown_query = """
            SELECT rejection_reason, COUNT(*) as failure_count
            FROM quarantine_transactions
            GROUP BY rejection_reason
            ORDER BY failure_count DESC;
        """
        results = connection.execute(text(breakdown_query)).fetchall()
        
        for row in results:
            print(f"❌ {row[0]} -> {row[1]} records")
            
    print("==================================================")

if __name__ == "__main__":
    generate_audit_report()