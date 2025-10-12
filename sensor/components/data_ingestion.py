import os , sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from sensor.logger import logging
from sensor.exception import SensorException

from sensor.constant.database import COLLECTION_NAME
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
            dataframe = sensor_data.export_collection_as_dataframe(collection_name = COLLECTION_NAME)

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # create directory if not available
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path , exist_ok=True)

            dataframe.to_csv(feature_store_file_path , index = False , header = True)

            logging.info("Data successfully exported to feature store")
            return dataframe

        except Exception as e:
            raise SensorException(e , sys)
        
    def split_data_as_train_test(self , dataframe : DataFrame) -> None:
        try:
            logging.info("Splitting data into train and test")

            train_set , test_set = train_test_split(dataframe , test_size = self.data_ingestion_config.test_size , random_state = 42)

            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path

            # create directory if not available
            dir_path = os.path.dirname(train_file_path)
            os.makedirs(dir_path , exist_ok=True)

            train_set.to_csv(test_file_path , index = False , header = True)
            test_set.to_csv(test_file_path , index = False , header = True)

            logging.info("Successfully split the data into train and test")

        except Exception as e:
            raise SensorException(e , sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feaure_store()

            self.split_data_as_train_test(dataframe = dataframe)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path = self.data_ingestion_config.train_file_path , 
                                                            test_file_path = self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e , sys)