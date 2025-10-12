import os , sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from sensor.logger import logging
from sensor.exception import SensorException

from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData

class DataIngesion:

    def __init__(self , data_ingestion_config : DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        
        except Exception as e:
            raise SensorException(e , sys)
        
    def eport_data_into_feaure_store(self) -> DataFrame:
        try:
            logging.info("Exporting data from mongodb to feature store")

            sensor_data = SensorData()
            df : DataFrame = sensor_data.export_collection_as_dataframe(collection_name = self.data_ingestion_config.collection_name)

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path , exist_ok=True)

            df.to_csv(feature_store_file_path , index = False , header = True)

            return df

        except Exception as e:
            raise SensorException(e , sys)