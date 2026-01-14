import os, sys
import pymongo
import certifi

from sensor.exception import SensorException
from sensor.logger import logging

import logging
logger = logging.getLogger(__name__)

from sensor.constant.env_variable import MONGODB_URL_KEY
from sensor.constant.database import DATABASE_NAME

ca = certifi.where()

class MongoDBClient:
    """
    Class to establish a secure, singleton connection to MongoDB.
    """
    client = None  # Class-level variable to ensure a single connection

    def __init__(self, database_name=DATABASE_NAME):
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment variable {MONGODB_URL_KEY} is not set.")
                
                # Check for secure connection vs localhost
                if "localhost" in mongo_db_url:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
                else:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logger.info(f"Successfully connected to database: {self.database_name}")
            
        except Exception as e:
            raise SensorException(e, sys)