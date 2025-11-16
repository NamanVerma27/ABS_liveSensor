import os , sys

from sensor.exception import SensorException
from sensor.logger import logging

from sensor.entity.config_entity import TrainingPipelineConfig , DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.components.data_ingestion import DataIngesion

from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataValidationArtifact
from sensor.components.data_validation import DataValidation

from sensor.entity.config_entity import DataPreprocessingConfig
from sensor.entity.artifact_entity import DataPreprocessingArtifact
from sensor.components.data_preprocessing import DataPreprocessing

from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import ModelTrainerArtifact
from sensor.components.model_trainer import ModelTrainer

class TrainPipeline:
    is_pipeline_running=False
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")
            data_ingestion = DataIngesion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except  Exception as e:
            raise  SensorException(e,sys)
        
    def start_data_validaton(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_data_preprocessing(self, data_validation_artifact: DataValidationArtifact) -> DataPreprocessingArtifact:
        try:
            data_preprocessing_config = DataPreprocessingConfig(training_pipeline_config=self.training_pipeline_config)
            data_preprocessing= DataPreprocessing(
                data_validation_artifact=data_validation_artifact,
                data_preprocessing_config=data_preprocessing_config
            )
            data_preprocessing_artifact = data_preprocessing.initiate_data_preprocessing()
            return data_preprocessing_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_model_trainer(self, data_preprocessing_artifact: DataPreprocessingArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(
                data_preprocessing_artifact=data_preprocessing_artifact,
                model_trainer_config=model_trainer_config
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)