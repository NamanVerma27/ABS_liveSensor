import os , sys
import logging
from dotenv import load_dotenv
import pymongo

import certifi
ca = certifi.where() # to handle SSL certificate verification

from sensor.exception import SensorException
from sensor.constant.env_variable import MONGODB_URL_KEY
from sensor.constant.database import DATABASE_NAME  , COLLECTION_NAME

load_dotenv() # load the environment variables from .env file

class MongoDBClient:
    Client = None # ensures only one connection is made to the database

    try:
        def __init__(self , database_name = DATABASE_NAME , collection_name = COLLECTION_NAME): 
            if MongoDBClient.Client is None:
                self.mongodb_url = os.getenv(MONGODB_URL_KEY)
                logging.info("Retrieved MongoDB URL from environment variables.")
            
            if self.mongodb_url is None:
                raise Exception(f"{MONGODB_URL_KEY} is not set in environment variables.")
            
            if "localhost" in self.mongodb_url:
                self.client = pymongo.MongoClient(self.mongodb_url)
            else:
                self.client = pymongo.MongoClient(self.mongodb_url , tlsCAFile=ca) # for secure connection

            self.database = self.client[database_name]
            self.collection = self.database[collection_name]
            logging.info(f"Connected to MongoDB database: {database_name}, collection: {collection_name}")
    
    except Exception as e:
        raise SensorException(e , sys)