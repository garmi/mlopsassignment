#############################################################################
# Import necessary modules and files
##############################################################################

import pandas as pd
import os
import sqlite3
from sqlite3 import Error
import sys
sys.path.append('/home/Assignment/airflow/dags')  # Ensure Python can find constants.py
from constants import DB_FILE_NAME, DB_PATH, DATA_DIRECTORY, INTERACTION_MAPPING
from mapping.city_tier_mapping import city_tier_mapping
from mapping.significant_categorical_level import list_platform, list_medium, list_source

###############################################################################
# Define function to load the csv file to the database
###############################################################################

def load_data_into_db():
    try:
        file_path = os.path.join(DATA_DIRECTORY, "leadscoring.csv")
        db_full_path = os.path.join(DB_PATH, DB_FILE_NAME)
        
        print("Using Database:", db_full_path)

        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found!")
            return

        df = pd.read_csv(file_path)
        print("CSV Loaded. Columns:", df.columns)
        
        df.fillna({"total_leads_dropped": 0, "referred_lead": 0}, inplace=True)
        
        conn = sqlite3.connect(db_full_path)
        
        # Write to DB
        df.to_sql("loaded_data", conn, if_exists="replace", index=False)
        
        # Verify tables after writing
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print("Tables after writing:", tables)
        
        conn.commit()  # Force Commit
        conn.close()

        print("Data successfully written to DB.")
    
    except Exception as e:
        print(f"Error in loading data: {e}")

###############################################################################
# Define function to map cities to their respective tiers
###############################################################################

def map_city_tier():
    try:
        db_full_path = os.path.join(DB_PATH, DB_FILE_NAME)
        print("Using Database:", db_full_path)
        
        conn = sqlite3.connect(db_full_path)
        
        # Check if loaded_data table exists
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        table_names = [table[0] for table in tables]
        print("Existing Tables:", table_names)
        
        if "loaded_data" not in table_names:
            print("Error: 'loaded_data' table not found in database!")
            conn.close()
            return
        
        df = pd.read_sql("SELECT * FROM loaded_data", conn)
        df["city_tier"] = df["city_mapped"].map(city_tier_mapping).fillna(3.0)
        
        # Write to DB
        df.to_sql("city_tier_mapped", conn, if_exists="replace", index=False)
        
        # Verify tables after writing
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print("Tables after writing:", tables)
        
        conn.commit()  # Force Commit
        conn.close()
        
        print("City tier mapping applied successfully.")
    
    except Exception as e:
        print(f"Error in mapping city tiers: {e}")

###############################################################################
# Define function to map insignificant categorical variables
###############################################################################

def map_categorical_vars():
    try:
        db_full_path = os.path.join(DB_PATH, DB_FILE_NAME)
        print("Using Database:", db_full_path)
        
        conn = sqlite3.connect(db_full_path)
        df = pd.read_sql("SELECT * FROM city_tier_mapped", conn)
        
        df["first_platform_c"] = df["first_platform_c"].apply(lambda x: x if x in list_platform else "others")
        df["first_utm_medium_c"] = df["first_utm_medium_c"].apply(lambda x: x if x in list_medium else "others")
        df["first_utm_source_c"] = df["first_utm_source_c"].apply(lambda x: x if x in list_source else "others")
        
        df.to_sql("categorical_variables_mapped", conn, if_exists="replace", index=False)
        
        conn.commit()
        conn.close()
        
        print("Categorical variables mapped successfully.")
    
    except Exception as e:
        print(f"Error in mapping categorical variables: {e}")
