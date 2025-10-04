from sensor.exception import SensorException

from sensor.logger import logging



if __name__ == "__main__":
    try:
        raise Exception("This is a custom exception")
    except Exception as e:
        print(e)