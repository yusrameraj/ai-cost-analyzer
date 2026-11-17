import sqlite3
import pandas as pd

print("Loading cleaned data...")
df = pd.read_csv("calls_clean.csv")

# 1. Connect to the database (it creates the file if it doesn't exist)
conn = sqlite3.connect("ai_costs.db")

# 2. Take our Pandas DataFrame and push it straight into a SQL table called "calls"
df.to_sql("calls", conn, if_exists="replace", index=False)
print("Data loaded into table 'calls'!")

# 3. Create a separate table for our pricing
conn.execute("DROP TABLE IF EXISTS model_pricing")
conn.execute("""
    CREATE TABLE model_pricing (
        model TEXT,
        input_per_1m REAL,
        output_per_1m REAL
    )
""")

# 4. Insert pricing rows
conn.execute("INSERT INTO model_pricing VALUES ('gpt-3.5-turbo', 0.50, 1.50)")
conn.execute("INSERT INTO model_pricing VALUES ('gpt-4', 30.00, 60.00)")

# 5. Save and close the connection
conn.commit()
conn.close()

print("Database 'ai_costs.db' created successfully!")