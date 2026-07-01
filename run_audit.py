from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://admin:fintech_secret@localhost:5432/fintech_audit"
engine = create_engine(DATABASE_URL)

def run_audit_pipeline():
    print("⚡ Starting FinTech Data Audit Validation Engine...")

    # SQL Queries to execute in sequence
    queries = {
        # 1. Clear out clean and quarantine tables from any previous runs
        "clear_clean": "TRUNCATE TABLE fct_transactions_clean;",
        "clear_quarantine": "TRUNCATE TABLE quarantine_transactions;",

        # 2. ISOLATE BAD & FRAUDULENT DATA INTO QUARANTINE
        "route_to_quarantine": """
            WITH ranked_transactions AS (
                SELECT 
                    transaction_id, user_id, timestamp, amount, currency, country_code,
                    -- Safe cast: Only convert if it starts with the correct YYYY- layout
                    CASE 
                        WHEN timestamp LIKE '2026-%' THEN CAST(timestamp AS TIMESTAMP)
                        ELSE NULL 
                    END as ts_converted,
                    LAG(CASE WHEN timestamp LIKE '2026-%' THEN CAST(timestamp AS TIMESTAMP) ELSE NULL END) OVER (
                        PARTITION BY user_id, amount 
                        ORDER BY CASE WHEN timestamp LIKE '2026-%' THEN CAST(timestamp AS TIMESTAMP) ELSE NULL END
                    ) as prev_timestamp
                FROM stg_transactions
            )
            INSERT INTO quarantine_transactions (
                transaction_id, user_id, timestamp, amount, currency, country_code, rejection_reason
            )
            SELECT 
                stg.transaction_id, stg.user_id, stg.timestamp, stg.amount, stg.currency, stg.country_code,
                CASE 
                    WHEN stg.amount IS NULL OR stg.amount <= 0 THEN 'INVALID_AMOUNT: Amount must be positive numeric value'
                    WHEN stg.country_code IS NULL OR LENGTH(stg.country_code) != 3 THEN 'INVALID_COUNTRY: Country code missing or must be 3 chars ISO'
                    WHEN stg.user_id IS NULL THEN 'MISSING_USER: User identification key is NULL'
                    WHEN stg.timestamp NOT LIKE '2026-%' THEN 'MALFORMED_DATE: Date format must be YYYY-MM-DD'
                    WHEN rt.ts_converted IS NOT NULL AND rt.prev_timestamp IS NOT NULL AND (rt.ts_converted - rt.prev_timestamp) <= INTERVAL '5 minutes' THEN 'SUSPECTED_FRAUD: Duplicate transaction within 5 minutes'
                    ELSE 'UNKNOWN_BIZ_VIOLATION'
                END as rejection_reason
            FROM stg_transactions stg
            JOIN ranked_transactions rt ON stg.transaction_id = rt.transaction_id
            WHERE stg.amount IS NULL 
               OR stg.amount <= 0 
               OR stg.country_code IS NULL 
               OR LENGTH(stg.country_code) != 3
               OR stg.user_id IS NULL
               OR stg.timestamp NOT LIKE '2026-%'
               OR (rt.ts_converted IS NOT NULL AND rt.prev_timestamp IS NOT NULL AND (rt.ts_converted - rt.prev_timestamp) <= INTERVAL '5 minutes');
        """,

        # 3. ROUTE GOOD DATA TO PRODUCTION
        "route_to_clean": """
            WITH ranked_transactions AS (
                SELECT 
                    transaction_id,
                    CASE WHEN timestamp LIKE '2026-%' THEN CAST(timestamp AS TIMESTAMP) ELSE NULL END as ts_converted,
                    LAG(CASE WHEN timestamp LIKE '2026-%' THEN CAST(timestamp AS TIMESTAMP) ELSE NULL END) OVER (
                        PARTITION BY user_id, amount 
                        ORDER BY CASE WHEN timestamp LIKE '2026-%' THEN CAST(timestamp AS TIMESTAMP) ELSE NULL END
                    ) as prev_timestamp
                FROM stg_transactions
            )
            INSERT INTO fct_transactions_clean (
                transaction_id, user_id, timestamp, amount, currency, country_code
            )
            SELECT DISTINCT ON (stg.transaction_id)
                stg.transaction_id, 
                stg.user_id, 
                CAST(stg.timestamp AS TIMESTAMP), 
                stg.amount, 
                stg.currency, 
                stg.country_code
            FROM stg_transactions stg
            JOIN ranked_transactions rt ON stg.transaction_id = rt.transaction_id
            WHERE stg.amount > 0 
              AND stg.country_code IS NOT NULL 
              AND LENGTH(stg.country_code) = 3
              AND stg.user_id IS NOT NULL
              AND stg.timestamp LIKE '2026-%'
              AND (rt.prev_timestamp IS NULL OR (rt.ts_converted - rt.prev_timestamp) > INTERVAL '5 minutes');
        """
    }
    

    with engine.connect() as connection:
        with connection.begin():
            # Run the steps sequentially inside a single transactional block
            connection.execute(text(queries["clear_clean"]))
            connection.execute(text(queries["clear_quarantine"]))
            
            res_quarantine = connection.execute(text(queries["route_to_quarantine"]))
            res_clean = connection.execute(text(queries["route_to_clean"]))
            
    print("✅ Audit pipeline execution completed successfully!")

if __name__ == "__main__":
    run_audit_pipeline()