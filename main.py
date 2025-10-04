from sensor.exception import SensorException

if __name__ == "__main__":
    try:
        raise Exception("This is a custom exception")
    except Exception as e:
        print(e)