import sqlite3
from utils import load_data_into_db, map_city_tier, map_categorical_vars

# Database path
db_path = "/home/Assignment/airflow/database/utils_output.db"

# Run the functions to create tables
print("Running: load_data_into_db()")
load_data_into_db()

print("Running: map_city_tier()")
map_city_tier()

print("Running: map_categorical_vars()")
map_categorical_vars()

print("✅ All tables created successfully!")

# Close database connection
conn = sqlite3.connect(db_path)
conn.close()
