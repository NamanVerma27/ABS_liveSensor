import logging
from datetime import datetime
import os , sys

LOG_FILE_NAME = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = logs_path = os.path.join(os.getcwd() , "logs" , LOG_FILE_NAME)
os.makedirs(os.path.dirname(logs_path) , exist_ok = True)

logging.basicConfig(

    filename = LOG_FILE_PATH,
    format = "[%(asctime)s] %(lineno)s %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO

)