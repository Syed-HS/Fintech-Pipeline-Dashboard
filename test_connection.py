from sqlalchemy import create_engine

# Windows local connection string
DATABASE_URL = "postgresql://admin:fintech_secret@localhost:5432/fintech_audit"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("🚀 Success! Python successfully connected to PostgreSQL on Windows.")
except Exception as e:
    print(f"❌ Connection failed. Error: {e}")