import os,sys
import shutil

from sensor.logger import logging as global_logging
from sensor.exception import SensorException
logger = global_logging.getLogger(__name__)

from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import(ModelPusherArtifact , 
                                          ModelEvaluationArtifact
                                          )

class ModelPusher:
    def __init__(self , model_pusher_config : ModelPusherConfig ,
                model_evaluation_artifact : ModelEvaluationArtifact):
            try:
                self.model_pusher_config = model_pusher_config
                self.model_evaluation_artifact = model_evaluation_artifact
            except Exception as e:
                raise SensorException(e , sys)
    
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logger.info("Starting model pusher stage")
            # Using the challenger path confirmed by evaluation
            trained_model_path = self.model_evaluation_artifact.trained_model_path

            # 1. Copy the trained model to the model pusher directory
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path) , exist_ok=True)
            shutil.copy(src=trained_model_path , dst=model_file_path)
            logger.info(f"Copied trained model from {trained_model_path} to {model_file_path}")
            
            # 2. Copy the trained model to the saved model directory for deployment
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)
            logger.info(f"Copied trained model from {trained_model_path} to {saved_model_path}")
            
            # 3. Create and return the ModelPusherArtifact
            model_pusher_artifact = ModelPusherArtifact(
                saved_model_path=saved_model_path,
                model_file_path=model_file_path
            )
            logger.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
            
        except Exception as e:
            raise SensorException(e , sys)