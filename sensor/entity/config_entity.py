from datetime import datetime
import os , sys
from sensor.constant.training_pipeline import PIPELINE_NAME , ARTIFACT_DIR , DATA_INGESTION_DIR_NAME , FILE_NAME , DATA_INGESTION_FEATURE_STORE_DIR , DATA_INGESTION_INGESTED_DIR , TEST_FILE_NAME
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
            self.train_file_path = os.path.join(self.data_ingestion_dir , DATA_INGESTION_INGESTED_DIR , "train" , TEST_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir , DATA_INGESTION_INGESTED_DIR , "test" , TEST_FILE_NAME)
            self.test_size = 0.2
            self.collection_name = "sensor"

    except Exception as e:
        raise SensorException(e , sys)