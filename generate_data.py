import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_dirty_data(num_records=1000):
    data = []
    start_date = datetime(2026, 1, 1)

    for i in range(num_records):
        tx_id = f"TXN_{10000 + i}"
        user_id = f"USR_{random.randint(1000, 1999)}"
        
        # Standard valid fields
        amount = round(random.uniform(10.0, 5000.0), 2)
        currency = random.choice(["USD", "EUR", "GBP"])
        country = random.choice(["USA", "DEU", "GBR"])
        timestamp = start_date + timedelta(minutes=random.randint(1, 50000))
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # --- Injecting Anomalies intentionally ---
        dice = random.random()
        
        if dice < 0.02: 
            # Anomaly Type A: Negative Amount
            amount = -amount
        elif dice < 0.04:
            # Anomaly Type B: Missing Country Code (Structural NULL)
            country = None
        elif dice < 0.06:
            # Anomaly Type C: Currency Mismatch (e.g., UK using USD)
            if country == "GBR": currency = "USD"
        elif dice < 0.08:
            # Anomaly Type D: Corrupted date string format
            timestamp_str = timestamp.strftime("%d/%m/%Y")
            
        data.append([tx_id, user_id, timestamp_str, amount, currency, country])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['transaction_id', 'user_id', 'timestamp', 'amount', 'currency', 'country_code'])
# Anomaly Type E: Duplicate entries (Exact row replication)
    duplicates = df.sample(n=15, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)

    # --- ADD THIS: Anomaly Type F: Velocity Fraud (Same user, same amount, +2 mins later) ---
    fraud_base = df.sample(n=10, random_state=7)
    fraud_records = fraud_base.copy()
    
    # Modify timestamps to be exactly 2 minutes later
    fraud_records['timestamp'] = fraud_records['timestamp'].apply(
        lambda x: (datetime.strptime(x, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
        if "-" in x else x
    )
    # Give them new distinct transaction IDs so they look like separate click events
    fraud_records['transaction_id'] = fraud_records['transaction_id'] + "_F"
    df = pd.concat([df, fraud_records], ignore_index=True)
   
    return df

if __name__ == "__main__":
    print("⏳ Generating dirty financial records...")
    df_dirty = generate_dirty_data()
    
    output_path = "dirty_transactions.csv"
    df_dirty.to_csv(output_path, index=False)
    
    print(f"✅ Generated {len(df_dirty)} records successfully!")
    print(f"📁 Saved to: {output_path}")