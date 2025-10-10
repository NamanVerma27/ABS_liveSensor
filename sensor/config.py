from dataclasses import dataclass
import os
import pymongo

# Configuration class to hold MongoDB connection details
@dataclass 

class EnvironmentConfig:
    mongo_db_url: str = os.getenv("MONGO_DB_URL")

# Initialize configuration
config = EnvironmentConfig()

mongo_client = pymongo.MongoClient(config.mongo_db_url)  #MongoDB client instance