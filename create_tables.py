from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://admin:fintech_secret@localhost:5432/fintech_audit"
engine = create_engine(DATABASE_URL)

def setup_database():
    # SQL commands to drop old tables if they exist and create fresh ones
    queries = [
        # 1. Drop existing tables if re-running
        "DROP TABLE IF EXISTS stg_transactions CASCADE;",
        "DROP TABLE IF EXISTS fct_transactions_clean CASCADE;",
        "DROP TABLE IF EXISTS quarantine_transactions CASCADE;",
        
        # 2. Staging Table (Loads data roughly as text/nullable for initial processing)
        """
        CREATE TABLE stg_transactions (
            transaction_id VARCHAR(50),
            user_id VARCHAR(50),
            timestamp VARCHAR(50),
            amount NUMERIC,
            currency VARCHAR(10),
            country_code VARCHAR(10)
        );
        """,
        
        # 3. Clean Production Table (Strict constraints)
        """
        CREATE TABLE fct_transactions_clean (
            transaction_id VARCHAR(50) PRIMARY KEY,
            user_id VARCHAR(50) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            amount NUMERIC(15, 2) NOT NULL,
            currency VARCHAR(3) NOT NULL,
            country_code VARCHAR(3) NOT NULL
        );
        """,
        
        # 4. Quarantine Table (Captures bad data and stores the failure reason)
        """
        CREATE TABLE quarantine_transactions (
            transaction_id VARCHAR(50),
            user_id VARCHAR(50),
            timestamp VARCHAR(50),
            amount NUMERIC,
            currency VARCHAR(10),
            country_code VARCHAR(10),
            rejection_reason TEXT,
            quarantined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    with engine.connect() as connection:
        # Start a database transaction block
        with connection.begin():
            for query in queries:
                connection.execute(text(query))
    print("✨ Database tables created successfully in PostgreSQL.")

if __name__ == "__main__":
    setup_database()