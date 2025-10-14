import os

"""
What this file is doing?
This file serves as a centralized location for defining constant variables used throughout the project.
By defining constants in one place, it promotes consistency and makes it easier to manage and update values that are used in multiple parts of the codebase.

"""

# Define all the constant variables here
FILE_NAME: str = 'sensor.csv'
TARGET_COLUMN = "class"
PIPELINE_NAME: str = "sensor" # Name of the main pipeline folder
ARTIFACT_DIR: str = "artifact"  # folder name where all the artifacts will be stored

# Define the common file name for all the stages
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl" # Name of the preprocessor object file name
MODEL_FILE_NAME = "model.pkl" # Name of the model file name
SCHEMA_FILE_PATH = os.path.join("config" , "schema.yaml") # Path of the schema file
SCHEMA_DROP_COLS = "drop_columns" # columns to be dropped during data cleaning

# Data Ingestion related constant start with DATA_INGESTION VARIBLEs
DATA_INGESTION_COLLECTION_NAME: str = "sensor_data" # collection name in mongodb
DATA_INGESTION_DIR_NAME: str = "data_ingestion" # folder name for data ingestion
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store" # folder name for feature store
DATA_INGESTION_INGESTED_DIR: str = "ingested" # folder name for ingested data
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2 # train test split ratio

# Data Validation related constant start with DATA_VALIDATION VARIBLEs
DATA_VALIDATION_DIR_NAME: str = "data_validation" # folder name for data validation
DATA_VALIDATION_VALID_DIR: str = "validated" # folder name for validated data
DATA_VALIDATION_INVALID_DIR: str = "invalid" # folder name for invalid data
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report" # folder name for drift report
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml" # file name for drift report