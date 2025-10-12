from datetime import datetime
import os , sys
from sensor.constant.training_pipeline import PIPELINE_NAME , ARTIFACT_DIR , DATA_INGESTION_DIR_NAME , FILE_NAME , DATA_INGESTION_FEATURE_STORE_DIR , DATA_INGESTION_INGESTED_DIR , TEST_FILE_NAME , DATA_INGESTION_COLLECTION_NAME , TRAIN_FILE_NAME , DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
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