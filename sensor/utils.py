import pandas as pd
from sensor.config import mongo_client

def dump_csv_file_to_mongodv_collection(file_path:str , database_name:str, collection_name:str) -> None:

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Reset index to ensure a clean DataFrame
        df.reset_index(drop=True, inplace=True)

        # Convert the DataFrame to a list of dicts (each dict = one document)
        records = df.to_dict(orient='records')

        if records:
            # Insert the records into the specified MongoDB collection
            mongo_client[database_name][collection_name].insert_many(records)
            print(f"Inserted {len(records)} records into {database_name}.{collection_name}")
        
        client.close()

    except Exception as e:
        print(f"An error occurred: {e}")