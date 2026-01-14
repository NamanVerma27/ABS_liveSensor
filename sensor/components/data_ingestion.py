import os, sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split


from sensor.logger import logging as global_logging # Keep the config import
from sensor.exception import SensorException

# Initialize a named logger for THIS specific module
import logging
logger = logging.getLogger(__name__)

from sensor.utils.main_utils import read_yaml_file, write_yaml_file
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH, SCHEMA_DROP_COLS

from sensor.constant.database import COLLECTION_NAME
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData


class DataIngestion:
    """
    Handles the data ingestion stage:
    - Extracts data from MongoDB (feature store)
    - Cleans and saves it to local feature store
    - Splits the data into training and testing sets
    - Returns metadata (artifact) for the next pipeline stages
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Step 1: Export data from MongoDB and save it to the feature store as a CSV file.
        Returns the extracted DataFrame for further processing.
        """
        try:
            logger.info("Exporting data from MongoDB to feature store")

            # Create a SensorData object to interact with MongoDB
            sensor_data = SensorData()

            # Fetch the collection as a Pandas DataFrame
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=COLLECTION_NAME)

            # Get the path to store the exported feature data
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # Create directory for feature store if it doesn’t exist
            dir_path = os.path.dirname(feature_store_file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            # Save the data to CSV
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            logger.info("Data successfully exported to feature store")
            return dataframe

        except Exception as e:
            raise SensorException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Step 2: Split the dataset into training and testing sets and save them as CSV files.
        """
        try:
            logger.info("Splitting data into train and test sets")

            # Split data using sklearn utility (deterministic via random_state)
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.test_size,
                random_state=42
            )

            # Define file paths for training and test data
            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path

            # Ensure output directory exists
            dir_path = os.path.dirname(train_file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            # Save train and test datasets separately
            train_set.to_csv(train_file_path, index=False, header=True)
            test_set.to_csv(test_file_path, index=False, header=True)

            logger.info("Successfully split and saved the data into train and test files")

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Orchestrates the complete data ingestion process:
        - Extract data from MongoDB
        - Drop unnecessary columns
        - Split into train/test
        - Create and return a DataIngestionArtifact object
        """
        try:
            # --- Step 1: Export data from MongoDB to feature store ---
            dataframe = self.export_data_into_feature_store()

            # --- Step 2: Drop columns defined in schema constants ---
            # Using errors='ignore' ensures it won’t crash if a column doesn’t exist
            dataframe = dataframe.drop(self._schema_config["drop_columns"],axis=1)
            logger.info(f"Dropped unnecessary columns: {SCHEMA_DROP_COLS}")

            # --- Step 3: Split into training and testing sets ---
            self.split_data_as_train_test(dataframe=dataframe)

            # --- Step 4: Create a DataIngestionArtifact to store metadata paths ---
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )

            logger.info(f"Data ingestion completed successfully. Artifact: {data_ingestion_artifact}")

            # --- Step 5: Return the artifact for the next pipeline stage ---
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)
