import os,sys

import pandas as pd
from pandas import DataFrame
from scipy.stats import ks_2samp

from sensor.logger import logging as global_logging
from sensor.exception import SensorException

import logging
logger = logging.getLogger(__name__)

from sensor.constant.training_pipeline import SCHEMA_FILE_PATH

from sensor.utils.main_utils import read_yaml_file, write_yaml_file
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    # static method to read data : not dependent on instance
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path, na_values="na")
        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            logger.info("Validating number of columns")
            logger.info(f"Required number of columns: {len(self._schema_config['columns'])} , Present number of columns: {len(dataframe.columns)}")
            number_of_columns = len(self._schema_config['columns'])
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_column_exist(self, dataframe: DataFrame) -> bool:
        try:
            logger.info("Validating numerical columns")
            numerical_columns = self._schema_config['numerical_columns']
            dataframe_columns = dataframe.select_dtypes(include=['int64', 'float64']).columns
            missing_numerical_columns = [col for col in numerical_columns if col not in dataframe_columns]
            if len(missing_numerical_columns) > 0:
                logger.info(f"Missing numerical columns: {missing_numerical_columns}")
                return False
            return True
        except Exception as e:
            raise SensorException(e, sys)

    def detect_data_drift(self, base_df, current_df, threshold: float = 0.05) -> bool:
        try:
            logger.info("Detecting data drift")
            drift_report = {}
            for column in base_df.columns:
                # <-- SAFETY: skip columns not present in current_df to avoid KeyError
                if column not in current_df.columns:
                    logger.warning(f"Column '{column}' present in base_df but missing in current_df. Skipping drift test for this column.")
                    continue

                base_data = base_df[column]
                current_data = current_df[column]
                ks_statistic, p_value = ks_2samp(base_data, current_data)
                if p_value < threshold:
                    drift_report[column] = {
                        "p_value": p_value,
                        "drift_detected": True
                    }
                else:
                    drift_report[column] = {
                        "p_value": p_value,
                        "drift_detected": False
                    }
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            write_yaml_file(file_path=drift_report_file_path, content=drift_report, replace=True)
            logger.info(f"Drift report written to {drift_report_file_path}")
            return any([report["drift_detected"] for report in drift_report.values()])
        except Exception as e:
            raise SensorException(e, sys)

    # <-- MOVED inside the class so `self` is valid
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logger.info("Starting data validation process.")

            # --- 1. Get file paths and read data ---
            train_file_path = self.data_ingestion_artifact.training_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Using class static method as in your provided code
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # --- 2. Validation Checks (Using Direct Exception Raising for Clarity) ---

            # 2.1 Validate number of columns
            if not self.validate_number_of_columns(dataframe=train_dataframe):
                raise SensorException("Training data does not have the required number of columns.", sys)
            logger.info("Training data: Number of columns validated successfully.")

            if not self.validate_number_of_columns(dataframe=test_dataframe):
                raise SensorException("Testing data does not have the required number of columns.", sys)
            logger.info("Testing data: Number of columns validated successfully.")
            
            # 2.2 Validate numerical columns
            if not self.is_numerical_column_exist(dataframe=train_dataframe):
                raise SensorException("Training data is missing required numerical columns.", sys)
            logger.info("Training data: Numerical columns validated successfully.")

            if not self.is_numerical_column_exist(dataframe=test_dataframe):
                raise SensorException("Testing data is missing required numerical columns.", sys)
            logger.info("Testing data: Numerical columns validated successfully.")

            # --- 3. Detect Data Drift ---
            drift_detected = self.detect_data_drift(base_df=train_dataframe, current_df=test_dataframe)

            # Set validation_status based on drift detection
            validation_status = not drift_detected

            if drift_detected:
                logger.warning("Data drift detected between training and testing datasets.")
            else:
                logger.info("No data drift detected between training and testing datasets.")

            # --- 4. Prepare and Save Artifacts ---
            os.makedirs(self.data_validation_config.valid_data_dir, exist_ok=True)
            os.makedirs(self.data_validation_config.invalid_data_dir, exist_ok=True)

            # Initialize artifact paths
            valid_train_file_path = None
            valid_test_file_path = None
            invalid_train_file_path = None
            invalid_test_file_path = None

            if validation_status:
                # Use the pre-calculated paths from the config object
                valid_train_file_path = self.data_validation_config.valid_train_file_path
                valid_test_file_path = self.data_validation_config.valid_test_file_path

                # Save the data to the VALID location
                train_dataframe.to_csv(valid_train_file_path, index=False, header=True)
                test_dataframe.to_csv(valid_test_file_path, index=False, header=True)
                logger.info(f"Data saved to valid directory: {self.data_validation_config.valid_data_dir}")

            else:
                # Use the pre-calculated paths from the config object
                invalid_train_file_path = self.data_validation_config.invalid_train_file_path
                invalid_test_file_path = self.data_validation_config.invalid_test_file_path

                # Save the data to the INVALID location
                train_dataframe.to_csv(invalid_train_file_path, index=False, header=True)
                test_dataframe.to_csv(invalid_test_file_path, index=False, header=True)
                logger.info(f"Data saved to invalid directory due to drift: {self.data_validation_config.invalid_data_dir}")

            # --- 5. Create and Return Artifact ---
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=valid_train_file_path,
                valid_test_file_path=valid_test_file_path,
                invalid_train_file_path=invalid_train_file_path,
                invalid_test_file_path=invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logger.info(f"Data validation artifact created: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys)
