# Configuration file for database and data processing paths
import os

# Get the base directory for Airflow DAGs
BASE_DIR = "/home/Assignment/airflow/"

# Path to the database where processed data will be stored
DB_PATH = os.path.join(BASE_DIR, "database")
DB_FILE_NAME = "utils_output.db"

# Unit test database file name (used for testing)
UNIT_TEST_DB_FILE_NAME = "unit_test_cases.db"

# Directory containing the raw data files
DATA_DIRECTORY = DATA_DIRECTORY = os.path.join(BASE_DIR, "data")

# Path to the interaction mapping file
INTERACTION_MAPPING = os.path.join(BASE_DIR, "data", "interaction_mapping.csv")

# Define column names for training and inference processing (Update with actual column names)
INDEX_COLUMNS_TRAINING = ["column1", "column2"]  
INDEX_COLUMNS_INFERENCE = ["column1", "column2"]  

# Features that should not be used for model training
NOT_FEATURES = ["unnecessary_feature1", "unnecessary_feature2"]  
