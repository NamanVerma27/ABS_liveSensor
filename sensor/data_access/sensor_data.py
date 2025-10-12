import os , sys
from typing import Optional

import pandas as pd
from sensor.logger import logging

from sensor.exception import SensorException
from sensor.constant.database import DATABASE_NAME, COLLECTION_NAME
from sensor.configuration.mongo_db_connection import MongoDBClient

class SensorData:
    # to get collection as dataframe

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME , collection_name=COLLECTION_NAME)

        except Exception as e:
            raise SensorException(e , sys)
        
    def dump_csv_file_to_mongodb_collection(self, file_path: str, collection_name: str, database_name: Optional[str] = None) -> None:

        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Reset index to ensure a clean DataFrame
            df.reset_index(drop=True, inplace=True)

            # Convert the DataFrame to a list of dicts (each dict = one document)
            records = df.to_dict(orient='records')

            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            if records:
                # Insert the records into the specified MongoDB collection
                collection.insert_many(records)
                logging.info(f"Inserted {len(records)} records into {database_name}.{collection_name}")
            
            self.mongo_client.close()

        except Exception as e:
            raise SensorException(e , sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            # Fetch all documents from the collection
            data = list(collection.find())

            if data:
                # Convert the list of documents to a DataFrame
                df = pd.DataFrame(data)

                # Drop the MongoDB-specific '_id' field if it exists
                if '_id' in df.columns:
                    df.drop(columns=['_id'], inplace=True)

                logging.info(f"Exported {len(df)} records from {database_name}.{collection_name} to DataFrame")
            else:
                logging.info(f"No records found in {database_name}.{collection_name}")
                df = pd.DataFrame()  # Return an empty DataFrame if no data

            self.mongo_client.close()
            return df
        
        except Exception as e:
            raise SensorException(e , sys)