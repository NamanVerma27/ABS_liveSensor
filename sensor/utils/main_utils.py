import os , sys
import yaml
from sensor.exception import SensorException

def read_yaml_file(file_path: str) -> dict:
    
    # Reads a YAML file and returns its contents as a dictionary

    try:
        with open(file_path , 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise SensorException(e , sys)
    
def write_yaml_file(file_path: str , content: object , replace: bool = False) -> None:
    # Writes a dictionary to a YAML file
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
                
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok=True)

        with open(file_path , 'w') as yaml_file:
            yaml.dump(content , yaml_file)
    
    except Exception as e:
        raise SensorException(e , sys)