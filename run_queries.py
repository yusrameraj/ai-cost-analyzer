import sqlite3
import pandas as pd

# 1. Connect to the database
conn = sqlite3.connect("ai_costs.db")

# 2. Write the SQL query as a string
query = query = """
SELECT 
    model, 
    COUNT(*) AS total_calls, 
    ROUND(SUM(cost_usd), 2) AS total_cost,
    
    SUM(CASE WHEN useful = 0 THEN 1 ELSE 0 END) AS waste_calls,
    ROUND(100.0 * SUM(CASE WHEN useful = 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS waste_pct,
    ROUND(SUM(CASE WHEN useful = 0 THEN cost_usd ELSE 0 END), 2) AS wasted_spend
    
FROM calls
GROUP BY model
"""

# 3. Use Pandas to run the query and save the result as a DataFrame
result = pd.read_sql(query, conn)

# 4. Print the result
print("--- TOTAL COST BY MODEL ---")
print(result)

result.to_csv("dashboard_data.csv", index=False)
print("Saved dashboard_data.csv!")

# 5. Close the connection
conn.close()