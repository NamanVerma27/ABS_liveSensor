import os,sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline

from sensor.exception import SensorException
from sensor.logger import logging

from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.config_entity import DataPreprocessingConfig
from sensor.entity.artifact_entity import (
    DataValidationArtifact,
    DataPreprocessingArtifact,
)
from sensor.ml_model_components.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array_data, save_object

class DataPreprocessing:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_preprocessing_config: DataPreprocessingConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_preprocessing_config = data_preprocessing_config
        except Exception as e:
            raise SensorException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        try:
            logging.info("Creating data transformer object")
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            preprocessor = Pipeline(steps=[
                ('Imputer', simple_imputer),
                ('RobustScaler', robust_scaler)
            ])
            return preprocessor
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_preprocessing(self) -> DataPreprocessingArtifact:
        try:
            logging.info("Starting data preprocessing")

            # ------1. Read training and testing data------
            train_df = DataPreprocessing.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataPreprocessing.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Read training and testing data successfully")

            # ------2. Separate features and target variable------
            # Separate features and target variable for training data
            X_train = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            y_train = train_df[TARGET_COLUMN].replace(TargetValueMapping().to_dict())

            # Separate features and target variable for testing data
            X_test = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            y_test = test_df[TARGET_COLUMN].replace(TargetValueMapping().to_dict())
            logging.info("Separated features and target variable")

            # Get the data transformer object
            preprocessor = self.get_data_transformer_object()

            # ------3. Apply transformations------
            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)
            logging.info("Applied preprocessing transformations")

            # ------4. Handle class imbalance using SMOTETomek------
            smt = SMOTETomek(sampling_strategy='minority')
            X_train_resampled , y_train_resampled = smt.fit_resample(X_train_transformed , y_train)
            X_test_final = X_test_transformed # No resampling
            y_test_final = y_test             # on test data
            logging.info("Handled class imbalance using SMOTETomek on training data only")

            # ------5. Save the preprocessed data and preprocessing object------
            # Combine features and target variable for training data
            train_array = np.c_[X_train_resampled , y_train_resampled]
            test_array = np.c_[X_test_final , y_test_final]

            # Save the preprocessed training and testing data as numpy arrays
            save_numpy_array_data(self.data_preprocessing_config.processed_train_file_path , train_array)
            save_numpy_array_data(self.data_preprocessing_config.processed_test_file_path , test_array)
            logging.info("Saved preprocessed training and testing data")

            # Save the preprocessing object
            save_object(self.data_preprocessing_config.preprocessed_object_dir , preprocessor)
            logging.info("Saved preprocessing object")

            # Create and return the DataPreprocessingArtifact
            data_preprocessing_artifact = DataPreprocessingArtifact(
                preprocessed_object_file_path=self.data_preprocessing_config.preprocessed_object_dir,
                processed_train_file_path=self.data_preprocessing_config.processed_train_file_path,
                processed_test_file_path=self.data_preprocessing_config.processed_test_file_path
            )

            logging.info("Data preprocessing completed successfully")
            return data_preprocessing_artifact
        
        except Exception as e:
            raise SensorException(e, sys)
