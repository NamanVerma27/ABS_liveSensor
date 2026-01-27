import os, sys
import pandas as pd
from sensor.logger import logging as global_logging
from sensor.exception import SensorException

import logging
logger = logging.getLogger(__name__)

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
        try:
            logger.info("Starting prediction process")
            
            # 1. Automatic Column Cleanup
            # If the user uploads the training CSV, we MUST drop the target column
            if TARGET_COLUMN in dataframe.columns:
                logger.info(f"Dropping target column: {TARGET_COLUMN} from input data")
                dataframe = dataframe.drop(columns=[TARGET_COLUMN], axis=1)

            # 2. Find the Latest 'Champion' Model
            if not self.model_resolver.is_model_exists():
                raise Exception("No model available for prediction. Please run the training pipeline first.")

            latest_model_path = self.model_resolver.get_best_model_path()
            
            # 3. Load the Model (which includes the preprocessor wrapper)
            model = load_object(file_path=latest_model_path)
            
            # 4. Generate Predictions
            y_pred = model.predict(dataframe)
            
            # 5. Map the results back to labels (optional but helpful)
            # Assuming 0 is 'neg' and 1 is 'pos'
            dataframe['prediction'] = y_pred
            dataframe['prediction'].replace({0: "neg", 1: "pos"}, inplace=True)
            
            return dataframe

        except Exception as e:
            raise SensorException(e, sys)