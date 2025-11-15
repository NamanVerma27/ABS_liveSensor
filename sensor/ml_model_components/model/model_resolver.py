# model_resolver.py

import os
from sensor.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

class ModelResolver:

    def __init__(self, model_dir=SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise e

    def get_best_model_path(self) -> str:
        """
        Finds the path to the latest saved model.
        """
        try:
            # Get all subdirectory names (which are timestamps)
            timestamps = list(map(int, os.listdir(self.model_dir)))
            latest_timestamp = max(timestamps)
            latest_model_path = os.path.join(
                self.model_dir, f"{latest_timestamp}", MODEL_FILE_NAME
            )
            return latest_model_path
        except Exception as e:
            raise e

    def is_model_exists(self) -> bool:
        """
        Checks if any model is saved and if the latest model file exists.
        """
        try:
            if not os.path.exists(self.model_dir):
                return False

            timestamps = os.listdir(self.model_dir)
            if len(timestamps) == 0:
                return False
            
            latest_model_path = self.get_best_model_path()

            if not os.path.exists(latest_model_path):
                return False

            return True
        except Exception as e:
            raise e