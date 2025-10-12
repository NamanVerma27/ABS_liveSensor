import sys
from sensor.exception import SensorException

from sensor.logger import logging

from sensor.utils import dump_csv_file_to_mongodb_collection


if __name__ == "__main__":
    # try:
    #     logging.info("Starting the sensor data ingestion process.")
    #     from sensor.utils import dump_csv_file_to_mongodb_collection

    #     # usage
    #     file_path = r"C:\Users\NAMAN VERMA\OneDrive\Desktop\ABS_sensorlive\aps_failure_training_set1.csv"
    #     database_name = "APS_project"
    #     collection_name = "sensor_data"

    #     dump_csv_file_to_mongodb_collection(file_path, database_name, collection_name)
    #     logging.info("Data ingestion completed successfully.")

    # except Exception as e:
    #     logging.error(f"An error occurred in the main execution: {e}")
    #     raise SensorException(e, sys)