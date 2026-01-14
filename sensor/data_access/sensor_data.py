import os , sys
from typing import Optional

import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException

import logging
logger = logging.getLogger(__name__)

from sensor.constant.database import DATABASE_NAME
from sensor.configuration.mongo_db_connection import MongoDBClient

class SensorData:
    """
    Methods to interact with MongoDB collections and convert data to/from Pandas.
    """
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise SensorException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        try:
            # Determine which database to use
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]

            # Convert MongoDB cursor to list and then to DataFrame
            df = pd.DataFrame(list(collection.find()))

            if not df.empty and "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            logger.info(f"Exported {len(df)} records from {collection_name}")
            return df

        except Exception as e:
            raise SensorException(e, sys)

    def dump_csv_file_to_mongodb_collection(self, file_path: str, collection_name: str, database_name: Optional[str] = None):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = df.to_dict(orient="records")

            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]

            if records:
                collection.insert_many(records)
                logger.info(f"Dumped {len(records)} records into {collection_name}")

        except Exception as e:
            raise SensorException(e, sys)