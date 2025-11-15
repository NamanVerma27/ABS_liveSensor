from datetime import datetime
import os , sys
from sensor.constant.training_pipeline import PIPELINE_NAME , ARTIFACT_DIR , DATA_INGESTION_DIR_NAME , FILE_NAME , DATA_INGESTION_FEATURE_STORE_DIR , DATA_INGESTION_INGESTED_DIR , TEST_FILE_NAME , DATA_INGESTION_COLLECTION_NAME , TRAIN_FILE_NAME , DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
from sensor.constant.training_pipeline import DATA_VALIDATION_DIR_NAME , DATA_VALIDATION_VALID_DIR , DATA_VALIDATION_INVALID_DIR , DATA_VALIDATION_DRIFT_REPORT_DIR , DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
from sensor.constant.training_pipeline import 
from sensor.exception import SensorException

class TrainingPipelineConfig:
    try:
        def __init__(self):
            self.timestamp = datetime.now().strftime("%m-%d-%Y__%H-%M-%S")

            self.pipeline_name = PIPELINE_NAME
            self.artifact_dir = os.path.join(ARTIFACT_DIR , self.timestamp)

    except Exception as e:
        raise SensorException(e , sys)
    
class DataIngestionConfig:
    try:
        def __init__(self , training_pipeline_config : TrainingPipelineConfig):
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , DATA_INGESTION_DIR_NAME)
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir , DATA_INGESTION_FEATURE_STORE_DIR , FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir , DATA_INGESTION_INGESTED_DIR , TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir , DATA_INGESTION_INGESTED_DIR , TEST_FILE_NAME)
            self.test_size = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
            self.collection_name: str = DATA_INGESTION_COLLECTION_NAME

    except Exception as e:
        raise SensorException(e , sys)
    
class DataValidationConfig:

    try:
        def __init__(self , training_pipeline_config : TrainingPipelineConfig):
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir , DATA_VALIDATION_DIR_NAME)
            self.valid_data_dir = os.path.join(self.data_validation_dir , DATA_VALIDATION_VALID_DIR)
            self.invalid_data_dir = os.path.join(self.data_validation_dir , DATA_VALIDATION_INVALID_DIR)
            self.valid_train_file_path = os.path.join(self.valid_data_dir , TRAIN_FILE_NAME)
            self.valid_test_file_path = os.path.join(self.valid_data_dir , TEST_FILE_NAME)
            self.invalid_train_file_path = os.path.join(self.invalid_data_dir , TRAIN_FILE_NAME)
            self.invalid_test_file_path = os.path.join(self.invalid_data_dir , TEST_FILE_NAME)
            
            self.drift_report_dir = os.path.join(self.data_validation_dir , DATA_VALIDATION_DRIFT_REPORT_DIR)
            self.drift_report_file_path = os.path.join(self.drift_report_dir , DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        
    except Exception as e:
        raise SensorException(e , sys)

class DataPreprocessingConfig:
    try:
        def __init__(self , training_pipeline_config : TrainingPipelineConfig):
