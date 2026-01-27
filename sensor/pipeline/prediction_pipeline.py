import os
import sys
import pandas as pd
import numpy as np
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.ml_model_components.model.model_resolver import ModelResolver
from sensor.utils.main_utils import load_object
from sensor.constant.training_pipeline import TARGET_COLUMN

class PredictionPipeline:

    def __init__(self):
        try:
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise SensorException(e, sys)

    def predict(self, dataframe: pd.DataFrame):
        """
        Logic: 
        1. Drops target column if present.
        2. Aligns columns to match training schema.
        3. Loads latest model and generates predictions.
        """
        try:
            logging.info("Starting prediction process...")

            # 1. Handle Target Column (if using training CSV for testing)
            if TARGET_COLUMN in dataframe.columns:
                logging.info(f"Target column '{TARGET_COLUMN}' found. Dropping for prediction.")
                dataframe = dataframe.drop(columns=[TARGET_COLUMN], axis=1)

            # 2. Check if a model exists
            if not self.model_resolver.is_model_exists():
                raise Exception("No model is currently available in the 'saved_models' directory.")

            # 3. Load the latest 'Champion' model (The SensorModel object)
            best_model_path = self.model_resolver.get_best_model_path()
            sensor_model = load_object(file_path=best_model_path)
            logging.info(f"Successfully loaded champion model from: {best_model_path}")

            # 4. Feature Alignment (The Fix for your error)
            # We extract the feature names the preprocessor was fitted on
            try:
                # If your preprocessor is a Scikit-Learn Pipeline/Transformer
                expected_features = sensor_model.preprocessor.feature_names_in_
                logging.info(f"Aligning {len(expected_features)} features with the model schema.")
                
                # Filter out the extra columns (ab_000, bn_000, etc.)
                dataframe = dataframe[expected_features]
            except AttributeError:
                logging.warning("Could not find 'feature_names_in_' in preprocessor. Proceeding with raw data.")

            # 5. Generate Predictions
            # SensorModel.predict internally calls preprocessor.transform then model.predict
            predictions = sensor_model.predict(dataframe)

            # 6. Optional: Convert numerical predictions back to labels
            # 0 -> neg, 1 -> pos
            df_with_predictions = dataframe.copy()
            df_with_predictions["prediction"] = predictions
            df_with_predictions["prediction"] = df_with_predictions["prediction"].replace({0: "neg", 1: "pos"})

            logging.info("Prediction completed successfully.")
            return df_with_predictions

        except Exception as e:
            raise SensorException(e, sys)