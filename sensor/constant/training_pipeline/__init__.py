import os

"""
What this file is doing?
This file serves as a centralized location for defining constant variables used throughout the project.
By defining constants in one place, it promotes consistency and makes it easier to manage and update values that are used in multiple parts of the codebase.

"""

# General constants defined here
TARGET_COLUMN = "class"
FILE_NAME: str = 'sensor.csv'
PIPELINE_NAME: str = "sensor" # Name of the main pipeline folder

# Define the common file name for all the stages
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SAVED_MODEL_DIR: str = "saved_models" # folder name where all the saved models will be stored
MODEL_FILE_NAME = "model.pkl" # Name of the model file name



ARTIFACT_DIR: str = "artifact"  # folder name where all the artifacts will be stored

SCHEMA_FILE_PATH = os.path.join("config" , "schema.yaml") # Path of the schema file
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

# Data Preprocessing related constant start with DATA_PREPROCESSING VARIBLEs
DATA_PREPROCESSING_DIR_NAME: str = "data_preprocessing" # folder name for data preprocessing
DATA_PREPROCESSING_PROCESSED_DATA_DIR: str = "processed_data" # folder name for processed data
DATA_PREPROCESSING_PROCESSED_OBJECT_DIR: str = "preprocessing_object" # folder name for preprocessor object
PREPROCESSING_OBJECT_FILE_NAME = "preprocessor.pkl" # Name of the preprocessor object file name

# Model Trainer related constant start with MODEL_TRAINER VARIBLEs
MODEL_TRAINER_DIR_NAME: str = "model_trainer" # folder name for model trainer
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model" # folder name for trained model
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl" # file name for trained model
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6 # expected accuracy score for the model
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD: float = 0.05 # threshold for overfitting and underfitting

# Model Evaluation related constant start with MODEL_EVALUATION VARIBLEs
MODEL_EVALUATION_DIR_NAME: str = "model_evaluation" # folder name for model evaluation
MODEL_EVALUATION_REPORT_NAME: str = "report.yaml" # file name for model evaluation report
MODEL_EVALUATION_THRESHOLD_SCORE: float = 0.02 # threshold for model evaluation

# Model Pusher related constant start with MODEL_PUSHER VARIBLEs
MODEL_PUSHER_DIR_NAME: str = "model_pusher" # folder name for model pusher
MODEL_PUSHER_SAVED_MODEL_DIR: str = SAVED_MODEL_DIR # folder name for saved models in model pusher